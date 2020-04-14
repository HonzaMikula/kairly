from html import escape
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

import lxml.html
import orjson as json

from articles.models import Post
from utils.url import fetch_url
from .parser.og import parse_og_tags
from .domains.facebook import FacebookImporter
from .domains.twitter import TwitterImporter
from .domains.threadreaderapp import ThreadReaderAppImporter
from .domains.medium import MediumImporter

IMPORTERS = {cls.DOMAIN: cls() for cls in (TwitterImporter, FacebookImporter, ThreadReaderAppImporter, MediumImporter)}
IGNORED_QUERY = set([
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'utm_brand',
    'fbclid', 'sessionId'])


def clean_qs(url):
    p = urlparse(url)
    cleaned_query = {k: v for k, v in parse_qs(p.query).items() if k not in IGNORED_QUERY}
    return urlunparse((p.scheme, p.netloc, p.path, p.params, urlencode(cleaned_query, doseq=True), ''))  # strip also fragment


def create_post_link(url, user, hidden=False, published=None, guid=None):
    extend_callback = None
    for importer in IMPORTERS.values():
        match = importer.match(url)
        if match:
            if isinstance(match, Post):
                return match
            url, guid, extend_callback = match

    if guid:
        try:
            return Post.objects.get(guid=guid, kind=Post.LINK)
        except Post.DoesNotExist:
            pass

    html, resolved_url = fetch_url(url)
    existing_post = Post.find_by_source_url(resolved_url)
    if existing_post:
        return existing_post

    # verify resolved url agains twitter again (handles url shorteners)
    post = TwitterImporter().match(resolved_url)
    if post:
        return post

    htmltree = lxml.html.fromstring(html)
    try:
        title = htmltree.cssselect('head title')[0].text
    except IndexError:
        title = resolved_url
    try:
        description = htmltree.cssselect('head meta[name=description]')[0].attrib.get('content', '')
    except IndexError:
        description = ''

    attachments = {}
    og = parse_og_tags(htmltree)
    if 'image' in og:
        attachments['image'] = og['image']

    args = dict(
        kind=Post.LINK,
        source=resolved_url,
        guid=guid,
        protected=False,
        hidden=hidden,
        title=og.get('title', title).strip(),
        perex='<p>' + escape(og.get('description', description).strip()) + '</p>',
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
