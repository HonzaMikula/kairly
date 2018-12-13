import lxml.html
from lxml import etree

PHRASING_CONTEXT_TAGS = {
    'a', 'abbr', 'b', 'bdo', 'br', 'cite', 'code',
    'data', 'datalist', 'dfn', 'em', 'i', 'img', 'kbd', 'mark', 'math',
    'meter', 'output', 'q', 'ruby', 'samp', 'small', 'span',
    'strong', 'sub', 'sup', 'svg', 'time', 'var', 'video', 'wbr'
}


def fragments_to_string(fragments):
    return ''.join(etree.tostring(el, encoding='utf-8').decode('utf-8') for el in fragments)


def create_element(tag, text=None, *, tail=None, children=None):
    el = lxml.html.HtmlElement()
    el.tag = tag
    if text:
        el.text = text
    if tail:
        el.tail = tail
    if children:
        el[:] = children
    return el


def copy_element(el, text=None, *, tail=None, children=None):
    cpy = create_element(el.tag, text, tail=tail, children=children)
    if el.attrib:
        cpy.attrib.update(el.attrib)
    return cpy


def is_header(el):
    if isinstance(el, str):
        return False
    return el.tag[0] == 'h' and len(el.tag) == 2


def is_phrasing_context(el):
    if isinstance(el, str):
        return True
    return el.tag in PHRASING_CONTEXT_TAGS


def is_br(el):
    return not isinstance(el, str) and el.tag == 'br'


def get_textual_length(el):
    # for each image inside add 200 chars comensation
    # nice to have, calculated image height and add exact compensation
    if el.tag == 'img':
        return 200

    size = len(el.text.strip()) if el.text else 0
    size += len(el.tail.strip()) if el.tail else 0
    for child in el:
        child_size = get_textual_length(child)
        if child_size:
            if size:
                size += 1
            size += child_size
    return size
