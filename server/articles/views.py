import html
from collections import defaultdict
from datetime import datetime
from decimal import ConversionSyntax, Decimal
from itertools import chain
from operator import attrgetter

import pytz
import rapidjson as json
from credits.utils import (get_user_credits, pay_author_subscription,
                           pay_newspaper_subscription)
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import transaction
from django.db.models import F, Q, Sum
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound)
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now as timezone_now
from django.views import View
from django.views.decorators.http import require_POST

from users.models import User
from utils.decorators import ajax_login_required
from utils.html import convert_data_uris, sanitize
from utils.json import JsonResponse
from utils.upload import file_from_data_uri
from .models import (Backlog, Issue, Newspaper, CoEditor, Post, Subscription,
                     SubscriptionToAuthor, IssuePost, Editorial, EditorialTweet,
                     round_fair_price)
from .period import parse_periodicity
from .signals import post_publish
from .utils import create_post_link

AUTOR_POSTS_PAGE_SIZE = 20


@ajax_login_required
def subscriptions(request):
    now = datetime.now(request.user.tzinfo)
    subscribed_authors = {}
    query = SubscriptionToAuthor.objects.filter(
        Q(valid_to__gt=now) | Q(renewal=True),
        user=request.user
    ).select_related('author')

    for s in query:
        subscribed_authors.update(s.to_json())

    subscribed_newspapers = {}
    newspapers = []
    query = Subscription.objects.filter(
        Q(valid_to__gt=now) | Q(renewal=True),
        user=request.user
    ).select_related('newspaper', 'newspaper__editor')

    for s in query:
        newspapers.append(s.newspaper.to_json(request.user.tzinfo))
        subscribed_newspapers.update(s.to_json())

    return JsonResponse({
        "newspapers": newspapers,
        "subscriptions": {
            "authors": subscribed_authors,
            "newspapers": subscribed_newspapers,
        }
    })


@ajax_login_required
def user_backlog(request):
    backlog = defaultdict(dict)
    for bl in Backlog.objects.filter(newspaper__editor=request.user).select_related('newspaper'):
        full_name = "{}/{}".format(request.user.username, bl.newspaper.slug)
        backlog[str(bl.post_id)][full_name] = 'P' if bl.publish_in else 'C'

    return JsonResponse({
        "backlog": backlog
    })


@ajax_login_required
def recent_issues(request):
    count = int(request.GET.get('count', 3))
    if count < 1 or count > 10:
        return HttpResponse('Invalid count.', status=400)

    tzinfo = request.user.tzinfo
    issues = list(Issue.objects.all().order_by('-published')[:count])
    newspaper_ids = [issue.newspaper_id for issue in issues]
    newspapers = {
        newspaper.id: newspaper for newspaper in
        Newspaper.objects.filter(id__in=newspaper_ids)
    }

    resp = []
    for issue in issues:
        issue.newspaper = newspapers[issue.newspaper_id]
        resp.append(issue.to_json(posts=True, tzinfo=tzinfo))

    return JsonResponse(resp)


@ajax_login_required
def recent_posts(request):
    tzinfo = request.user.tzinfo
    posts = Post.objects.filter(draft=False, published__lt=timezone.now())\
        .exclude(kind__in=[Post.RECOMMENDATION, Post.LINK])\
        .select_related('author').order_by('-published')[:12]
    return JsonResponse([post.to_json(tzinfo=tzinfo) for post in posts])


def delete_newspaper(request, newspaper):
    if newspaper.editor_id != request.user.id:
        return HttpResponseForbidden()
    newspaper.delete()
    return HttpResponse(status=204)


