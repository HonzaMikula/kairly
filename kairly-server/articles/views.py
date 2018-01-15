from libgravatar import Gravatar

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from .models import Edition, Post, UserTags
from .serializers import edition_json, post_json
from utils.decorators import ajax_login_required


def index(request, *args, **kwargs):
    return render(request, 'index.html')


@ajax_login_required
def timeline(request):
    tags = UserTags.objects.get(user=request.user).tags.all() \
        .order_by('ordering', '-published')
    editions = Edition.objects.filter(tags__in=tags).select_related('editor')
    return JsonResponse({
        'editions': [edition_json(e) for e in editions]
    })


@ajax_login_required
def post(request, post_id):
    return JsonResponse({
        'post': post_json(get_object_or_404(Post, id=post_id))
    })


@ajax_login_required
def profile(request):
    g = Gravatar(request.user.email)
    return JsonResponse({
        "user": {
            "name": request.user.get_full_name(),
            'picture': g.get_image(use_ssl=True)
            # "picture": "https://pbs.twimg.com/profile_images/522497269447147520/uGF7lbPY.jpeg"
        }
    })
