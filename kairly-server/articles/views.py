from libgravatar import Gravatar

from django.shortcuts import render
from django.http import JsonResponse

from .models import Edition
from utils.decorators import ajax_login_required


def index(request):
    return render(request, 'index.html')


@ajax_login_required
def timeline(request):
    def edition_json(edition):
        return {
            "id": edition.id,
            "title": edition.title,
            "edition": edition.edition,
            "time": str(edition.published),
            "author": {
                "name": edition.editor.name,
                "picture": edition.editor.picture,
            },
            "posts": [],
        }

    editions = Edition.objects.filter(useredition__user=request.user).select_related('editor')
    return JsonResponse({
        'editions': [edition_json(e) for e in editions]
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
