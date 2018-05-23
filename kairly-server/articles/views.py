import json
from datetime import datetime, timedelta, timezone, time

from libgravatar import Gravatar
from dateutil.parser import parse

from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST


from .models import EditionIssue, Post, Edition, Subscription, SubscriptionToAuthor, Author
from .serializers import edition_issue_json, post_json, edition_json, author_json
from utils.decorators import ajax_login_required


def index(request, *args, **kwargs):
    return render(request, 'index.html')


AUTOR_POSTS_PAGE_SIZE = 20
TIMELINE_PAGE_SIZE = 5


def get_timeline_issues(user, end, tz):
    editions = {e.id: e for e in Edition.objects.filter(subscription__user=user)}
    author_subscriptions = {s.id: s for s in SubscriptionToAuthor.objects.filter(user=user)}
    author_ids = [asub.author_id for asub in author_subscriptions.values()]
    authors = {a.id: a for a in Author.objects.filter(id__in=author_ids)}

    edition_issues = EditionIssue.objects.filter(published__lt=end, edition_id__in=editions.keys())[:TIMELINE_PAGE_SIZE]

    def get_interval(author_subscription, dt):
        sub_time = author_subscription.time
        start = dt.replace(hour=sub_time.hour, minute=sub_time.minute, second=0, microsecond=0)
        if start > dt:
            start -= timedelta(days=1)
        return start, start + timedelta(days=1)

    def get_author_issues(begin, end):
        author_issues = []

        for asub in author_subscriptions.values():
            author = authors[asub.author_id]

            abegin = get_interval(asub, begin)[0]
            aend = get_interval(asub, end)[1]

            if aend < end:
                continue

            posts = Post.objects.filter(
                author_id=author.id,
                published__gte=abegin,
                published__lt=aend
            ).order_by('-published').values('id', 'published')

            bucket_begin = None
            post_ids = None

            def flush():
                if post_ids:
                    author_issues.append({
                        'time': bucket_begin,
                        'author': author,
                        'posts': post_ids
                    })

            for post in posts:
                b = get_interval(asub, post['published'].astimezone(tz))[0]
                if bucket_begin != b:
                    flush()
                    post_ids = []
                    bucket_begin = b
                post_ids.append(post['id'])
            flush()

        author_issues.sort(key=lambda x: x['time'], reverse=True)
        return author_issues

    def serialize_author_issues(begin, endm):
        for issue in get_author_issues(begin, end):
            author = issue['author']
            published = issue['time']
            posts = Post.objects.filter(id__in=issue['posts'])
            yield {
                'id': '{}-{}'.format(author.slug, str(published)),
                'type': 'author',
                'title': 'New posts on {:%x}'.format(published),
                'time': str(published),
                'author': author_json(author),
                'posts': [post_json(p, short=True, tzinfo=tz) for p in posts],
            }

    iend = end
    for ei in edition_issues:
        ibegin = ei.published.astimezone(tz)
        yield from serialize_author_issues(ibegin, iend)
        yield edition_issue_json(ei, edition=editions[ei.edition_id], tzinfo=tz)
        iend = ibegin
    yield from serialize_author_issues(datetime(2017, 1, 1, tzinfo=tz), iend)


@ajax_login_required
def timeline(request):
    # Group author issues by period defined by client local zone
    # It means that timeline for same user may differ when user is in different
    # timezone
    timezone_offset = int(request.META.get('HTTP_X_TIMEZONE', 0))
    tz = timezone(timedelta(minutes=-timezone_offset))

    try:
        ts = int(request.GET.get('cursor'))
        end = datetime.fromtimestamp(ts, tz)
    except (ValueError, TypeError):
        end = datetime.now(tz)

    issues = []
    stop_on_next = None
    for issue in get_timeline_issues(request.user, end, tz):
        if stop_on_next and issue['time'] != stop_on_next:
            break
        issues.append(issue)
        if len(issues) >= TIMELINE_PAGE_SIZE:
            # include all other issues with same published time
            # this is requeire to make cursor working
            stop_on_next = issue['time']

    return JsonResponse({
        'issues': issues,
        'cursor': parse(stop_on_next).timestamp() if stop_on_next else None  # TODO avoid parsing
    })


