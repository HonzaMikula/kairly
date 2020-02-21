import io
import html
from datetime import datetime
from decimal import ConversionSyntax, Decimal
from operator import attrgetter
import urllib.parse

import requests
import pytz
import orjson as json
from PIL import Image
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q, Sum
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound)
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.utils.timezone import now as timezone_now
from django.views import View
from django.views.decorators.http import require_POST

from credits.utils import get_user_credits, pay_author_subscription, pay_newspaper_subscription
from users.models import User
from utils.decorators import ajax_login_required
from utils.html import convert_data_uris, sanitize
from utils.json import JsonResponse, Ref, entities_json_response
from utils.upload import file_from_data_uri
from .models import (Backlog, BacklogPost, Issue, Newspaper, CoEditor, Post, Subscription,
                     SubscriptionToAuthor, round_fair_price)
from .period import parse_periodicity
from .signals import post_publish
from .utils import create_post_link

AUTOR_POSTS_PAGE_SIZE = 20

SUBSCRIPTIONS_CACHE_KEY = 'subscriptions-{}'


@ajax_login_required
@entities_json_response
def subscriptions(request, entities):
    cache_key = SUBSCRIPTIONS_CACHE_KEY.format(request.user.id)
    cached = cache.get(cache_key)

    if cached:
        refs, response = cached
        entities.add_references(refs)
        return response

    entities.track_references = set()

    now = datetime.now(request.user.tzinfo)
    subscribed_authors = []
    query = SubscriptionToAuthor.objects.filter(
        Q(valid_to__gt=now) | Q(renewal=True),
        user=request.user
    )

    valid_to = None

    for s in query:
        subscribed_authors.append(s.to_json(entities))
        valid_to = min(valid_to, s.valid_to) if valid_to else s.valid_to

    subscribed_newspapers = []
    query = Subscription.objects.filter(
        Q(valid_to__gt=now) | Q(renewal=True),
        user=request.user
    )

    for s in query:
        subscribed_newspapers.append(s.to_json(entities))
        valid_to = min(valid_to, s.valid_to) if valid_to else s.valid_to

    response = {
        'subscriptions': {
            "authors": subscribed_authors,
            "newspapers": subscribed_newspapers,
        }
    }

    cache.set(cache_key, (entities.track_references, response), (valid_to - now).total_seconds() if valid_to else None)
    entities.track_references = None
    return response


@ajax_login_required
def user_backlog(request):
    user_backlog = {}  # do not use defaultdict becase urjson can serialize by default
    query = BacklogPost.objects \
        .filter(Q(backlog__newspaper__editor=request.user) | Q(backlog__newspaper__coeditor__editor=request.user)) \
        .select_related('backlog')

    items = list(query)
    newspaper_ids = set(bp.backlog.newspaper_id for bp in items)

    full_names = {}
    to_load = []
    newspaper_refs = [Ref(Newspaper, newspaper_id) for newspaper_id in newspaper_ids]
    cached = cache.get_many([ref.cache_key for ref in newspaper_refs])
    for ref in newspaper_refs:
        cached_ent = cached.get(ref.cache_key)
        if cached_ent:
            full_names[ref.id] = cached_ent[0]
        else:
            to_load.append(ref.id)

    if to_load:
        for n in Newspaper.objects.filter(id__in=to_load).select_related('editor'):
            full_names[n.id] = n.full_name

    for bp in items:
        full_name = full_names[bp.backlog.newspaper_id]
        user_backlog.setdefault(str(bp.post_id), {})[full_name] = bp.backlog.name

    return JsonResponse({
        "backlog": user_backlog
    })


@entities_json_response
def recent_issues(request, entities):
    count = int(request.GET.get('count', 3))
    if count < 1 or count > 10:
        return HttpResponse('Invalid count.', status=400)

    issues = list(Issue.objects.all().order_by('-published')[:count])
    newspaper_ids = [issue.newspaper_id for issue in issues]
    newspapers = {
        newspaper.id: newspaper for newspaper in
        Newspaper.objects.filter(id__in=newspaper_ids)
    }

    resp = {
        'issues': []
    }
    for issue in issues:
        issue.newspaper = newspapers[issue.newspaper_id]
        resp['issues'].append(issue.to_json(entities, posts=True))

    return resp


