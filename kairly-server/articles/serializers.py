from datetime import timezone

from django.conf import settings

from .models import Post


def author_json(author):
    res = {
        "name": author.name,
        "picture": author.picture,
        "medium": author.medium,
        "bio": author.bio,
        "url": '/author/{}'.format(author.slug),
        "followUrl": '/api/subscribe/{}'.format(author.slug),
        "unfollowUrl": '/api/unsubscribe/{}'.format(author.slug),
    }
    if hasattr(author, 'user_subscription'):
        sub = author.user_subscription
        if sub:
            res['subscription'] = {
                'period': sub.period,
                'dow': sub.period_dow,
                'time': sub.period_time,
            }
        else:
            res['subscription'] = None
    return res


def post_json(post, short=False, tzinfo=timezone.utc):
    j = {
        'id': post.id,
        "author": author_json(post.author),
        "type": post.kind,
        "time": str(post.published.astimezone(tzinfo)),
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


def edition_issue_json(issue, posts=True, edition=None, tzinfo=timezone.utc):
    if edition is None:
        edition = issue.edition
    result = {
        "id": issue.id,
        "type": 'edition',
        "title": issue.title,
        "edition": {
            "id": "{}/{}".format(edition.editor.slug, edition.slug),
            "period": edition.period,
            "picture": settings.MEDIA_SITE + edition.image.url,
            "description": edition.description,
        },
        "time": str(issue.published.astimezone(tzinfo)),
        "author": author_json(issue.editor),
    }
    if posts:
        result["posts"] = [
            post_json(p, short=True, tzinfo=tzinfo) for p in
            issue.posts.all().order_by('editionissuepost__ordering', '-published')
        ]
    return result


def edition_json(edition):
    return {
        "id": "{}/{}".format(edition.editor.slug, edition.slug),
        "title": edition.title,
        "picture": settings.MEDIA_SITE + edition.image.url,
        "description": edition.description,
        "editor": author_json(edition.editor),
        "period": edition.period,
        "subscription": edition.user_subscription is not None,
        "issues": edition.issues,
        "likes": edition.likes,
    }