class NewspaperView(View):
    def get(self, request, username, newspapeper_slug):
        tzinfo = request.user.tzinfo
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
                issue = Issue.objects.filter(newspaper=newspaper).order_by('-number').select_related('editor')[0]
            except IndexError:
                issue = None

        data = {
            'newspaper': newspaper.to_json(tzinfo, co_editors=newspaper.editor == request.user),
            'issue': None,
            'links': {}
        }

        if issue:
            data['issue'] = issue.to_json(anonymous=request.user.is_anonymous)

            try:
                prev_num = Issue.objects.filter(newspaper=newspaper, number__lt=issue.number).order_by('-number').values_list('number', flat=True)[0]
                data['links']['prev'] = '/{}/{}'.format(newspaper.full_name, prev_num)
            except IndexError:
                pass
            try:
                next_num = Issue.objects.filter(newspaper=newspaper, number__gt=issue.number).order_by('number').values_list('number', flat=True)[0]
                data['links']['next'] = '/{}/{}'.format(newspaper.full_name, next_num)
            except IndexError:
                pass

            if request.user.is_authenticated:
                if Post.objects.filter(author=request.user, kind=Post.RECOMMENDATION, ref_issue=issue).exists():
                    data['recommended'] = [data['issue']['id']]  # pylint: disable=unsubscriptable-object
                else:
                    data['recommended'] = []

        return JsonResponse(data)

    @ajax_login_required
    @transaction.atomic
    def patch(self, request, username, newspapeper_slug):
        tzinfo = request.user.tzinfo
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

        return JsonResponse({
            'newspaper': newspaper.to_json(tzinfo),
        })

    @ajax_login_required
    @transaction.atomic
    def delete(self, request, username, newspapeper_slug):
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)

        if newspaper.editor_id != request.user.id:
            return HttpResponseForbidden()

        newspaper.delete()
        return HttpResponse(status=204)


def author_detail(request, username):
    tzinfo = request.user.tzinfo
    author = get_object_or_404(User, username=username)

    newspapers = list(Newspaper.objects.filter(editor=author))
    newspapers.sort(key=attrgetter('likes'), reverse=True)
    return JsonResponse({
        'author': author.to_json(),
        'newspapers': [n.to_json(tzinfo) for n in newspapers],
    })


def author_posts(request, username):
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

    posts = [post.to_json(short=True, anonymous=request.user.is_anonymous) for post in posts_query]
    return JsonResponse({
        'posts': posts,
        'cursor': offset + AUTOR_POSTS_PAGE_SIZE if len(posts) == AUTOR_POSTS_PAGE_SIZE else None
    })


@ajax_login_required
@transaction.atomic
def newspaper_backlog(request, username, newspapeper_slug):
    newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
    if newspaper.editor_id != request.user.id:
        if request.user not in newspaper.co_editors.all():
            return HttpResponseForbidden()

    if request.method == 'GET':
        result = {'backlog': []}

        query = Backlog.objects.filter(
            newspaper=newspaper).select_related('post').order_by(F('publish_in').asc(nulls_last=True), F('ordering').asc(nulls_last=True), 'id')
        for log in query:
            result['backlog'].append({
                'post': log.post.to_json(),
                'publish': log.publish_in,
                'editorial': log.editorial.to_json() if log.editorial else None
            })

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

        return JsonResponse(result)

    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))
        upcoming_ids = payload['publish'][0]
        next_ids = payload['publish'][1]
        consider_ids = payload['consider']

        ordering = {}
        for idx, id in enumerate(chain(upcoming_ids, next_ids, consider_ids)):
            ordering[id] = idx

        issues = {id: 1 for id in upcoming_ids}
        issues.update({id: 2 for id in next_ids})
        issues.update({id: None for id in consider_ids})

        # after ordering is captured, convert lists to sets
        upcoming_ids = set(upcoming_ids)
        next_ids = set(next_ids)
        consider_ids = set(consider_ids)

        for log in Backlog.objects.filter(newspaper=newspaper).order_by(F('publish_in').asc(nulls_last=True), 'ordering'):
            idx = ordering.get(log.post_id)
            publish_in = issues.get(log.post_id)
            if idx != log.ordering or publish_in != log.publish_in:
                log.ordering = idx
                log.publish_in = publish_in
                log.save()

        return HttpResponse(status=204)

    if request.method == 'PUT':
        payload = json.loads(request.body.decode('utf-8'))
        post = get_object_or_404(Post, id=payload.get('post'))
        created = Backlog.consider_post(newspaper, post)
        return HttpResponse(status=201 if created else 204)

    if request.method == 'DELETE':
        payload = json.loads(request.body.decode('utf-8'))
        post = get_object_or_404(Post, id=payload.get('post'))
        Backlog.objects.filter(newspaper=newspaper, post=post).delete()

        if post.kind == Post.LINK:
            post.delete()

        return HttpResponse(status=204)

    return HttpResponse('405 Method Not Allowed', status=405)


@ajax_login_required
@require_POST
@transaction.atomic
def create_link(request, username, newspapeper_slug):
    newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
    if newspaper.editor_id != request.user.id:
        if request.user not in newspaper.co_editors.all():
            return HttpResponseForbidden()

    payload = json.loads(request.body.decode('utf-8'))
    url = payload['url']

    if '://' not in url:
        url = 'http://' + url

    try:
        post = create_post_link(url, request.user, hidden=True)
    except IOError as e:
        return JsonResponse({
            'error': str(e)
        }, status=409)

    created = Backlog.consider_post(newspaper, post)
    return JsonResponse({
        'post': post.to_json() if created else None
    })