@entities_json_response
def recent_posts(request, entities):
    posts = Post.objects.filter(draft=False, published__lt=timezone.now())\
        .exclude(kind__in=[Post.RECOMMENDATION, Post.LINK])\
        .order_by('-published')[:12]

    return {
        'posts': [post.to_json(entities) for post in posts]
    }


def delete_newspaper(request, newspaper):
    if newspaper.editor_id != request.user.id:
        return HttpResponseForbidden()
    newspaper.delete()
    return HttpResponse(status=204)


class NewspaperView(View):
    @method_decorator(entities_json_response)
    def get(self, request, entities, username, newspapeper_slug):
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)

        issue_no = request.GET.get('issue')
        if issue_no:
            try:
                issue_no = int(issue_no)
            except ValueError:
                return HttpResponse('Invalid issue number.', status=400)
            issue = get_object_or_404(Issue, newspaper=newspaper, number=issue_no)
        else:
            try:
                issue = Issue.objects.filter(newspaper=newspaper).order_by('-number')[0]
            except IndexError:
                issue = None

        resp = {
            'newspaper': entities.make_ref(Newspaper, newspaper),
            'issue': None,
            'links': {}
        }

        if issue:
            resp['issue'] = issue.to_json(entities)

            try:
                prev_num = Issue.objects.filter(newspaper=newspaper, number__lt=issue.number).order_by('-number').values_list('number', flat=True)[0]
                resp['links']['prev'] = '/{}/{}'.format(newspaper.full_name, prev_num)
            except IndexError:
                pass
            try:
                next_num = Issue.objects.filter(newspaper=newspaper, number__gt=issue.number).order_by('number').values_list('number', flat=True)[0]
                resp['links']['next'] = '/{}/{}'.format(newspaper.full_name, next_num)
            except IndexError:
                pass

            if request.user.is_authenticated:
                if Post.objects.filter(author=request.user, kind=Post.RECOMMENDATION, ref_issue=issue).exists():
                    resp['recommended'] = [resp['issue']['id']]  # pylint: disable=unsubscriptable-object
                else:
                    resp['recommended'] = []

        return resp

    @ajax_login_required
    @transaction.atomic
    @method_decorator(entities_json_response)
    def patch(self, request, entities, username, newspapeper_slug):
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
        payload = json.loads(request.body.decode('utf-8'))

        if newspaper.editor_id != request.user.id:
            return HttpResponseForbidden()

        if 'title' in payload:
            newspaper.title = payload['title'].strip()

        if 'description' in payload:
            newspaper.description = payload['description'].strip()

        if 'periodicity' in payload:
            try:
                periodicity = parse_periodicity(payload['periodicity'])
            except ValueError as e:
                return HttpResponseBadRequest(str(e))
            newspaper.period = periodicity.frequency
            newspaper.period_time = periodicity.time
            newspaper.period_dow = periodicity.dow

        if 'price' in payload:
            price = Decimal(payload['price'])
            if price not in settings.ALLOWED_PRICE_LEVELS:
                return HttpResponseBadRequest('invalid price')
            newspaper.price = price

        image = payload.get('image')
        if image:
            image = file_from_data_uri(image, "{}-{}".format(request.user.username, newspaper.slug))
            newspaper.image = image

        if 'coEditors' in payload:
            editors = {u.id for u in User.objects.filter(username__in=payload['coEditors']).exclude(id=newspaper.editor_id)}
            actual = set(newspaper.co_editors.values_list('id', flat=True))

            to_del = list(actual - editors)
            to_add = list(editors - actual)
            if to_del:
                CoEditor.objects.filter(newspaper=newspaper, editor_id__in=to_del).delete()
            if to_add:
                CoEditor.objects.bulk_create(
                    [CoEditor(newspaper=newspaper, editor_id=eid) for eid in to_add]
                )

        newspaper.save()

        return {
            'newspaper': newspaper.to_json(entities),
        }

    @ajax_login_required
    @transaction.atomic
    def delete(self, request, username, newspapeper_slug):
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)

        if newspaper.editor_id != request.user.id:
            return HttpResponseForbidden()

        newspaper.delete()
        return HttpResponse(status=204)


