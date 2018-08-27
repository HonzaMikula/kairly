import json
from datetime import datetime
from collections import defaultdict

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
from .models import (Newspaper, Issue, Backlog,
                     Post, Subscription, SubscriptionToAuthor, Topic)
from .period import parse_periodicity, periodicity_to_json


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


def annotate_newspapers(request, newspapers):
    yield from newspapers \
        .annotate(issues=Count('issue', distinct=True)) \
        .annotate(likes=Count('subscription', distinct=True))


@ajax_login_required
def subscriptions(request):
    subscribed_authors = {}
    query = SubscriptionToAuthor.objects.filter(user=request.user).select_related('author', 'topic')
    for s in query:
        author_json = s.author.to_json(topic=s.topic)
        subscribed_authors[author_json['id']] = {
            'author': author_json,
            'periodicity': periodicity_to_json(s)
        }

    subscribed_newspapers = {}
    query = Newspaper.objects.filter(subscription__user=request.user).select_related('editor')
    for newspaper in query:
        full_name = "{}/{}".format(newspaper.editor.username, newspaper.slug)
        subscribed_newspapers[full_name] = True

    return JsonResponse({
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
        backlog[bl.post_id][full_name] = 'C' if bl.publish_stamp is None else 'P'

    return JsonResponse({
        "backlog": backlog
    })


# @ajax_login_required # TODO REVIEW PUBLIC
def recent_issues(request):
    issues = list(Issue.objects.all().order_by('-published')[:3])
    newspaper_ids = [issue.newspaper_id for issue in issues]
    newspapers = {
        newspaper.id: newspaper for newspaper in
        annotate_newspapers(request, Newspaper.objects.filter(id__in=newspaper_ids))
    }

    resp = []
    for issue in issues:
        issue.newspaper = newspapers[issue.newspaper_id]
        resp.append(issue.to_json(posts=True, tzinfo=request.tzinfo)),

    return JsonResponse(resp, safe=False)


# @ajax_login_required # TODO REVIEW PUBLIC
def recent_posts(request):
    posts = Post.objects.filter(draft=False, published__lt=datetime.now()).select_related('author').order_by('-published')[:12]
    return JsonResponse([post.to_json(tzinfo=request.tzinfo) for post in posts], safe=False)


def delete_newspaper(request, newspaper):
    if newspaper.editor_id != request.user.id:
        return HttpResponseForbidden()
    newspaper.delete()
    return HttpResponse(status=204)


class NewspaperView(View):
    # @ajax_login_required # TODO REVIEW PUBLIC
    def get(self, request, username, newspapeper_slug):
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)

        newspaper.issues = newspaper.issue_set.count()
        newspaper.likes = newspaper.subscription_set.count()

        issueNo = request.GET.get('issue')
        if issueNo:
            issue = get_object_or_404(Issue, newspaper=newspaper, number=int(issueNo))
        else:
            try:
                issue = Issue.objects.filter(newspaper=newspaper).order_by('-number').select_related('editor')[0]
            except IndexError:
                issue = None

        return JsonResponse({
            'newspaper': newspaper.to_json(),
            'issue': issue.to_json() if issue else None,
        })

    @ajax_login_required
    def patch(self, request, username, newspapeper_slug):
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

        if 'image' in payload:
            image = file_from_data_uri(payload['image'], "{}-{}".format(request.user.username, newspaper.slug))
            newspaper.image = image

        newspaper.save()

        return JsonResponse({
            'newspaper': newspaper.to_json(),
        })

    @ajax_login_required
    def delete(self, request, username, newspapeper_slug):
        newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)

        if newspaper.editor_id != request.user.id:
            return HttpResponseForbidden()

        newspaper.delete()
        return HttpResponse(status=204)


@ajax_login_required
def author(request, username):
    author, topic = get_user_and_topic(username)
    topics = {t.slug: t for t in Topic.objects.filter(author=author)}

    newspapers = Newspaper.objects.filter(editor=author).order_by('-likes')
    data = {
        'author': author.to_json(topic=topic),
        'newspapers': [e.to_json() for e in annotate_newspapers(request, newspapers)],
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
def backlog_publish(request, username, newspapeper_slug):
    newspaper = get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)
    if newspaper.editor_id != request.user.id:
        return HttpResponseForbidden()

    post_ids = json.loads(request.body.decode('utf-8'))
    publish_stamp = datetime.now()
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


@ajax_login_required
@require_POST
def subscribe(request, username, newspapeper_slug):
    author, _ = get_user_and_topic(username)
    newspaper = get_object_or_404(Newspaper, editor=author, slug=newspapeper_slug)
    Subscription.objects.create(user=request.user, newspaper=newspaper)

    # TODO return user subscription instead
    newspaper.issues = newspaper.issue_set.count()
    newspaper.likes = newspaper.subscription_set.count()
    return JsonResponse(newspaper.to_json())


@ajax_login_required
@require_POST
def unsubscribe(request, username, newspapeper_slug):
    author, _ = get_user_and_topic(username)
    newspaper = get_object_or_404(Newspaper, editor=author, slug=newspapeper_slug)
    Subscription.objects.filter(user=request.user, newspaper=newspaper).delete()

    # TODO return user subscription instead
    newspaper.issues = newspaper.issue_set.count()
    newspaper.likes = newspaper.subscription_set.count()
    return JsonResponse(newspaper.to_json())


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


def post(request, post_id):
    post = get_object_or_404(Post, id=post_id, draft=False, published__lt=datetime.now())
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
def start_newspaper(request, username):
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
    while Newspaper.objects.filter(editor=author, slug=slug).exists():
        slug_suffix += 1
        slug = '{}-{}'.format(base_slug, slug_suffix)

    image = file_from_data_uri(payload['image'], "{}-{}".format(author.username, base_slug))
    newspaper = Newspaper.objects.create(
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
        'newspaper': newspaper.to_json()
    })