class EditorialsView(View):

    @ajax_login_required
    @transaction.atomic
    def post(self, request, username, newspapeper_slug, post_id):
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
        if newspaper.editor_id != request.user.id:
            if request.user not in newspaper.co_editors.all():
                return HttpResponseForbidden()

        payload = json.loads(request.body.decode('utf-8'))
        position = payload['position']
        kind = payload['type']

        if position not in ('left', 'right'):
            return HttpResponseBadRequest("Invalid position value")

        backlog = get_object_or_404(Backlog, newspaper=newspaper, post__id=post_id)
        kind_changed = backlog.editorial and backlog.editorial.kind != kind
        editorial = backlog.editorial or Editorial(kind=kind)
        editorial.position = position
        editorial.kind = kind

        if kind == 'article':
            title = payload['title'].strip()
            content = sanitize(payload['content'].strip())

            if not title:
                return HttpResponseBadRequest("No title")

            editorial.title = title
            editorial.content = content

        elif kind == 'tweets':
            editorial.title = None
            editorial.content = None
        else:
            return HttpResponseBadRequest("Invalid editorial type")

        # keep original author even if different editor change content
        if not editorial.author_id:
            editorial.author = request.user

        editorial.save()

        if kind == 'tweets':
            ids = payload['tweets']
            valid_tweet_ids = set(Post.objects.filter(id__in=payload['tweets'], kind=Post.TWEET).values_list('id', flat=True))
            ids = [id for id in ids if id in valid_tweet_ids]
            ids_in_db = set()
            for et in EditorialTweet.objects.filter(editorial=editorial):
                ids_in_db.add(et.post_id)
                try:
                    idx = ids.index(et.post_id)
                    if et.ordering != idx:
                        et.ordering = idx
                        et.save()
                except ValueError:
                    et.delete()
                    Backlog.consider_post(newspaper, et.post_id)

            for post_id in set(ids) - ids_in_db:
                idx = ids.index(post_id)
                EditorialTweet.objects.create(editorial=editorial, post_id=post_id, ordering=idx)
                Backlog.objects.filter(newspaper=newspaper, post_id=post_id).delete()

        else:
            if kind_changed:
                EditorialTweet.objects.filter(editorial=editorial).delete()

        if not backlog.editorial:
            Backlog.objects.filter(id=backlog.id).update(editorial=editorial)

        return JsonResponse(editorial.to_json())

    @ajax_login_required
    @transaction.atomic
    def patch(self, request, username, newspapeper_slug, post_id):
        """Update editorial position"""
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
        if newspaper.editor_id != request.user.id:
            if request.user not in newspaper.co_editors.all():
                return HttpResponseForbidden()

        payload = json.loads(request.body.decode('utf-8'))
        if set(payload.keys()) != {'position'}:
            return HttpResponseBadRequest("Only position key is expected")

        position = payload['position']

        if position not in ('left', 'right'):
            return HttpResponseBadRequest("Invalid position value")

        backlog = get_object_or_404(Backlog, newspaper=newspaper, post__id=post_id)
        editorial = backlog.editorial
        editorial.position = position
        editorial.save()

        return JsonResponse(editorial.to_json())

    @ajax_login_required
    @transaction.atomic
    def delete(self, request, username, newspapeper_slug, post_id):
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
        if newspaper.editor_id != request.user.id:
            if request.user not in newspaper.co_editors.all():
                return HttpResponseForbidden()

        backlog = get_object_or_404(Backlog, newspaper=newspaper, post__id=post_id)
        if not backlog.editorial:
            return HttpResponseNotFound()

        for et in EditorialTweet.objects.filter(editorial=backlog.editorial):
            # put back tweers to backlog
            Backlog.consider_post(newspaper, et.post_id)

        backlog.editorial.delete()
        return HttpResponse(status=204)


class NewspaperSubscriptionView(View):

    @ajax_login_required
    @transaction.atomic
    def post(self, request, username, newspapeper_slug):
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

        return JsonResponse({
            'credits': str(credits),
            'subscription': subscription.to_json()
        })

    @ajax_login_required
    @transaction.atomic
    def delete(self, request, username, newspapeper_slug):
        now = datetime.now(request.user.tzinfo)
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)

        subscription = Subscription.objects.filter(
            Q(renewal=True) | Q(suspended=True),
            user=request.user, newspaper=newspaper
        ).order_by('-valid_to').first()

        if subscription is None:
            return HttpResponseNotFound()

        if newspaper.price == 0:
            subscription.delete()
            return JsonResponse({'subscription': None})

        subscription.renewal = False
        subscription.suspended = False
        subscription.save()
        return JsonResponse({
            'subscription': subscription.to_json() if subscription.valid_to > now else None
        })


