import base64
import re
from functools import partial

import requests
import lxml.html
import orjson as json

from articles.models import Post
from sources.parser.og import parse_og_tags
from sources.twitter_api import get_api_connection, status_to_post_args
from utils.url import fetch_url

RE_TWITTER_URL = re.compile(r'https://(mobile\.)?twitter\.com/[^/]+/status/(\d+)(\?.*)?')
RE_FACEBOOK_POST = re.compile(r'https://(m|www).facebook.com/([^/]+)/posts/(\d+)(\?.*)?')


def create_twitter_link(status_id):
    try:
        return Post.objects.get(guid=f'twitter|{status_id}', kind=Post.TWEET)
    except Post.DoesNotExist:
        api = get_api_connection()
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
        args['attachments'] = json.dumps(attachments).decode()
        return Post.objects.create(**args)


def extend_facebook_link(source, fb_user, fb_post_id, post_args, htmltree):
    post_args['source'] = source
    try:
        el = htmltree.cssselect('.userContentWrapper .clearfix img')[0]
        author_name = el.attrib['aria-label']
        icon_resp = requests.get(el.attrib['src'])
        content_type = icon_resp.headers['Content-Type']
        content = base64.b64encode(icon_resp.content).decode()
        icon = f"data:{content_type};base64,{content}"

        post_args['attachments']['author'] = {
            'id': fb_user,
            'name': author_name,
            'profile_url': f"https://www.facebook.com/{fb_user}",
            'image': icon
        }
        post_args['title'] = None
        post_args['guid'] = f'fb|{fb_user}_{fb_post_id}'
    except IndexError:
        pass
    return post_args


def create_post_link(url, user, hidden=False, published=None, guid=None):
    m = RE_TWITTER_URL.fullmatch(url)
    if m:
        return create_twitter_link(m.group(2))

    extend_callback = None

    m = RE_FACEBOOK_POST.fullmatch(url)
    if m:
        fb_user = m.group(2)
        fb_post_id = m.group(3)
        source = f"https://www.facebook.com/{fb_user}/posts/{fb_post_id}"

        url = source + '?_fb_noscript=1'
        extend_callback = partial(extend_facebook_link, source, fb_user, fb_post_id)

    html, resolved_url = fetch_url(url)
    print(resolved_url)
    existing_post = Post.find_by_source_url(resolved_url)
    if existing_post:
        return existing_post

    m = RE_TWITTER_URL.fullmatch(resolved_url)
    if m:
        return create_twitter_link(m.group(1))

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
        attachments=attachments,  # keep it as dist for extend callback
        author=user,
        price=0,
        weight=0
    )

    if extend_callback:
        args = extend_callback(args, htmltree)

    if published is not None:
        args['published'] = published

    args['attachments'] = json.dumps(args['attachments']).decode() if args['attachments'] else None

    return Post.objects.create(**args)
