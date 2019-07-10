import re
import lxml.html

import rapidjson as json

from articles.models import Post
from sources.parser.og import parse_og_tags
from sources.twitter_api import get_api_connection, status_to_post_args
from utils.url import fetch_url

RE_TWITTER_URL = re.compile(r'https://twitter\.com/[^/]+/status/(\d+)')


def create_post_link(url, user, hidden=False, published=None, guid=None):
    html, resolved_url = fetch_url(url)
    existing_post = Post.find_by_source_url(resolved_url)
    if existing_post:
        return existing_post

    m = RE_TWITTER_URL.fullmatch(resolved_url)
    if m:
        api = get_api_connection()
        status_id = m.group(1)
        status = api.GetStatus(status_id)
        args = status_to_post_args(api, status, dump_attachments=False)
        attachments = args['attachments'] or []
        attachments.append({
            'type': 'author',
            'id': status.user.id,
            'name': status.user.name,
            'screen_name': status.user.screen_name,
            'profile_image_url_https': status.user.profile_image_url_https,
        })
        args['attachments'] = json.dumps(attachments)
        return Post.objects.create(**args)

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

