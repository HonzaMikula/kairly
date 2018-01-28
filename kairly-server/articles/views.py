import json
from libgravatar import Gravatar

from django.db.models import Count
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST


from .models import EditionIssue, Post, Edition, Subscription
from .serializers import edition_issue_json, post_json, edition_json
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
        'last_page': issues.paginator.num_pages
    })


@ajax_login_required
def editions(request):
    editions = Edition.objects.all().select_related('editor') \
        .annotate(issues=Count('editionissue', distinct=True)) \
        .annotate(likes=Count('subscription', distinct=True))
    subscribed = set(Edition.objects
                     .filter(subscription__user=request.user)
                     .values_list('id', flat=True))

    def add_flag(edition):
        edition.is_subscribed = edition.id in subscribed
        return edition

    return JsonResponse([edition_json(add_flag(e)) for e in editions], safe=False)


@ajax_login_required
@require_POST
def subscribe(request, edition_id):
    edition = Edition.objects.get(id=edition_id)
    payload = json.loads(request.body)
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
    return JsonResponse({
        'post': post_json(get_object_or_404(Post, id=post_id))
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
