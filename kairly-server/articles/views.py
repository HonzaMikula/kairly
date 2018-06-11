import json
from datetime import time

from libgravatar import Gravatar

from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_POST


from .models import (Author, Edition, EditionIssue, Post, Subscription, SubscriptionToAuthor, Topic)
from .serializers import edition_issue_json, post_json, edition_json, author_json
from utils.decorators import ajax_login_required


AUTOR_POSTS_PAGE_SIZE = 20


def index(request, *args, **kwargs):
    if request.path.startswith('/api') or request.path == '/favicon.ico':
        return HttpResponseNotFound()
    accept = request.META.get('HTTP_ACCEPT')
    if accept and 'text/html' not in accept:
        return HttpResponseBadRequest()

    return render(request, 'index.html')


def annotate_editions(request, editions):
    editions = editions \
        .annotate(issues=Count('editionissue', distinct=True)) \
        .annotate(likes=Count('subscription', distinct=True))

    subscribed = set(Edition.objects
                     .filter(subscription__user=request.user)
                     .values_list('id', flat=True))

    def annotate(edition):
        # HACK passing boolean instead full Subscription object
        # currenly value is only tested to not null
        edition.user_subscription = edition.id in subscribed
        return edition

    for edition in editions:
        yield annotate(edition)


@ajax_login_required
def editions(request):
    editions = Edition.objects.all().select_related('editor').order_by('-likes')

    return JsonResponse([edition_json(e) for e in annotate_editions(request, editions)],
                        safe=False)


@ajax_login_required
def authors(request):
    subscriptions = SubscriptionToAuthor.objects.filter(user=request.user) \
        .select_related('author').order_by('author__name')

    def map_to_author(sub):
        author = sub.author
        author.user_subscription = sub
        return author

    return JsonResponse([author_json(map_to_author(sub)) for sub in subscriptions],
                        safe=False)


@ajax_login_required
def edition(request, editor_slug, edition_slug):
    edition = get_object_or_404(Edition, editor__slug=editor_slug, slug=edition_slug)
    try:
        edition.user_subscription = Subscription.objects.get(user=request.user, edition=edition)
    except Subscription.DoesNotExist:
        edition.user_subscription = None
    edition.issues = edition.editionissue_set.count()
    edition.likes = edition.subscription_set.count()

    issueId = request.GET.get('issue')
    if issueId:
        issue = get_object_or_404(EditionIssue, edition=edition, id=int(issueId))
    else:
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
    topics = {t.slug: t for t in Topic.objects.filter(author=author)}
    topic_slug = request.GET.get('topic')
    if topic_slug:
        topic = topics.get(topic_slug)
        if not topic:
            return HttpResponseNotFound()
    else:
        topic = None

    try:
        if topic:
            author.user_subscription = SubscriptionToAuthor.objects.get(
                user=request.user, author=author, topic=topic)
        else:
            author.user_subscription = SubscriptionToAuthor.objects.get(
                user=request.user, author=author, topic__isnull=True)
    except SubscriptionToAuthor.DoesNotExist:
        author.user_subscription = None

    editions = Edition.objects.filter(editor=author).order_by('-likes')
    data = {
        'author': author_json(author, topic),
        'editions': [edition_json(e) for e in annotate_editions(request, editions)],
    }
    if not topic and topics:
        data['topics'] = [{
            'name': t.name,
            'url': '/author/{}/{}'.format(author_slug, t.slug)
        } for t in topics.values()]
    return JsonResponse(data)


@ajax_login_required
def author_posts(request, author_slug):
    try:
        offset = int(request.GET.get('cursor', 0))
    except ValueError:
        offset = 0

    topic_slug = request.GET.get('topic')

    author = get_object_or_404(Author, slug=author_slug)

    posts_query = Post.objects.filter(author=author, draft=False)
    if topic_slug:
        topic = get_object_or_404(Topic, slug=topic_slug, author=author)
        posts_query = posts_query.filter(topics=topic)
    posts_query = posts_query.order_by('-published')[offset:offset + AUTOR_POSTS_PAGE_SIZE]
    posts = [post_json(post, short=True) for post in posts_query]
    return JsonResponse({
        'posts': posts,
        'cursor': offset + AUTOR_POSTS_PAGE_SIZE if len(posts) == AUTOR_POSTS_PAGE_SIZE else None
    })


@ajax_login_required
@require_POST
def subscribe(request, editor_slug, edition_slug):
    edition = get_object_or_404(Edition, editor__slug=editor_slug, slug=edition_slug)
    Subscription.objects.create(user=request.user, edition=edition)

    edition.user_subscription = True
    edition.issues = edition.editionissue_set.count()
    edition.likes = edition.subscription_set.count()
    return JsonResponse(edition_json(edition))


@ajax_login_required
@require_POST
def unsubscribe(request, editor_slug, edition_slug):
    edition = get_object_or_404(Edition, editor__slug=editor_slug, slug=edition_slug)
    Subscription.objects.filter(user=request.user, edition=edition).delete()

    edition.user_subscription = False
    edition.issues = edition.editionissue_set.count()
    edition.likes = edition.subscription_set.count()
    return JsonResponse(edition_json(edition))


@ajax_login_required
@require_POST
def subscribe_author(request, editor_slug):
    author = get_object_or_404(Author, slug=editor_slug)
    topic_slug = request.GET.get('topic')
    if topic_slug:
        topic = Topic.objects.get(slug=topic_slug)
        if not topic:
            return HttpResponseNotFound()
    else:
        topic = None
    payload = json.loads(request.body.decode('utf-8'))

    period = payload.get('period')
    if period not in (SubscriptionToAuthor.X3_PER_DAY, SubscriptionToAuthor.DAILY, SubscriptionToAuthor.WEEKLY):
        return HttpResponseBadRequest('Invalid period')

    if period == SubscriptionToAuthor.X3_PER_DAY:
        period_time = None
        period_dow = None
    else:
        period_time = payload.get('time')
        if period_time not in ('6:00', '9:00', '12:00', '15:00', '18:00', '21:00'):
            return HttpResponseBadRequest('Invalid time format')
        period_time = time(*map(int, period_time.split(':', maxsplit=1)))

        if period == SubscriptionToAuthor.WEEKLY:
            period_dow = int(payload.get('dow'))
            if period_dow < 1 or period_dow > 7:
                return HttpResponseBadRequest('Invalid day of week')
        else:
            period_dow = None

    subscription = SubscriptionToAuthor.objects.create(
        user=request.user, author=author, topic=topic,
        period=period, period_time=period_time, period_dow=period_dow
    )

    author.user_subscription = subscription
    return JsonResponse(author_json(author, topic))


@ajax_login_required
@require_POST
def unsubscribe_author(request, editor_slug):
    author = get_object_or_404(Author, slug=editor_slug)
    topic_slug = request.GET.get('topic')
    if topic_slug:
        topic = Topic.objects.get(slug=topic_slug)
        if not topic:
            return HttpResponseNotFound()
    else:
        topic = None
    SubscriptionToAuthor.objects.filter(
        user=request.user, author=author, topic=topic).delete()

    author.user_subscription = None
    return JsonResponse(author_json(author, topic))


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
    authors = Author.objects.filter(users=request.user).values_list('slug', flat=True)
    return JsonResponse({
        "user": {
            "name": request.user.get_full_name(),
            'picture': g.get_image(use_ssl=True, default='blank')
        },
        "authors": list(authors)
    })
