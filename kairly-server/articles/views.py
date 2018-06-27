import json
from datetime import datetime

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import (Http404, JsonResponse, HttpResponse,
                         HttpResponseForbidden, HttpResponseBadRequest)
from django.views.decorators.http import require_POST
from django.utils.text import slugify

from utils.decorators import ajax_login_required
from utils.upload import file_from_data_uri
from users.models import User
from .models import (Edition, EditionIssue, EditionBacklog,
                     Post, Subscription, SubscriptionToAuthor, Topic)
from .period import parse_periodicity


AUTOR_POSTS_PAGE_SIZE = 20


def get_user_and_topic(username):
    if '|' in username:
        username, topic_slug = username.split('|', maxsplit=1)
    else:
        topic_slug = None

    user = get_object_or_404(User, username=username)
    if topic_slug:
        topic = Topic.objects.get(slug=topic_slug)
        if not topic:
            raise Http404
    else:
        topic = None

    return user, topic


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
def user_editions(request):
    editions = Edition.objects \
        .filter(subscription__user=request.user) \
        .annotate(issues=Count('editionissue', distinct=True)) \
        .annotate(likes=Count('subscription', distinct=True))

    resp = []
    for edition in editions:
        edition.user_subscription = True
        resp.append(edition.to_json())

    return JsonResponse(resp, safe=False)


@ajax_login_required
def recent_issues(request):
    issues = list(EditionIssue.objects.all().order_by('-published')[:3])
    edition_ids = [issue.edition_id for issue in issues]
    editions = {
        edition.id: edition for edition in
        annotate_editions(request, Edition.objects.filter(id__in=edition_ids))
    }

    resp = []
    for issue in issues:
        issue.edition = editions[issue.edition_id]
        resp.append(issue.to_json(posts=False, tzinfo=request.tzinfo)),

    return JsonResponse(resp, safe=False)


@ajax_login_required
def recent_posts(request):
    posts = Post.objects.all().select_related('author').order_by('-published')[:12]
    return JsonResponse([post.to_json(tzinfo=request.tzinfo) for post in posts], safe=False)


@ajax_login_required
def user_authors(request):
    subscriptions = SubscriptionToAuthor.objects.filter(user=request.user) \
        .select_related('author').order_by('author__name')

    def map_to_author(sub):
        author = sub.author
        author.user_subscription = sub
        return author

    return JsonResponse([map_to_author(sub).to_json(topic=sub.topic) for sub in subscriptions],
                        safe=False)


def delete_edition(request, edition):
    if edition.editor_id != request.user.id:
        return HttpResponseForbidden()
    edition.delete()
    return HttpResponse(status=204)


@ajax_login_required
def edition(request, username, edition_slug):
    edition = get_object_or_404(Edition, editor__username=username, slug=edition_slug)
    if request.method == 'DELETE':
        return delete_edition(request, edition)

    try:
        edition.user_subscription = Subscription.objects.get(user=request.user, edition=edition)
    except Subscription.DoesNotExist:
        edition.user_subscription = None
    edition.issues = edition.editionissue_set.count()
    edition.likes = edition.subscription_set.count()

    issueNo = request.GET.get('issue')
    if issueNo:
        issue = get_object_or_404(EditionIssue, edition=edition, number=int(issueNo))
    else:
        try:
            issue = EditionIssue.objects.filter(edition=edition).order_by('-number').select_related('editor')[0]
        except IndexError:
            issue = None

    return JsonResponse({
        'edition': edition.to_json(),
        'issue': issue.to_json() if issue else None,
    })


@ajax_login_required
def author(request, username):
    author, topic = get_user_and_topic(username)
    topics = {t.slug: t for t in Topic.objects.filter(author=author)}

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
        'author': author.to_json(topic=topic),
        'editions': [e.to_json() for e in annotate_editions(request, editions)],
    }
    if not topic and topics:
        data['topics'] = [{
            'name': t.name,
            'url': '/author/{}|{}'.format(author.username, t.slug)
        } for t in topics.values()]
    return JsonResponse(data)


@ajax_login_required
def author_posts(request, username):
    try:
        offset = int(request.GET.get('cursor', 0))
    except ValueError:
        offset = 0

    author, topic = get_user_and_topic(username)

    posts_query = Post.objects.filter(author=author, draft=False)
    if topic:
        posts_query = posts_query.filter(topics=topic)
    posts_query = posts_query.order_by('-published')[offset:offset + AUTOR_POSTS_PAGE_SIZE]
    posts = [post.to_json(short=True) for post in posts_query]
    return JsonResponse({
        'posts': posts,
        'cursor': offset + AUTOR_POSTS_PAGE_SIZE if len(posts) == AUTOR_POSTS_PAGE_SIZE else None
    })