@entities_json_response
def author_detail(request, entities, username):
    author = get_object_or_404(User, username=username)

    newspapers = list(Newspaper.objects.filter(editor=author, archived=False))
    newspapers.sort(key=attrgetter('likes'), reverse=True)

    resp = {
        'author': entities.make_ref(User, author),
        'newspapers': []
    }

    for newspaper in newspapers:
        resp['newspapers'].append(entities.make_ref(Newspaper, newspaper))

    return resp


@entities_json_response
def author_posts(request, entities, username):
    try:
        offset = int(request.GET.get('cursor', 0))
    except ValueError:
        offset = 0

    author = get_object_or_404(User, username=username)

    posts_query = Post.objects.filter(
        author=author,
        draft=False,
        published__lt=timezone.now(),
        hidden=False,
    )

    if request.GET.get('skipRecommendations') == '1':
        posts_query = posts_query.exclude(kind__in=[Post.RECOMMENDATION, Post.LINK])
    posts_query = posts_query.order_by('-published')[offset:offset + AUTOR_POSTS_PAGE_SIZE]

    posts = [post.to_json(entities, short=True) for post in posts_query]
    return {
        'posts': posts,
        'cursor': offset + AUTOR_POSTS_PAGE_SIZE if len(posts) == AUTOR_POSTS_PAGE_SIZE else None
    }


@ajax_login_required
@transaction.atomic
@entities_json_response
def newspaper_backlog(request, entities, username, newspapeper_slug):
    newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
    if newspaper.editor_id != request.user.id:
        if request.user not in newspaper.co_editors.all():
            return HttpResponseForbidden()

    if request.method == 'GET':
        name = 'upcoming'  # DEV
        result = {
            'backlogs': {},
            'posts': {}
        }

        newspaper_ref = entities.make_ref(Newspaper, newspaper.id)
        for name in ['considered', 'upcoming', 'next']:
            try:
                backlog = Backlog.objects.get(newspaper=newspaper, name=name)
                data = backlog.to_json(entities)
                result['backlogs'][name] = data
                result['posts'].update(data['posts'])
                del data['posts']
            except Backlog.DoesNotExist:
                result['backlogs'][name] = {
                    'name': name,
                    'newspaper': newspaper_ref,
                    'layout': []
                }

        editor_tz = pytz.timezone(newspaper.editor.timezone)
        now = timezone_now().astimezone(editor_tz)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        issue_ids = Issue.objects.filter(newspaper=newspaper, published__gte=month_start).values_list('id', flat=True)
        cost = Post.objects.filter(issuepost__issue__id__in=issue_ids).aggregate(Sum('price'))['price__sum']
        if cost is None:
            cost = Decimal(0)

        result['currentMonth'] = {
            'priorIssues': len(issue_ids),
            'priorIssuesCost': str(cost),
            'upcommingIssues': len(newspaper.current_month_upcomming_issues())
        }
        return result

    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))

        for name, layout in payload.items():
            if name not in ['considered', 'upcoming', 'next']:
                raise HttpResponseBadRequest('Invalid backlog name')

            try:
                backlog = Backlog.objects.get(newspaper=newspaper, name=name)
            except Backlog.DoesNotExist:
                backlog = Backlog(newspaper=newspaper, name=name)
            backlog.save_layout(layout)

        # TODO nice to have delete unreferenced comments
        return HttpResponse(status=204)

    return HttpResponse('405 Method Not Allowed', status=405)


@ajax_login_required
@require_POST
@transaction.atomic
@entities_json_response
def create_link(request, entities):
    payload = json.loads(request.body.decode('utf-8'))
    url = payload['url']

    if '://' not in url:
        url = 'http://' + url

    try:
        post = create_post_link(url, None, hidden=True)
    except IOError as e:
        return JsonResponse({
            'error': str(e)
        }, status=409)

    return {
        'post': post.to_json(entities)
    }


