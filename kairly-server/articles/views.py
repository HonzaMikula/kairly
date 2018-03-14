import json
from libgravatar import Gravatar

from django.db.models import Count
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST


from .models import EditionIssue, Post, Edition, Subscription, Author
from .serializers import edition_issue_json, post_json, edition_json, author_json
from utils.decorators import ajax_login_required


def index(request, *args, **kwargs):
    return render(request, 'index.html')


@ajax_login_required
def timeline(request):
    editions = Edition.objects.filter(subscription__user=request.user)
    query = EditionIssue.objects \
        .filter(edition__in=editions) \
        .select_related('editor', 'edition')
    paginator = Paginator(query, 5)
    page = request.GET.get('page')
    issues = paginator.get_page(page)
    return JsonResponse({
        'issues': [edition_issue_json(e) for e in issues],
        'page': issues.number,
        'lastPage': issues.paginator.num_pages
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
    edition = Edition.objects.get(editor__slug=editor_slug, slug=edition_slug)
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
    author = Author.objects.get(slug=author_slug)
    editions = Edition.objects.filter(editor=author).order_by('-likes')
    return JsonResponse({
        'author': author_json(author),
        'editions': [edition_json(e) for e in annotate_editions(request, editions)],
        'posts': []
    })


@ajax_login_required
@require_POST
def subscribe(request, editor_slug, edition_slug):
    edition = Edition.objects.get(editor__slug=editor_slug, slug=edition_slug)
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
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    edition = EditionIssue.objects.get(posts=post).edition
    is_subscribed = Subscription.objects.filter(user=request.user, edition=edition).count() > 0
    if not is_subscribed:
        return HttpResponse('402 Payment Required', status=402)

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
