from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import views
from django.shortcuts import render
from django.http import JsonResponse

from .models import Edition


def index(request):
    return render(request, 'index.html')


@login_required
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