class NewspaperSubscriptionView(View):

    @ajax_login_required
    @transaction.atomic
    @method_decorator(entities_json_response)
    def post(self, request, entities, username, newspapeper_slug):
        now = datetime.now(request.user.tzinfo)
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)

        payload = json.loads(request.body.decode('utf-8'))
        allow_suspended = payload.get('allowSuspended')
        donation = payload.get('donation')
        if donation:
            donation = Decimal(donation)
            if donation < 0 or donation > 100000:
                return HttpResponseBadRequest("Donation must be between range from 0 and 100000")

        credits = get_user_credits(request.user.id)

        try:
            # just reactivate renewal if current cancelled subscription exists
            subscription = Subscription.objects.get(
                Q(valid_to__gt=now) | Q(renewal=True),
                user=request.user, newspaper=newspaper)
        except Subscription.DoesNotExist:
            subscription = None

        transaction.on_commit(lambda: cache.delete(SUBSCRIPTIONS_CACHE_KEY.format(request.user.id)))

        if subscription and not subscription.suspended:
            subscription.renewal = True
            subscription.donation = donation or Decimal(0)
            subscription.save()
        else:
            donation = donation or Decimal(0)
            has_credits = credits >= newspaper.price + donation

            if not has_credits and not allow_suspended:
                return HttpResponse("Insufficient credit.", status=402)

            if not subscription:
                subscription = Subscription(
                    user=request.user,
                    newspaper=newspaper
                )

            if has_credits:
                subscription.suspended = False
                subscription.valid_from = now
                subscription.valid_to = now + relativedelta(months=1)
            else:
                if not subscription.suspended:
                    subscription.suspended = True
                    subscription.valid_from = now - relativedelta(months=1)
                    subscription.valid_to = now

            subscription.donation = donation
            subscription.save()

            if has_credits:
                credits -= newspaper.price + donation
                pay_newspaper_subscription(subscription)

        return {
            'credits': str(credits),
            'subscription': subscription.to_json(entities)
        }

    @ajax_login_required
    @transaction.atomic
    @method_decorator(entities_json_response)
    def delete(self, request, entities, username, newspapeper_slug):
        now = datetime.now(request.user.tzinfo)
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)

        subscription = Subscription.objects.filter(
            Q(renewal=True) | Q(suspended=True),
            user=request.user, newspaper=newspaper
        ).order_by('-valid_to').first()

        if subscription is None:
            return HttpResponseNotFound()

        transaction.on_commit(lambda: cache.delete(SUBSCRIPTIONS_CACHE_KEY.format(request.user.id)))

        if newspaper.price == 0:
            subscription.delete()
            return {
                'subscription': None
            }

        subscription.renewal = False
        subscription.suspended = False
        subscription.save()

        return {
            'subscription': subscription.to_json(entities) if subscription.valid_to > now else None
        }


class AuthorSubscriptionView(View):

    @ajax_login_required
    @transaction.atomic
    @method_decorator(entities_json_response)
    def post(self, request, entities, username):
        now = datetime.now(request.user.tzinfo)
        author = get_object_or_404(User, username=username)
        payload = json.loads(request.body.decode('utf-8'))

        if 'periodicity' in payload:
            try:
                periodicity = parse_periodicity(payload['periodicity'])
            except ValueError as e:
                return HttpResponseBadRequest(str(e))
        else:
            periodicity = None

        allow_suspended = payload.get('allowSuspended')
        keep_status = payload.get('keepStatus')
        donation = payload.get('donation')
        if donation:
            donation = Decimal(donation)
            if donation < 0 or donation > 100000:
                return HttpResponseBadRequest("Donation must be between range from 0 and 100000")

        credits = get_user_credits(request.user.id)

        try:
            # Handle unique together manually, because
            # mysql ignores key when one of values is NULL (usually topic)
            # TODO when topic removed, is it still needed?
            # There is still place for race condition!
            subscription = SubscriptionToAuthor.objects.get(
                Q(valid_to__gt=now) | Q(renewal=True),
                user=request.user, author=author,
            )
        except SubscriptionToAuthor.DoesNotExist:
            if not periodicity:
                return HttpResponseBadRequest("Periodicity is required.")
            subscription = None

        transaction.on_commit(lambda: cache.delete(SUBSCRIPTIONS_CACHE_KEY.format(request.user.id)))

        if subscription and not subscription.suspended:
            if periodicity:
                subscription.set_periodicity(periodicity)

            if not keep_status and not subscription.renewal:
                subscription.renewal = True

            if donation is not None:
                subscription.donation = donation

            subscription.save()
        else:
            donation = donation or Decimal(0)
            has_credits = credits >= author.price + donation

            if not has_credits and not allow_suspended:
                return HttpResponse("Insufficient credit.", status=402)

            if not subscription:
                subscription = SubscriptionToAuthor(
                    user=request.user,
                    author=author
                )

            if has_credits:
                subscription.suspended = False
                subscription.valid_from = now
                subscription.valid_to = now + relativedelta(months=1)
            else:
                if not subscription.suspended:
                    subscription.suspended = True
                    subscription.valid_from = now - relativedelta(months=1)
                    subscription.valid_to = now

            if periodicity:
                subscription.set_periodicity(periodicity)

            subscription.donation = donation
            subscription.save()

            if has_credits:
                pay_author_subscription(subscription)
                credits -= author.price + donation

        return {
            'credits': str(credits),
            'subscription': subscription.to_json(entities)
        }

    @ajax_login_required
    @transaction.atomic
    @method_decorator(entities_json_response)
    def delete(self, request, entities, username):
        author = get_object_or_404(User, username=username)
        now = datetime.now(request.user.tzinfo)

        subscription = SubscriptionToAuthor.objects.filter(
            Q(renewal=True) | Q(suspended=True),
            user=request.user, author=author,
        ).order_by('-valid_to').first()

        if not subscription:
            return HttpResponseNotFound()

        transaction.on_commit(lambda: cache.delete(SUBSCRIPTIONS_CACHE_KEY.format(request.user.id)))

        if author.price == 0:
            subscription.delete()
            return {
                'subscription': None
            }

        subscription.renewal = False
        subscription.suspended = False
        subscription.save()

        return {
            'subscription': subscription.to_json(entities) if subscription.valid_to > now else None
        }


