from libgravatar import Gravatar

from django.shortcuts import render
from django.http import JsonResponse

from .models import Edition, Post
from utils.decorators import ajax_login_required


def index(request):
    return render(request, 'index.html')


@ajax_login_required
def timeline(request):
    def author_json(author):
        return {
            "name": author.name,
            "picture": author.picture,
            "medium": author.medium,
            "bio": author.bio
        }

    def post_json(post):
        j = {
            'id': post.id,
            "author": author_json(post.author),
            "type": post.kind,
            "testType": "post-" + post.kind,
            "postType": 'article' if post.kind == Post.NEWSPAPER else post.kind,
            "time": str(post.published),
            "favorites": 131
        }
        if post.kind == Post.PICTURE:
            j['content'] = {
                'title': post.title,
                'picture': post.picture,
            }
        elif post.kind == Post.TWEET:
            j['content'] = post.content
        elif post.kind == Post.NEWSPAPER:
            j['timeRead'] = post.read_time
            j['content'] = {
                'title': post.title,
                'content': post.perex,
            }
        return j

    def edition_json(edition):
        return {
            "id": edition.id,
            "title": edition.title,
            "edition": edition.edition,
            "time": str(edition.published),
            "author": author_json(edition.editor),
            "posts": [post_json(p) for p in edition.posts.all().order_by('-published')],
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
