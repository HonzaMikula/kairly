from libgravatar import Gravatar

from django.db.models import Count
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from .models import Edition, Post, Subscription
from .serializers import edition_json, post_json, subscription_json
from utils.decorators import ajax_login_required


def index(request, *args, **kwargs):
    return render(request, 'index.html')


@ajax_login_required
def timeline(request):
    subscriptions = Subscription.objects.filter(usersubscription__user=request.user)
    query = Edition.objects.filter(subscription__in=subscriptions).select_related('editor')
    paginator = Paginator(query, 5)
    page = request.GET.get('page')
    editions = paginator.get_page(page)
    return JsonResponse({
        'editions': [edition_json(e) for e in editions],
        'page': editions.number,
        'last_page': editions.paginator.num_pages
    })


@ajax_login_required
def subscription(request):
    subscriptions = Subscription.objects.all().select_related('editor') \
        .annotate(issues=Count('edition', distinct=True)) \
        .annotate(likes=Count('usersubscription', distinct=True))
    subscribed = set(Subscription.objects
                     .filter(usersubscription__user=request.user)
                     .values_list('id', flat=True))

    def add_flag(subscription):
        subscription.is_subscribed = subscription.id in subscribed
        return subscription

    return JsonResponse([subscription_json(add_flag(s)) for s in subscriptions], safe=False)


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