def validate_post_attributes(request, payload, draft):
    kind = payload['type']

    if kind == Post.NEWSPAPER:
        title = payload['title'].strip()
        perex = sanitize(payload['perex'].strip())
        content = sanitize(payload['content'].strip())

        if not title:
            raise ValueError("No title")
        if not draft and not perex:
            raise ValueError("No perex")

        perex = convert_data_uris(perex)
        content = convert_data_uris(content)
    elif kind == Post.COMMENT:
        title = payload['title'].strip()
        content = sanitize(payload['content'].strip())

        perex = None
        content = convert_data_uris(content)
    elif kind == Post.TWEET:
        raw_content = payload['content'].strip()

        if not raw_content:
            raise ValueError("Tweet is empty")
        if len(raw_content) > 320:
            raise ValueError("Content too long.")

        title = "{}: {}...".format(request.user.username, raw_content[:60])
        perex = None
        content = html.escape(raw_content)
    else:
        raise ValueError("Invalid post kind.")

    return {
        'kind': kind,
        'title': title,
        'perex': perex,
        'content': content
    }


class DraftsView(View):
    @ajax_login_required
    @method_decorator(entities_json_response)
    def get(self, request, entities):
        posts = Post.objects.filter(author=request.user, draft=True, kind=Post.NEWSPAPER).order_by('-published')
        return{
            'posts': [post.to_json(entities) for post in posts]
        }

    @ajax_login_required
    @method_decorator(entities_json_response)
    def post(self, request, entities):
        payload = json.loads(request.body.decode('utf-8'))

        try:
            attrs = validate_post_attributes(request, payload, True)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

        post = Post.objects.create(
            draft=True,
            protected=False,
            author=request.user,
            hidden=payload['type'] == Post.COMMENT,
            **attrs
        )

        return {
            'post': post.to_json(entities)
        }


class DraftDetailView(View):

    @ajax_login_required
    @method_decorator(entities_json_response)
    def get(self, request, entities, post_id):
        # user can get (and patch) also published posts
        post = get_object_or_404(Post, author=request.user, id=post_id)
        return {
            'post': post.to_json(entities)
        }

    @ajax_login_required
    @method_decorator(entities_json_response)
    def patch(self, request, entities, post_id):
        """User can patch published posts and such use case is handled
        also by this view despite its name."""
        post = get_object_or_404(Post, author=request.user, id=post_id)
        payload = json.loads(request.body.decode('utf-8'))

        try:
            attrs = validate_post_attributes(request, payload, post.draft)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

        post.__dict__.update(attrs)
        post.save(recalculate_weight=True)

        return {
            'post': post.to_json(entities)
        }

    @ajax_login_required
    def delete(self, request, post_id):
        post = get_object_or_404(Post, author=request.user, id=post_id, draft=True)
        post.delete()
        return HttpResponse(status=204)


