import lxml.html
import orjson as json

from articles.models import Post
from utils.url import fetch_url
from .parser.og import parse_og_tags
from .domains.facebook import FacebookImporter
from .domains.twitter import TwitterImporter
from .domains.thereaderapp import TheReaderAppImporter
from .domains.medium import MediumImporter

importers = {cls.DOMAIN: cls() for cls in (TwitterImporter, FacebookImporter, TheReaderAppImporter, MediumImporter)}


def create_post_link(url, user, hidden=False, published=None, guid=None):
    # TODO get imported by domain
    extend_callback = None
    for importer in importers.values():
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
