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


def edition_json(edition):
    return {
        "id": edition.id,
        "title": edition.title,
        "edition": edition.edition,
        "time": str(edition.published),
        "author": author_json(edition.editor),
        "posts": [post_json(p, short=True) for p in
                  edition.posts.all().order_by('editionpost__ordering', '-published')],
    }
