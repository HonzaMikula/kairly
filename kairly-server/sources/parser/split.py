import nltk
from nltk import tokenize
import lxml.html

from .html import is_header, get_textual_length, fragments_to_string, copy_element


class SplitNotPossible(Exception):
    pass


def split_text_to_sentences(text):
    try:
        return tokenize.sent_tokenize(text)
    except LookupError:
        nltk.download('punkt')
        return tokenize.sent_tokenize(text)


def split_element(parent, perex_size):
    perex_size_min, perex_size_max = perex_size
    p1 = copy_element(parent, text=parent.text)
    p2 = copy_element(parent, tail=parent.tail)
    size = len((p1.text or '').strip())  # strip is important, do not change bound with text which contais just spaces

    if size > perex_size_max:
        # wee need to split text

        text_size = 0
        sentences = split_text_to_sentences(p1.text)
        for i, sentence in enumerate(sentences):
            sentence_size = len(sentence)
            if i > 0 and text_size + sentence_size > perex_size_max:
                p1.text = ' '.join(sentences[:i])
                p2.text = ' '.join(sentences[i:])
                p2[:] = list(parent)
                return p1, p2

            text_size += sentence_size

        raise SplitNotPossible()

    # copy elements, because etree modifying parent as elements are assigned to another element
    elements = list(parent)
    p1_elements = []
    p2_elements = []

    def build():
        # do not leave HX tags at the end of perex
        while p1_elements and is_header(p1_elements[-1]):
            p2_elements.insert(0, p1_elements[-1])
            p1_elements.pop()

        if not p1_elements:
            raise SplitNotPossible()

        p1.extend(p1_elements)
        p2.extend(p2_elements)
        return p1, p2

    for i, el in enumerate(elements):
        element_size = get_textual_length(el)

        if size + element_size > perex_size_max:
            if size >= perex_size_min:
                p2_elements = elements[i:]
                return build()

            try:
                # another split needed
                split_size = [min(1, perex_size_min - size), perex_size_max - size]
                part1, part2 = split_element(el, split_size)

                p1_elements.append(part1)
                p2_elements.append(part2)
            except SplitNotPossible as ex:
                if len(elements) == 1:
                    raise ex

                # at least one element is alredy in perex
                if i > 0:
                    p2_elements = elements[i:]
                    return build()

                # no element in perex, add this
                p1_elements.append(el)

            p2.extend(elements[i + 1:])
            return build()

        size += element_size
        p1_elements.append(el)

    raise SplitNotPossible()


def split_article_to_perex_and_content(fragments, perex_size):
    """Split document (represented as list of etree fragments to perex and content.
    perex_size is interval [min_size, max_size]
    Function tries to find as big as possbile perex in given intrval without
    splitting fragments. If not possible, one fragment is splitted.
    """
    perex_size_min, perex_size_max = perex_size
    size = 0
    perex_fragments = []
    content_fragments = []
    nocontent = False

    # print("FRAGMENTS ", fragments)

    for i, el in enumerate(fragments):
        # skip first header at the beginning of article
        if i == 0 and is_header(el):
            continue

        element_size = get_textual_length(el)

        # print("ITER ", element_size, ' ', fragments_to_string([el]))

        if size + element_size > perex_size_max:
            if perex_fragments and size >= perex_size_min:
                content_fragments = fragments[i:]
                break

            # element is too big, split is needed
            try:
                split_size = [max(0, perex_size_min - size), perex_size_max - size]
                part1, part2 = split_element(el, split_size)
                perex_fragments.append(part1)
                content_fragments = [part2]
                content_fragments.extend(fragments[i + 1:])
                break
            except SplitNotPossible:
                perex_fragments.append(el)
                content_fragments = fragments[i + 1:]
                break

        size += element_size
        perex_fragments.append(el)
    else:
        nocontent = True

    perex = fragments_to_string(perex_fragments)
    content = '' if nocontent else fragments_to_string(content_fragments)
    return perex, content
