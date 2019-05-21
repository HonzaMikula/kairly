import lxml.html

import rapidjson as json

from articles.models import Post
from sources.parser.og import parse_og_tags
from utils.url import fetch_url


def create_post_link(url, user, hidden=False, published=None, guid=None):
    html, resolved_url = fetch_url(url)
    existing_post = Post.find_by_source_url(resolved_url)
    if existing_post:
        return existing_post

    htmltree = lxml.html.fromstring(html)
    try:
        title = htmltree.cssselect('head title')[0].text
    except IndexError:
        title = resolved_url
    try:
        description = htmltree.cssselect('head meta[name=description]')[0].attrib.get('content', '')
    except IndexError:
        description = ''

    og = parse_og_tags(htmltree)

    attachments = {}
    if 'image' in og:
        attachments['image'] = og['image']

    args = dict(
        kind=Post.LINK,
        source=resolved_url,
        guid=guid,
        protected=False,
        hidden=hidden,
        title=og.get('title', title),
        perex=og.get('description', description),
        attachments=json.dumps(attachments) if attachments else None,
        author=user,
        price=0,
        weight=0
    )

    if published is not None:
        args['published'] = published

    return Post.objects.create(**args)

