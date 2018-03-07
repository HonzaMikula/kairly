from django.conf import settings

from .models import Post


def author_json(author):
    return {
        "name": author.name,
        "picture": author.picture,
        "medium": author.medium,
        "bio": author.bio
    }


def post_json(post, short=False):
    j = {
        'id': post.id,
        "author": author_json(post.author),
        "type": post.kind,
        "time": str(post.published),
        "favorites": 131
    }
    if post.kind == Post.PICTURE:
        j['content'] = {
            'title': post.title,
            'picture': post.picture,
        }
    elif post.kind == Post.TWEET:
        j['content'] = {
            'content': post.content,
            'picture': post.picture,
        }
    elif post.kind == Post.NEWSPAPER:
        j['timeRead'] = post.read_time
        j['content'] = {
            'title': post.title,
            'content': post.perex if short else post.content,
            'perex': post.perex
        }
    return j


def edition_issue_json(issue):
    return {
        "id": issue.id,
        "title": issue.title,
        "period": issue.edition.period,
        "time": str(issue.published),
        "author": author_json(issue.editor),
        "posts": [post_json(p, short=True) for p in
                  issue.posts.all().order_by('editionissuepost__ordering', '-published')],
    }


def edition_json(edition):
    return {
        "id": "{}/{}".format(edition.editor.slug, edition.slug),
        "title": edition.title,
        "picture": settings.MEDIA_SITE + edition.image.url,
        "description": edition.description,
        "editor": author_json(edition.editor),
        "period": edition.period,
        "isSubscribed": edition.is_subscribed,
        "issues": edition.issues,
        "likes": edition.likes,
    }