def annotate_editions(request, editions):
    editions = editions \
        .annotate(issues=Count('editionissue', distinct=True)) \
        .annotate(likes=Count('subscription', distinct=True))

    subscribed = set(Edition.objects
                     .filter(subscription__user=request.user)
                     .values_list('id', flat=True))

    def annotate(edition):
        edition.is_subscribed = edition.id in subscribed
        return edition

    for edition in editions:
        yield annotate(edition)


@ajax_login_required
def editions(request):
    editions = Edition.objects.all().select_related('editor').order_by('-likes')

    return JsonResponse([edition_json(e) for e in annotate_editions(request, editions)],
                        safe=False)


@ajax_login_required
def edition(request, editor_slug, edition_slug):
    edition = get_object_or_404(Edition, editor__slug=editor_slug, slug=edition_slug)
    edition.is_subscribed = Subscription.objects.filter(user=request.user, edition=edition).count() > 0
    edition.issues = edition.editionissue_set.count()
    edition.likes = edition.subscription_set.count()

    try:
        issue = EditionIssue.objects.filter(edition=edition).select_related('editor')[0]
    except IndexError:
        issue = None

    return JsonResponse({
        'edition': edition_json(edition),
        'issue': edition_issue_json(issue) if issue else None,
    })

    return JsonResponse(edition_json(edition))


@ajax_login_required
def author(request, author_slug):
    author = get_object_or_404(Author, slug=author_slug)
    author.is_subscribed = SubscriptionToAuthor.objects.filter(user=request.user, author=author).count() > 0
    editions = Edition.objects.filter(editor=author).order_by('-likes')
    return JsonResponse({
        'author': author_json(author),
        'editions': [edition_json(e) for e in annotate_editions(request, editions)],
    })


@ajax_login_required
def author_posts(request, author_slug):
    try:
        offset = int(request.GET.get('cursor', 0))
    except ValueError:
        offset = 0

    author = get_object_or_404(Author, slug=author_slug)
    posts_query = Post.objects.filter(author=author, draft=False) \
        .order_by('-published')[offset:offset + AUTOR_POSTS_PAGE_SIZE]
    posts = [post_json(post, short=True) for post in posts_query]
    return JsonResponse({
        'posts': posts,
        'cursor': offset + AUTOR_POSTS_PAGE_SIZE if len(posts) == AUTOR_POSTS_PAGE_SIZE else None
    })


@ajax_login_required
@require_POST
def subscribe(request, editor_slug, edition_slug):
    edition = get_object_or_404(Edition, editor__slug=editor_slug, slug=edition_slug)
    payload = json.loads(request.body.decode('utf-8'))
    subscribe = payload['subscribe']
    if subscribe:
        Subscription.objects.create(user=request.user, edition=edition)
    else:
        Subscription.objects.filter(user=request.user, edition=edition).delete()

    edition.is_subscribed = subscribe
    edition.issues = edition.editionissue_set.count()
    edition.likes = edition.subscription_set.count()
    return JsonResponse(edition_json(edition))


@ajax_login_required
@require_POST
def subscribe_author(request, editor_slug):
    author = get_object_or_404(Author, slug=editor_slug)
    payload = json.loads(request.body.decode('utf-8'))
    subscribe = payload.get('subscribe')
    if subscribe is None:
        return HttpResponseBadRequest('Subscribe field is missing')

    if subscribe:
        time = payload.get('time')
        if time not in ('6:00', '9:00', '12:00', '15:00', '18:00', '21:00'):
            return HttpResponseBadRequest('Invalid time format')
        time = time(*map(int, time.split(':', maxsplit=1)))
        SubscriptionToAuthor.objects.create(user=request.user, author=author, time=time)
    else:
        SubscriptionToAuthor.objects.filter(user=request.user, author=author).delete()
    author.is_subscribed = subscribe
    return JsonResponse(author_json(author))


@ajax_login_required
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Doesn't work, post can be part of multiple issues or just related to author
    # edition = EditionIssue.objects.get(posts=post).edition
    # is_subscribed = Subscription.objects.filter(user=request.user, edition=edition).count() > 0
    # if not is_subscribed:
    #     return HttpResponse('402 Payment Required', status=402)

    return JsonResponse({
        'post': post_json(post)
    })


@ajax_login_required
def profile(request):
    g = Gravatar(request.user.email)
    return JsonResponse({
        "user": {
            "name": request.user.get_full_name(),
            'picture': g.get_image(use_ssl=True, default='blank')
        }
    })