@ajax_login_required
def draft_fair_price(request, post_id):
    post = get_object_or_404(Post, author=request.user, id=post_id, draft=True)
    price = post.calculate_fair_price()

    if price is None:
        price = round_fair_price(request.user.price / 5)

    return JsonResponse({
        'price': f"{price:.2f}"
    })


@ajax_login_required
@require_POST
@transaction.atomic
@entities_json_response
def publish_draft(request, entities, post_id):
    post = get_object_or_404(Post, author=request.user, id=post_id, draft=True)
    payload = json.loads(request.body.decode('utf-8'))

    if post.kind == Post.NEWSPAPER and post.perex == '':
        return JsonResponse({'error': 'Perex is empty'}, status=400)

    try:
        price = Decimal(payload['price']).quantize(Decimal('0.01'))
    except ConversionSyntax:
        return JsonResponse({'error': "Invalid syntax"}, status=400)

    if price < 0:
        return JsonResponse({'error': "Price can't be negative"}, status=400)

    if price > 100000:
        return JsonResponse({'error': "Price too high"}, status=400)

    post.price = price
    post.draft = False
    post.published = timezone_now()
    post.save()

    post_publish.send(sender=publish_draft, post=post)

    return {
        'post': post.to_json(entities)
    }


@entities_json_response
def post(request, entities, username, post_slug):
    post = get_object_or_404(Post, author__username=username, slug=post_slug, draft=False, published__lt=timezone.now())

    # Doesn't work, post can be part of multiple issues or just related to author
    # newspaper = Issue.objects.get(posts=post).newspaper
    # is_subscribed = Subscription.objects.filter(user=request.user, newspaper=newspaper).count() > 0
    # if not is_subscribed:
    #     return HttpResponse('402 Payment Required', status=402)

    # editorials = []
    # query = IssuePost.objects.filter(post=post, editorial__isnull=False) \
    #     .select_related('editorial', 'issue') \
    #     .order_by('issue_id', 'ordering')

    # for issue_post in query:
    #     item = issue_post.editorial.to_json(entities)
    #     item['issue'] = issue_post.issue.to_json(entities, posts=False)
    #     del item['position']
    #     editorials.append(item)

    resp = {
        'post': post.to_json(entities),
        # 'editorials': editorials
        'editorials': []
    }

    if request.user.is_authenticated:
        resp['recommended'] = Post.objects.filter(
            author=request.user, kind=Post.RECOMMENDATION, ref_post=post).exists()

    return resp


def get_type_from_data_uri(data):
    return data.split(';', maxsplit=1)[0].split('/')[1]


@ajax_login_required
@require_POST
@transaction.atomic
@entities_json_response
def start_newspaper(request, entities, username):
    author = get_object_or_404(User, username=username)
    payload = json.loads(request.body.decode('utf-8'))

    if author.id != request.user.id:
        return HttpResponseForbidden()

    title = payload['title'].strip()
    description = payload['description'].strip()

    try:
        periodicity = parse_periodicity(payload['periodicity'])
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    base_slug = slugify(title)
    slug = base_slug
    slug_suffix = 1
    while Newspaper.objects.filter(editor=author, slug=slug).exists():
        slug_suffix += 1
        slug = '{}-{}'.format(base_slug, slug_suffix)

    image = payload.get('image')
    if image:
        image = file_from_data_uri(image, "{}-{}".format(author.username, base_slug))

    price = Decimal(payload['price'])
    if price not in settings.ALLOWED_PRICE_LEVELS:
        return JsonResponse({'error': 'invalid price'}, status=400)

    newspaper = Newspaper.objects.create(
        title=title,
        slug=slug,
        description=description,
        image=image,
        price=price,
        period=periodicity.frequency,
        period_time=periodicity.time,
        period_dow=periodicity.dow,
        editor=author
    )

    CoEditor.objects.bulk_create(
        [
            CoEditor(newspaper=newspaper, editor_id=u.id)
            for u in User.objects.filter(username__in=payload['coEditors']).exclude(id=author.id)
        ]
    )

    return {
        'newspaper': entities.make_ref(Newspaper, newspaper)
    }


