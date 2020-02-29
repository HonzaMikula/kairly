from string import whitespace
from collections import namedtuple

import lxml.html
from lxml.etree import ParserError


PostWeight = namedtuple('PostWeight', ['word_chars', 'images'])
IMAGE_WEIGHT = 140
MIN_POST_WEIGHT = 100


def calculate_post_weight(post):
    # dont' import Post to avoid circular import
    if post.kind in [post.RECOMMENDATION, post.REFERENCE]:
        return 0

    word_chars = 0
    images = 0

    if post.perex:
        try:
            htmltree = lxml.html.fromstring(post.perex)
            perex_word_chars, perex_images = calculate_element_weight(htmltree)
            word_chars += perex_word_chars
            images += perex_images
        except ParserError:
            pass

    if post.content:
        try:
            htmltree = lxml.html.fromstring(post.content)
            content_word_chars, content_images = calculate_element_weight(htmltree)
            word_chars += content_word_chars
            images += content_images
        except ParserError:
            pass

    weight = word_chars + min(images, 8) * IMAGE_WEIGHT  # count not more than 8 images
    return max(MIN_POST_WEIGHT, weight)


def calculate_element_weight(el):
    # nice to have, calculated image height and add exact compensation
    if el.tag == 'img':
        return PostWeight(0, 1)

    word_chars = count_word_chars(el.text) if el.text is not None else 0
    word_chars += count_word_chars(el.tail) if el.tail is not None else 0
    images = 0
    for child in el:
        child_word_chars, child_images = calculate_element_weight(child)
        word_chars += child_word_chars
        images += child_images

    return PostWeight(word_chars, images)


def count_word_chars(s):
    return sum(1 for c in s if c not in whitespace)