@ajax_login_required
def edition_backlog(request, username, edition_slug):
    edition = get_object_or_404(Edition, editor__username=username, slug=edition_slug)
    if edition.editor_id != request.user.id:
        return HttpResponseForbidden()

    if request.method == 'GET':
        result = {'backlog': [], 'publish': []}
        for log in EditionBacklog.objects.filter(edition=edition).select_related('post'):
            target = result['publish'] if log.publish_stamp else result['backlog']
            target.append(log.post.to_json())
        return JsonResponse(result)

    if request.method == 'PUT':
        payload = json.loads(request.body.decode('utf-8'))
        post = get_object_or_404(Post, id=payload.get('post'))
        publish = payload.get('publish', False)
        publish_stamp = datetime.now() if publish else None

        try:
            log = EditionBacklog.objects.get(edition=edition, post=post)
            log.publish_stamp = publish_stamp
            log.save()
        except EditionBacklog.DoesNotExist:
            EditionBacklog.objects.create(
                edition=edition,
                post=post,
                publish_stamp=publish_stamp
            )
        return HttpResponse(status=204)

    if request.method == 'DELETE':
        payload = json.loads(request.body.decode('utf-8'))
        post = get_object_or_404(Post, id=payload.get('post'))
        EditionBacklog.objects.filter(edition=edition, post=post).delete()
        return HttpResponse(status=204)

    return HttpResponse('405 Method Not Allowed', status=405)


@ajax_login_required
@require_POST
def subscribe(request, username, edition_slug):
    author, _ = get_user_and_topic(username)
    edition = get_object_or_404(Edition, editor=author, slug=edition_slug)
    Subscription.objects.create(user=request.user, edition=edition)

    edition.user_subscription = True
    edition.issues = edition.editionissue_set.count()
    edition.likes = edition.subscription_set.count()
    return JsonResponse(edition.to_json())


@ajax_login_required
@require_POST
def unsubscribe(request, username, edition_slug):
    author, _ = get_user_and_topic(username)
    edition = get_object_or_404(Edition, editor=author, slug=edition_slug)
    Subscription.objects.filter(user=request.user, edition=edition).delete()

    edition.user_subscription = False
    edition.issues = edition.editionissue_set.count()
    edition.likes = edition.subscription_set.count()
    return JsonResponse(edition.to_json())


@ajax_login_required
@require_POST
def subscribe_author(request, username):
    author, topic = get_user_and_topic(username)
    payload = json.loads(request.body.decode('utf-8'))

    try:
        periodicity = parse_periodicity(payload)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    try:
        # Handle unique together manually, because
        # mysql ignores key when one of values is NULL (usually topic)
        #
        # There is still place for race condition
        # it could be solved by adding topic slug on this table
        # (with empty string value when there is no topic) and
        # make unique together on that
        subscription = SubscriptionToAuthor.objects.get(
            user=request.user,
            author=author,
            topic=topic
        )
    except SubscriptionToAuthor.DoesNotExist:
        subscription = SubscriptionToAuthor.objects.create(
            user=request.user,
            author=author,
            topic=topic,
            period=periodicity.frequency,
            period_time=periodicity.time,
            period_dow=periodicity.dow,
        )

    author.user_subscription = subscription
    return JsonResponse(author.to_json(topic=topic))


@ajax_login_required
@require_POST
def unsubscribe_author(request, username):
    author, topic = get_user_and_topic(username)
    SubscriptionToAuthor.objects.filter(
        user=request.user, author=author, topic=topic).delete()

    author.user_subscription = None
    return JsonResponse(author.to_json(topic=topic))


@ajax_login_required
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Doesn't work, post can be part of multiple issues or just related to author
    # edition = EditionIssue.objects.get(posts=post).edition
    # is_subscribed = Subscription.objects.filter(user=request.user, edition=edition).count() > 0
    # if not is_subscribed:
    #     return HttpResponse('402 Payment Required', status=402)

    return JsonResponse({
        'post': post.to_json()
    })


def get_type_from_data_uri(data):
    return data.split(';', maxsplit=1)[0].split('/')[1]


@ajax_login_required
@require_POST
def create_edition(request, username):
    author, topic = get_user_and_topic(username)
    payload = json.loads(request.body.decode('utf-8'))
    title = payload['title']

    try:
        periodicity = parse_periodicity(payload['periodicity'])
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    base_slug = slugify(title)
    slug = base_slug
    slug_suffix = 1
    while Edition.objects.filter(editor=author, slug=slug).exists():
        slug_suffix += 1
        slug = '{}-{}'.format(base_slug, slug_suffix)

    image = file_from_data_uri(payload['image'], "{}-{}".format(author.username, base_slug))
    edition = Edition.objects.create(
        title=title,
        slug=slug,
        description=payload['description'],
        image=image,
        period=periodicity.frequency,
        period_time=periodicity.time,
        period_dow=periodicity.dow,
        editor=author
    )

    return JsonResponse({
        "edition": edition.to_json()
    })