class AuthorSubscriptionView(View):

    @ajax_login_required
    @transaction.atomic
    def post(self, request, username):
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

        return JsonResponse({
            'credits': str(credits),
            'subscription': subscription.to_json()
        })

    @ajax_login_required
    @transaction.atomic
    def delete(self, request, username):
        author = get_object_or_404(User, username=username)
        now = datetime.now(request.user.tzinfo)

        subscription = SubscriptionToAuthor.objects.filter(
            Q(renewal=True) | Q(suspended=True),
            user=request.user, author=author,
        ).order_by('-valid_to').first()

        if not subscription:
            return HttpResponseNotFound()

        if author.price == 0:
            subscription.delete()
            return JsonResponse({'subscription': None})

        subscription.renewal = False
        subscription.suspended = False
        subscription.save()

        return JsonResponse({
            'subscription': subscription.to_json() if subscription.valid_to > now else None
        })


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
        'content': content,
    }


class DraftsView(View):
    @ajax_login_required
    def get(self, request):
        posts = Post.objects.filter(author=request.user, draft=True).order_by('-published')
        return JsonResponse({
            'posts': [post.to_json() for post in posts]
        })

    @ajax_login_required
    def post(self, request):
        payload = json.loads(request.body.decode('utf-8'))

        try:
            attrs = validate_post_attributes(request, payload, True)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

        post = Post.objects.create(
            draft=True,
            protected=False,
            author=request.user,
            **attrs
        )

        return JsonResponse({
            'post': post.to_json()
        })


class DraftDetailView(View):

    @ajax_login_required
    def get(self, request, post_id):
        # user can get (and patch) also published posts
        post = get_object_or_404(Post, author=request.user, id=post_id)
        return JsonResponse({
            'post': post.to_json()
        })

    @ajax_login_required
    def patch(self, request, post_id):
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

        return JsonResponse({
            'post': post.to_json()
        })

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
def publish_draft(request, post_id):
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

    return JsonResponse({
        'post': post.to_json()
    })


def post(request, username, post_slug):
    post = get_object_or_404(Post, author__username=username, slug=post_slug, draft=False, published__lt=timezone.now())

    # Doesn't work, post can be part of multiple issues or just related to author
    # newspaper = Issue.objects.get(posts=post).newspaper
    # is_subscribed = Subscription.objects.filter(user=request.user, newspaper=newspaper).count() > 0
    # if not is_subscribed:
    #     return HttpResponse('402 Payment Required', status=402)

    editorials = []
    query = IssuePost.objects.filter(post=post, editorial__isnull=False) \
        .select_related('editorial', 'issue__newspaper') \
        .order_by('issue_id', 'ordering')
    for issue_post in query:
        item = issue_post.editorial.to_json()
        item['issue'] = issue_post.issue.to_json(posts=False)
        del item['position']
        editorials.append(item)

    data = {
        'post': post.to_json(anonymous=request.user.is_anonymous),
        'editorials': editorials
    }

    if request.user.is_authenticated:
        data['recommended'] = Post.objects.filter(
            author=request.user, kind=Post.RECOMMENDATION, ref_post=post).exists()

    return JsonResponse(data)


def get_type_from_data_uri(data):
    return data.split(';', maxsplit=1)[0].split('/')[1]


@ajax_login_required
@require_POST
@transaction.atomic
def start_newspaper(request, username):
    tzinfo = request.user.tzinfo
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

    return JsonResponse({
        'newspaper': newspaper.to_json(tzinfo)
    })


class PostRecommendationView(View):

    @ajax_login_required
    @transaction.atomic
    def post(self, request, username, post_slug):
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

        return JsonResponse({
            'post': recommendation.to_json()
        })

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
    def post(self, request, username, newspapeper_slug, issue_number):
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

        return JsonResponse({
            'post': recommendation.to_json()
        })

    @ajax_login_required
    @transaction.atomic
    def delete(self, request, username, newspapeper_slug, issue_number):
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
        issue = get_object_or_404(Issue, newspaper=newspaper, number=issue_number)
        recommendation = get_object_or_404(Post, author=request.user, ref_issue=issue, kind=Post.RECOMMENDATION)
        recommendation.delete()

        return JsonResponse({})
