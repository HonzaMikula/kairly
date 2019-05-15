from urllib.parse import urlsplit, urlunsplit, parse_qs, urlencode

import codecs
import requests
import lxml.html
from bs4 import UnicodeDammit

from django.core.cache import cache
from django.conf import settings


def clean_url(url):
    u = urlsplit(url)
    query = parse_qs(u.query)
    query.pop('ref', None)
    query.pop('source', None)
    query.pop('utm_source', None)
    query.pop('utm_medium', None)
    query.pop('utm_campaign', None)
    query.pop('fbclid', None)
    query.pop('preview', None)
    query.pop('redirected', None)
    qs = urlencode(query)

    return urlunsplit(
        (u.scheme, u.netloc, u.path, qs, u.fragment)
    )


def fetch_url(url, *, usecache=False, user_agent=None):
    cache_key_document = 'fetchurl:doc:' + url
    cache_key_resolved_url = 'fetchurl:resolved_url:' + url

    html = cache.get(cache_key_document) if usecache else None
    resolved_url = cache.get(cache_key_resolved_url) if usecache else None
    if html is None:
        headers = {}
        if user_agent:
            headers['User-Agent'] = user_agent
        else:
            headers['User-Agent'] = settings.DEFAULT_USER_AGENT

        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        if resp.encoding == 'ISO-8859-1':
            # some sources doesn't sent proper encoding header, eg osel.cz or atletika.cz
            encoding = get_encoding_from_meta(resp.content)
            if encoding is not None:
                html = resp.content.decode(encoding)

            if html is None:
                ud = UnicodeDammit(resp.content)
                if ud.unicode_markup:
                    html = ud.unicode_markup

        if html is None:
            html = resp.content.decode(resp.encoding)

        resolved_url = resp.url

        if usecache:
            cache.set(cache_key_document, html, 3600)
            cache.set(cache_key_resolved_url, resolved_url, 3610)

    assert resolved_url is not None, "Inconsistent cache"
    return html, resolved_url


def get_encoding_from_meta(content):
    for meta in lxml.html.fromstring(content).cssselect('meta'):
        try:
            if meta.attrib['http-equiv'] == 'Content-Type':
                _, charset = meta.attrib['content'].split('=')
                return codecs.lookup(charset).name
        except (KeyError, ValueError, LookupError):
            pass
