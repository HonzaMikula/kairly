import json
from collections import namedtuple

from libgravatar import Gravatar

from django.db import connection
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST


from .models import EditionIssue, Post, Edition, Subscription, SubscriptionToAuthor, Author
from .serializers import edition_issue_json, post_json, edition_json, author_json
from utils.decorators import ajax_login_required


def index(request, *args, **kwargs):
    return render(request, 'index.html')


PAGE_SIZE = 5
TIMELINE_QUERY = """
SELECT *
FROM ((
         ( SELECT published,
                  author_id,
                  GROUP_CONCAT(posts) AS posts,
                  GROUP_CONCAT(issues) AS issues,
                  NULL AS editionissue_id,
                  NULL AS edition_id
          FROM (
                  (SELECT DATE(published) AS published,
                          p.author_id AS author_id,
                          GROUP_CONCAT(p.id) AS posts,
                          NULL AS issues
                   FROM articles_post p
                   JOIN articles_subscriptiontoauthor sa ON (p.author_id = sa.author_id)
                   WHERE sa.user_id = %s AND p.draft = 0
                   GROUP BY p.author_id,
                            DATE(published))
                UNION
                  (SELECT DATE(published) AS published,
                          aei.editor_id AS author_id,
                          NULL AS posts,
                          GROUP_CONCAT(aei.id) AS issues
                   FROM articles_editionissue aei
                   JOIN articles_subscriptiontoauthor sa ON (aei.editor_id = sa.author_id)
                   WHERE sa.user_id = %s
                   GROUP BY aei.editor_id,
                            DATE(published))) AS au
          GROUP BY published, author_id )
       UNION
         ( SELECT published,
                  NULL,
                  NULL,
                  NULL,
                  ei.id,
                  ei.edition_id
          FROM articles_editionissue ei
          JOIN articles_subscription se ON (ei.edition_id = se.edition_id)
          WHERE ei.edition_id IS NOT NULL
            AND se.user_id = %s )) AS u)
ORDER BY published DESC LIMIT %s OFFSET %s
"""


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


@ajax_login_required
def timeline(request):
    try:
        offset = int(request.GET.get('cursor', 0))
    except ValueError:
        offset = 0

    user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute(TIMELINE_QUERY, [user_id, user_id, user_id, PAGE_SIZE, offset])
        results = namedtuplefetchall(cursor)

    issues = []
    for row in results:
        if row.editionissue_id:
            # TODO nice to have load all issues together
            issue = EditionIssue.objects.get(id=row.editionissue_id)
            issues.append(edition_issue_json(issue))
        else:
            author = Author.objects.get(id=row.author_id)
            if row.posts:
                posts = Post.objects.filter(id__in=map(int, row.posts.split(',')))
            else:
                posts = []
            if row.issues:
                author_issues = EditionIssue.objects \
                    .filter(id__in=row.issues.split(',')) \
                    .select_related('edition')
            else:
                author_issues = []
            issues.append({
                'id': '{}-{}'.format(author.slug, str(row.published)),
                'type': 'author',
                'title': 'New posts on {:%x}'.format(row.published),
                'period': 'Posts',
                'time': str(row.published),
                'author': author_json(author),
                'posts': [post_json(p, short=True) for p in posts],
                'issues': [edition_issue_json(i, posts=False) for i in author_issues]
            })

    return JsonResponse({
        'issues': issues,
        'cursor': offset + PAGE_SIZE if len(results) == PAGE_SIZE else None
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
    posts = Post.objects.filter(author=author, draft=False)
    return JsonResponse({
        'author': author_json(author),
        'editions': [edition_json(e) for e in annotate_editions(request, editions)],
        'posts': [post_json(post, short=True) for post in posts]
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
    subscribe = payload['subscribe']
    if subscribe:
        SubscriptionToAuthor.objects.create(user=request.user, author=author)
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
    g = Gravatar('a@b.cz')
    return JsonResponse({
        "user": {
            "name": request.user.get_full_name(),
            'picture': g.get_image(use_ssl=True, default='blank')
        }
    })