class PostRecommendationView(View):

    @ajax_login_required
    @transaction.atomic
    @method_decorator(entities_json_response)
    def post(self, request, entities, username, post_slug):
        post = get_object_or_404(Post, author__username=username, slug=post_slug, draft=False)

        if post.kind == Post.RECOMMENDATION:
            return JsonResponse({'error': "Recommendation post can't be recommended."}, status=400)

        if Post.objects.filter(kind=Post.RECOMMENDATION, author=request.user, ref_post=post).exists():
            return JsonResponse({'error': "Post is already recommended."}, status=400)

        recommendation = Post.objects.create(
            title=post.title,
            kind=Post.RECOMMENDATION,
            author=request.user,
            ref_post=post,
            protected=False
        )

        return {
            'post': recommendation.to_json(entities)
        }

    @ajax_login_required
    @transaction.atomic
    def delete(self, request, username, post_slug):
        post = get_object_or_404(Post, author__username=username, slug=post_slug, draft=False)
        recommendation = get_object_or_404(Post, author=request.user, ref_post=post, kind=Post.RECOMMENDATION)
        recommendation.delete()

        return JsonResponse({})


class IssueRecommendationView(View):

    @ajax_login_required
    @transaction.atomic
    @method_decorator(entities_json_response)
    def post(self, request, entities, username, newspapeper_slug, issue_number):
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
        issue = get_object_or_404(Issue, newspaper=newspaper, number=issue_number)

        if Post.objects.filter(kind=Post.RECOMMENDATION, author=request.user, ref_issue=issue).exists():
            return JsonResponse({'error': "Issue is already recommended."}, status=400)

        recommendation = Post.objects.create(
            title=f'{newspaper.title} #{issue.number}',
            kind=Post.RECOMMENDATION,
            author=request.user,
            ref_issue=issue,
            protected=False
        )

        return {
            'post': recommendation.to_json(entities)
        }

    @ajax_login_required
    @transaction.atomic
    def delete(self, request, username, newspapeper_slug, issue_number):
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
        issue = get_object_or_404(Issue, newspaper=newspaper, number=issue_number)
        recommendation = get_object_or_404(Post, author=request.user, ref_issue=issue, kind=Post.RECOMMENDATION)
        recommendation.delete()

        return JsonResponse({})


def media_proxy(request):
    src = request.GET['src']
    slug = request.GET['post']
    size = request.GET.get('size')

    if size != 'timeline':
        return HttpResponseBadRequest("Invalid size")

    cache_key = f'media-{slug}-{src}-{size}'

    cached = cache.get(cache_key)
    if cached:
        if 'status' in cached and cached['status'] == 404:
            return HttpResponseNotFound()
        return HttpResponse(cached['content'], content_type=cached['content-type'])

    perex, source = Post.objects.filter(slug=slug).values_list('perex', 'source')[0]
    perex_unespaced = html.unescape(perex)
    norm_src = src.replace('http://', '').replace('https://', '')

    if norm_src not in perex_unespaced and urllib.parse.unquote_plus(norm_src) not in perex_unespaced:
        print(f'{src} not found in post {slug}')
        return HttpResponseBadRequest("Post doesn't contain such media object")

    ua = request.META.get('HTTP_USER_AGENT', settings.DEFAULT_USER_AGENT)

    if src.startswith('//'):
        if source is None:
            # should never happen
            src = 'http:' + source
        else:
            src = source.split('//')[0] + src

    resp = requests.get(src, headers={'User-Agent': ua})

    TIMELINE_WIDTH = 254

    try:
        orig_image = image = Image.open(io.BytesIO(resp.content))
    except OSError:
        cache.set(cache_key, {'status': 404}, 60)
        return HttpResponseNotFound()

    if image.width > TIMELINE_WIDTH:
        dim = (TIMELINE_WIDTH, int(image.height * TIMELINE_WIDTH / image.width))
        image = image.resize(dim, Image.LANCZOS)
        image.format = orig_image.format

    buf = io.BytesIO()
    image.save(buf, format=image.format)
    content = buf.getvalue()
    content_type = resp.headers.get('Content-Type')

    if resp.ok:
        cache.set(cache_key, {
            'content-type': content_type,
            'content': content,
            'size': f'{image.width}x{image.height}'
        }, 14 * 86400)

    return HttpResponse(content, status=resp.status_code, content_type=content_type)
