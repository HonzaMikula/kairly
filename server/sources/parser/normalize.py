import re

from .html import is_br, create_element, copy_element, is_phrasing_context

TAG_OMIT_ALLOWED = {'body', 'div', 'article', 'main', 'aside', 'section', 'header', 'footer', 'nav'}
PARAGRAPH_REPLACEMENTS = {'div', 'article', 'main', 'aside', 'section', 'header', 'footer', 'nav'}

SPACE_REGEXP = re.compile(r'(\s)\s+')


def append_text(el, text):
    if el.text:
        el.text += text
    else:
        el.text = text


def append_tail(el, text):
    if el.tail:
        el.tail += text
    else:
        el.tail = text


def get_text(el):
    if not el.text:
        return None
    text = SPACE_REGEXP.sub(r'\1', el.text)
    if not is_phrasing_context(el):
        text = text.lstrip()
    return text


def get_tail(el, rstrip=False):
    if not el.tail:
        return None
    tail = SPACE_REGEXP.sub(r'\1', el.tail)
    if el.tag == 'br' or not is_phrasing_context(el):
        tail = tail.lstrip()
    if rstrip:
        tail = tail.rstrip()
    return tail


class BrBrSplitter:
    """Split element to blocks by <br><br> + flatten block content"""

    def __init__(self, parent, elements):
        self.parent = parent
        self.elements = elements
        self.phrasing_context = is_phrasing_context(parent)
        self.open_block = None

    def append_to_open_block(self, item):
        if self.open_block is None:
            self.open_block = copy_element(self.parent)
        if isinstance(item, str):
            if len(self.open_block):
                append_tail(self.open_block[-1], item)
            else:
                append_text(self.open_block, item)
        else:
            self.open_block.append(item)

    def ends_with_brbr(self):
        try:
            e1, e2 = self.open_block[-2:]
            between = e1.tail and e1.tail.strip()
            if is_br(e1) and is_br(e2) and not between:
                return [e1, e2]
        except ValueError:
            pass

    def trim_brbr(self):
        self.open_block[-2:] = []

    def split(self):
        omit_allowed = self.parent.tag in TAG_OMIT_ALLOWED

        if not omit_allowed:
            self.open_block = copy_element(self.parent)

        if self.parent.text:  # text is already stripped
            self.append_to_open_block(self.parent.text)

        brbr_triggered = False

        for c in self.elements:
            is_block_start = self.open_block is None and not self.phrasing_context

            if (brbr_triggered or is_block_start) and is_br(c):
                # skip all <br>s following immediatelly <br><br>
                # also skip all <br> at the beggining of block tags
                tail = get_tail(c)
                if tail:
                    self.append_to_open_block(tail)
                    brbr_triggered = False
                continue

            brbr_triggered = False

            if is_phrasing_context(c):
                self.append_to_open_block(c)
                brbr = self.ends_with_brbr()
                if brbr:
                    self.trim_brbr()

                    yield self.open_block
                    self.open_block = None
                    tail = get_tail(brbr[1])

                    if self.phrasing_context:
                        # For phrasing context parent, move only <br><br> to block tag level
                        # and split all there
                        # eg transform:
                        #   <i>Hello<br><br>Kitty!<i>
                        # to
                        #    <i>Hello<i/><br><br><i>Kitty!<i>
                        brbr[1].tail = None
                        yield from brbr

                    if tail:  # move tail to a new open block
                        self.append_to_open_block(tail)
                    else:
                        # set flag only if brbr was not interrupted with tail
                        brbr_triggered = True
                continue

            if omit_allowed:
                if self.open_block is not None:
                    yield self.open_block
                    self.open_block = None
                yield c
            else:
                self.append_to_open_block(c)

        if self.open_block is not None:
            yield self.open_block
            self.open_block = None


# @normalize_logging
def normalize_element(el):
    mapped_children = []

    def append_str(s):
        nonlocal mapped_children
        if mapped_children:
            append_tail(mapped_children[-1], s)
        else:
            append_text(el, s)

    for i, child in enumerate(el):
        tail = get_tail(child, rstrip=i == len(el) - 1 and is_phrasing_context(el))
        child.tail = None

        for c in normalize_element(child):
            if isinstance(c, str):
                append_str(c)
            else:
                mapped_children.append(c)

        if tail:
            append_str(tail)

    # read text from element after children are mapped! mapping can change it
    text = el.text = get_text(el)

    # Remove empty elements
    if not text and len(mapped_children) == 0 and el.tag not in {'img', 'video', 'hr', 'br'}:
        return []

    # Don't put <body> to output
    if el.tag == 'body':
        el.tag = 'div'

    # Unfold inline with no semantic
    if el.tag in {'span', 'label', 'legend'}:
        if text:
            mapped_children.insert(0, text)
        return mapped_children

    # Unfold wrapped br
    # Maps <div><br/></div> to just <br/>
    single_br = len(mapped_children) == 1 and is_br(mapped_children[0])
    if not text and single_br and el.tag in TAG_OMIT_ALLOWED:
        return [create_element('br')]

    return list(BrBrSplitter(el, mapped_children).split())


def normalize(fragments):
    result = []
    for el in fragments:
        # fragments has never tail (parser strips them)
        for c in normalize_element(el):
            if isinstance(c, str):
                result.append(create_element('p', text=c))
            else:
                result.append(c)

    result = top_level_cleanup(result)

    # for el in result:
    #     print("---------------")
    #     print(fragments_to_string([el]))

    return result


def top_level_cleanup(blocks):
    result = []
    phrasing_wrapper = None

    for block in blocks:
        tail = get_tail(block)
        is_phrasing = is_phrasing_context(block)

        if block.tag == 'img' and phrasing_wrapper is None:
            # image can remain standalone at top level (if open phrasing
            # wrapped is before)
            is_phrasing = False

        if is_phrasing:
            if block.tag == 'br' and not tail:
                continue  # ignore <br> without tail on top level

            if phrasing_wrapper is None:
                phrasing_wrapper = create_element('p')
                result.append(phrasing_wrapper)

            if block.tag == 'br':
                # append just tail
                if phrasing_wrapper.text:
                    phrasing_wrapper.text += ' ' + tail + ' '
                else:
                    phrasing_wrapper.text = tail + ' '
            else:
                phrasing_wrapper.append(block)
        else:
            # ignore empty blocks
            is_p_like = block.tag == 'p' or block.tag in PARAGRAPH_REPLACEMENTS
            if is_p_like and not list(block) and not (block.text and block.text.strip()):
                continue

            block.tail = None
            result.append(block)
            phrasing_wrapper = None  # prev phrasing_wrapper can't be extended

            if tail:
                phrasing_wrapper = create_element('p', text=tail)
                result.append(phrasing_wrapper)

    # replace top elements with <p> if replacement is safe
    for block in result:
        if block.tag not in PARAGRAPH_REPLACEMENTS:
            continue
        if all(is_phrasing_context(c) for c in block):
            block.tag = 'p'

    return result
