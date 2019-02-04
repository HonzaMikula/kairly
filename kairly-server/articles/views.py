import rapidjson as json
import html
from collections import defaultdict
from datetime import datetime
from operator import attrgetter
from decimal import Decimal

from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseForbidden, HttpResponseBadRequest)
from django.views import View
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now as timezone_now

from utils.decorators import ajax_login_required
from utils.html import sanitize, convert_data_uris
from utils.json import JsonResponse
from utils.upload import file_from_data_uri
from users.models import User
from credits.utils import get_user_credits, pay_author_subscription, pay_newspaper_subscription
from .models import (Newspaper, Issue, Backlog,
                     Post, Subscription, SubscriptionToAuthor)
from .signals import post_publish
from .period import parse_periodicity


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
        backlog[str(bl.post_id)][full_name] = 'C' if bl.publish_stamp is None else 'P'

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
        resp.append(issue.to_json(posts=True, tzinfo=tzinfo)),

    return JsonResponse(resp)


@ajax_login_required
def recent_posts(request):
    tzinfo = request.user.tzinfo
    posts = Post.objects.filter(draft=False, published__lt=timezone.now()).select_related('author').order_by('-published')[:12]
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

        issueNo = request.GET.get('issue')
        if issueNo:
            try:
                issueNo = int(issueNo)
            except ValueError:
                return HttpResponse('Invalid issue number.', status=400)
            issue = get_object_or_404(Issue, newspaper=newspaper, number=issueNo)
        else:
            try:
                issue = Issue.objects.filter(newspaper=newspaper).order_by('-number').select_related('editor')[0]
            except IndexError:
                issue = None

        links = {}
        if issue:
            try:
                prev_num = Issue.objects.filter(newspaper=newspaper, number__lt=issue.number).order_by('-number').values_list('number', flat=True)[0]
                links['prev'] = '/{}/{}'.format(newspaper.full_name, prev_num)
            except IndexError:
                pass
            try:
                next_num = Issue.objects.filter(newspaper=newspaper, number__gt=issue.number).order_by('number').values_list('number', flat=True)[0]
                links['next'] = '/{}/{}'.format(newspaper.full_name, next_num)
            except IndexError:
                pass

        return JsonResponse({
            'newspaper': newspaper.to_json(tzinfo),
            'issue': issue.to_json(anonymous=request.user.is_anonymous) if issue else None,
            'links': links
        })

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


def author(request, username):
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

    posts_query = Post.objects.filter(author=author, draft=False, published__lt=timezone.now())
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
        return HttpResponseForbidden()

    if request.method == 'GET':
        result = {'backlog': [], 'publish': []}

        query = Backlog.objects.filter(
            newspaper=newspaper, publish_stamp__isnull=True).select_related('post')
        for log in query:
            result['backlog'].append(log.post.to_json())

        query = Backlog.objects.filter(
            newspaper=newspaper, publish_stamp__isnull=False)\
            .order_by('ordering').select_related('post')
        for log in query:
            result['publish'].append(log.post.to_json())
        return JsonResponse(result)

    if request.method == 'PUT':
        payload = json.loads(request.body.decode('utf-8'))
        post = get_object_or_404(Post, id=payload.get('post'))

        if Backlog.objects.filter(newspaper=newspaper, post=post).exists():
            return HttpResponse(status=204)
        else:
            Backlog.objects.create(
                newspaper=newspaper,
                post=post
            )
            return HttpResponse(status=201)

    if request.method == 'DELETE':
        payload = json.loads(request.body.decode('utf-8'))
        post = get_object_or_404(Post, id=payload.get('post'))
        Backlog.objects.filter(newspaper=newspaper, post=post).delete()
        return HttpResponse(status=204)

    return HttpResponse('405 Method Not Allowed', status=405)


@ajax_login_required
@require_POST
@transaction.atomic
def backlog_publish(request, username, newspapeper_slug):
    newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
    if newspaper.editor_id != request.user.id:
        return HttpResponseForbidden()

    post_ids = json.loads(request.body.decode('utf-8'))
    publish_stamp = timezone.now()
    for log in Backlog.objects.filter(newspaper=newspaper):
        try:
            idx = post_ids.index(log.post_id)
            log.publish_stamp = publish_stamp
            log.ordering = idx + 1
        except ValueError:
            if log.publish_stamp is None:
                continue
            log.publish_stamp = None
            log.ordering = None
        log.save()
    return HttpResponse(status=204)


class NewspaperSubscriptionView(View):

    @ajax_login_required
    @transaction.atomic
    def post(self, request, username, newspapeper_slug):
        now = datetime.now(request.user.tzinfo)
        author = get_object_or_404(User, username=username)
        newspaper = get_object_or_404(Newspaper, editor=author, slug=newspapeper_slug)

        payload = json.loads(request.body.decode('utf-8'))
        donation = payload.get('donation')
        if donation:
            donation = Decimal(donation)
            if donation < 0:
                return HttpResponseBadRequest("Invalid donation")

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
            if credits < newspaper.price + donation:
                return HttpResponse("Insufficient credit.", status=402)

            if not subscription:
                subscription = Subscription(
                    user=request.user,
                    newspaper=newspaper
                )

            subscription.suspended = False
            subscription.valid_from = now
            subscription.valid_to = now + relativedelta(months=1)
            subscription.donation = donation
            subscription.save()

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
        author = get_object_or_404(User, username=username)
        newspaper = get_object_or_404(Newspaper, editor=author, slug=newspapeper_slug)

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

        keep_status = payload.get('keepStatus')
        donation = payload.get('donation')
        if donation:
            donation = Decimal(donation)
            if donation < 0:
                return HttpResponseBadRequest("Invalid donation")

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
            if credits < author.price + donation:
                return HttpResponse("Insufficient credit.", status=402)

            if not subscription:
                subscription = SubscriptionToAuthor(
                    user=request.user,
                    author=author
                )

            if periodicity:
                subscription.set_periodicity(periodicity)

            subscription.suspended = False
            subscription.valid_from = now
            subscription.valid_to = now + relativedelta(months=1)
            subscription.donation = donation
            subscription.save()

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
def publish_draft(request, post_id):
    post = get_object_or_404(Post, author=request.user, id=post_id, draft=True)

    if post.kind == Post.NEWSPAPER and post.perex == '':
        return HttpResponseBadRequest('Perex is empty')

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

    return JsonResponse({
        'post': post.to_json(anonymous=request.user.is_anonymous)
    })


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

    return JsonResponse({
        'newspaper': newspaper.to_json(tzinfo)
    })
