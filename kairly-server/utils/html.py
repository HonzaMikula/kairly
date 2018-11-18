import os
import os.path
import uuid

from lxml import etree
import lxml.html
import bleach

from utils.upload import file_from_data_uri
from django.conf import settings

ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'br', 'blockquote', 'code', 'div', 'em',
    'h2', 'h3', 'h4',
    'i', 'img',
    'li', 'ol', 'p', 'span', 'strong', 'u', 'ul'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
    'img': ['src', 'alt', 'title', 'width', 'height']
}
# allow data URIs
ALLOWED_PROTOCOLS = ['http', 'https', 'data']


def sanitize(text):
    text = bleach.clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
                        protocols=ALLOWED_PROTOCOLS)
    if text == '<p><br></p>':
        return ''
    return text


def convert_data_uris(content):
    """Extract all data uris and save them as regular media files"""
    try:
        htmltree = lxml.html.fromstring(content)
    except etree.ParserError as ex:
        if ex.args[0] == 'Document is empty':
            return ''
        raise

    for el in htmltree.cssselect("img[src^='data:']"):
        hash = uuid.uuid4().hex
        rel_dir = os.path.join('posts', hash[:2], hash[2:4])
        abs_dir = os.path.join(settings.MEDIA_ROOT, rel_dir)
        basename = hash[4:]
        f = file_from_data_uri(el.attrib['src'], basename)
        rel_name = os.path.join(rel_dir, f.name)
        abs_name = os.path.join(abs_dir, f.name)
        os.makedirs(abs_dir, exist_ok=True)
        with open(abs_name, 'wb') as outf:
            outf.write(f.file.read())
        el.attrib['src'] = settings.MEDIA_SITE + settings.MEDIA_URL + rel_name

    return etree.tostring(htmltree, encoding='utf-8').decode('utf-8')
