import json
from datetime import datetime

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import (Http404, JsonResponse, HttpResponse,
                         HttpResponseForbidden, HttpResponseBadRequest)
from django.views import View
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
        topic = Topic.objects.get(author=user, slug=topic_slug)
        if not topic:
            raise Http404
    else:
        topic = None

    return user, topic


def annotate_editions(request, editions):
    yield from editions \
        .annotate(issues=Count('editionissue', distinct=True)) \
        .annotate(likes=Count('subscription', distinct=True))


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
        resp.append(issue.to_json(posts=True, tzinfo=request.tzinfo)),

    return JsonResponse(resp, safe=False)


@ajax_login_required
def recent_posts(request):
    posts = Post.objects.filter(draft=False, published__lt=datetime.now()).select_related('author').order_by('-published')[:12]
    return JsonResponse([post.to_json(tzinfo=request.tzinfo) for post in posts], safe=False)


def delete_edition(request, edition):
    if edition.editor_id != request.user.id:
        return HttpResponseForbidden()
    edition.delete()
    return HttpResponse(status=204)


class EditionView(View):
    @ajax_login_required
    def get(self, request, username, edition_slug):
        edition = get_object_or_404(Edition, editor__username=username, slug=edition_slug)

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
    def patch(self, request, username, edition_slug):
        edition = get_object_or_404(Edition, editor__username=username, slug=edition_slug)
        payload = json.loads(request.body.decode('utf-8'))

        if edition.editor_id != request.user.id:
            return HttpResponseForbidden()

        if 'title' in payload:
            edition.title = payload['title'].strip()

        if 'description' in payload:
            edition.title = payload['description'].strip()

        if 'periodicity' in payload:
            try:
                periodicity = parse_periodicity(payload['periodicity'])
            except ValueError as e:
                return HttpResponseBadRequest(str(e))
            edition.period = periodicity.frequency
            edition.period_time = periodicity.time
            edition.period_dow = periodicity.dow

        if 'image' in payload:
            image = file_from_data_uri(payload['image'], "{}-{}".format(request.user.username, edition.slug))
            edition.image = image

        edition.save()

        return JsonResponse({
            'edition': edition.to_json(),
        })

    @ajax_login_required
    def delete(self, request, username, edition_slug):
        edition = get_object_or_404(Edition, editor__username=username, slug=edition_slug)

        if edition.editor_id != request.user.id:
            return HttpResponseForbidden()

        edition.delete()
        return HttpResponse(status=204)


@ajax_login_required
def author(request, username):
    author, topic = get_user_and_topic(username)
    topics = {t.slug: t for t in Topic.objects.filter(author=author)}

    editions = Edition.objects.filter(editor=author).order_by('-likes')
    data = {
        'author': author.to_json(topic=topic),
        'editions': [e.to_json() for e in annotate_editions(request, editions)],
    }
    if not topic and topics:
        data['topics'] = [{
            'name': t.name,
            'url': '{}|{}'.format(author.username, t.slug)
        } for t in topics.values()]
    return JsonResponse(data)


@ajax_login_required
def author_posts(request, username):
    try:
        offset = int(request.GET.get('cursor', 0))
    except ValueError:
        offset = 0

    author, topic = get_user_and_topic(username)

    posts_query = Post.objects.filter(author=author, draft=False, published__lt=datetime.now())
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

        query = EditionBacklog.objects.filter(
            edition=edition, publish_stamp__isnull=True).select_related('post')
        for log in query:
            result['backlog'].append(log.post.to_json())

        query = EditionBacklog.objects.filter(
            edition=edition, publish_stamp__isnull=False)\
            .order_by('ordering').select_related('post')
        for log in query:
            result['publish'].append(log.post.to_json())
        return JsonResponse(result)

    if request.method == 'PUT':
        payload = json.loads(request.body.decode('utf-8'))
        post = get_object_or_404(Post, id=payload.get('post'))

        if EditionBacklog.objects.filter(edition=edition, post=post).exists():
            return HttpResponse(status=204)
        else:
            EditionBacklog.objects.create(
                edition=edition,
                post=post
            )
            return HttpResponse(status=201)

    if request.method == 'DELETE':
        payload = json.loads(request.body.decode('utf-8'))
        post = get_object_or_404(Post, id=payload.get('post'))
        EditionBacklog.objects.filter(edition=edition, post=post).delete()
        return HttpResponse(status=204)

    return HttpResponse('405 Method Not Allowed', status=405)


@ajax_login_required
@require_POST
def edition_backlog_publish(request, username, edition_slug):
    edition = get_object_or_404(Edition, editor__username=username, slug=edition_slug)
    if edition.editor_id != request.user.id:
        return HttpResponseForbidden()

    post_ids = json.loads(request.body.decode('utf-8'))
    publish_stamp = datetime.now()
    for log in EditionBacklog.objects.filter(edition=edition):
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


@ajax_login_required
@require_POST
def subscribe(request, username, edition_slug):
    author, _ = get_user_and_topic(username)
    edition = get_object_or_404(Edition, editor=author, slug=edition_slug)
    Subscription.objects.create(user=request.user, edition=edition)

    # TODO return user subscription instead
    edition.issues = edition.editionissue_set.count()
    edition.likes = edition.subscription_set.count()
    return JsonResponse(edition.to_json())


@ajax_login_required
@require_POST
def unsubscribe(request, username, edition_slug):
    author, _ = get_user_and_topic(username)
    edition = get_object_or_404(Edition, editor=author, slug=edition_slug)
    Subscription.objects.filter(user=request.user, edition=edition).delete()

    # TODO return user subscription instead
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
        subscription.period = periodicity.frequency
        subscription.period_time = periodicity.time
        subscription.period_dow = periodicity.dow
        subscription.save()
    except SubscriptionToAuthor.DoesNotExist:
        SubscriptionToAuthor.objects.create(
            user=request.user,
            author=author,
            topic=topic,
            period=periodicity.frequency,
            period_time=periodicity.time,
            period_dow=periodicity.dow,
        )

    # TODO return user subscription instead
    return JsonResponse(author.to_json(topic=topic))


@ajax_login_required
@require_POST
def unsubscribe_author(request, username):
    author, topic = get_user_and_topic(username)
    SubscriptionToAuthor.objects.filter(
        user=request.user, author=author, topic=topic).delete()

    # TODO return user subscription instead
    return JsonResponse(author.to_json(topic=topic))


@ajax_login_required
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id, draft=False, published__lt=datetime.now())

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
    while Edition.objects.filter(editor=author, slug=slug).exists():
        slug_suffix += 1
        slug = '{}-{}'.format(base_slug, slug_suffix)

    image = file_from_data_uri(payload['image'], "{}-{}".format(author.username, base_slug))
    edition = Edition.objects.create(
        title=title,
        slug=slug,
        description=description,
        image=image,
        period=periodicity.frequency,
        period_time=periodicity.time,
        period_dow=periodicity.dow,
        editor=author
    )

    return JsonResponse({
        "edition": edition.to_json()
    })
