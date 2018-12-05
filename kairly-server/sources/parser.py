import re
from collections import namedtuple, defaultdict
from itertools import product

import lxml
from lxml import etree

Rule = namedtuple('Rule', ['props', 'selector'])
NestingLevel = namedtuple('NestingLevel', ['indent', 'parts'])


def fragments_to_string(fragments):
    return ''.join(etree.tostring(el, encoding='utf-8').decode('utf-8') for el in fragments)


def get_element_size(el):
    # for each image inside add 200 chars comensation
    # nice to have, calculated image height and add exact compensation
    if el.tag == 'img':
        return 200

    size = len(el.text.strip()) if el.text else 0
    size += len(el.tail.strip()) if el.tail else 0
    for child in el:
        child_size = get_element_size(child)
        if child_size:
            size += child_size + 1
    return size


def split_article_to_perex_and_content(fragments, perex_size):
    chars = 0
    perex_fragments = []
    content_fragments = []
    nocontent = False

    def is_hx(tag):
        return tag[0] == 'h' and len(tag) == 2

    for i, el in enumerate(fragments):
        # skip all headers at the beginning of article
        if not perex_fragments and is_hx(el.tag):
            continue

        element_size = get_element_size(el)

        if perex_fragments and chars + element_size > perex_size:
            content_fragments = fragments[i:]
            break

        chars += element_size
        perex_fragments.append(el)
    else:
        nocontent = True

    perex = fragments_to_string(perex_fragments)
    content = '' if nocontent else fragments_to_string(content_fragments)
    return perex, content


class ArticleParser:

    REGEX_COMMENT_MULTILINE = re.compile(r"/\*.*?\*/", re.DOTALL)
    REGEX_COMMENT_ONELINE = re.compile(r"([\^ ])//.*")  # do not match // inside eg attr selectors
    REGEX_SPACE = re.compile(r"\s*")
    REGEX_ATTR_PROP = re.compile(r"\[(\w+)\]")

    DANGEROUS_ELEMENTS = ', '.join((
        'script', 'noscript',
        'style',
        'iframe', 'applet', 'object', 'canvas',
        'audio', 'input', 'textarea', 'button', 'select', 'datalist', 'meter',
        'output'
    ))

    LEAF_BLOCK_TAGS = ('p', 'h2', 'h3', 'h4', 'h5', 'h6')
    PARENT_BLOCK_TAGS = ('body', 'div', 'article', 'main', 'aside', 'section', 'header', 'footer', 'nav')

    def __init__(self, rules):
        self.rules = rules

    def parse(self, htmltree):
        """Returns list of fragments (etree Elements)"""
        self.props = defaultdict(dict)

        # self._print(htmltree, "Raw HTML")

        for comment in htmltree.xpath('//comment()'):
            parent = comment.getparent()
            if parent is not None:
                parent.remove(comment)

        # first remove dangerous elements
        for el in htmltree.cssselect(self.DANGEROUS_ELEMENTS):
            el.getparent().remove(el)

        # fix self closing A tags
        for el in htmltree.xpath('//a[not(text())]'):
            if not list(el):  # if not child elements exists
                el.getparent().remove(el)

        for el in htmltree.cssselect('p,div,article,section'):
            if not list(el) and (not el.text or not el.text.strip()):
                el.getparent().remove(el)

        for rule in self.flatten_rules():
            if rule.selector == '*':
                elements = [htmltree]
            else:
                elements = self.cssselect_with_slice(htmltree, rule.selector)

            move_after = None
            move_after_selector = rule.props.get('move-after')
            if move_after_selector:
                try:
                    move_after = htmltree.cssselect(move_after_selector)[0]
                except IndexError:
                    pass

            for el in elements:
                props = self.props[el]
                props.update({'tag': 'auto'})
                props.update(rule.props)

                if move_after is not None:
                    el.getparent().remove(el)
                    parent = move_after.getparent()
                    parent.insert(parent.index(move_after) + 1, el)

        elements = self._find_elements(htmltree)

        self.props = None
        return elements

    def _contains_brbr(self, el):
        prev = None
        for node in el.xpath("child::node()"):
            curr = getattr(node, 'tag', None)
            if prev == 'br' and curr == 'br':
                return True
            prev = curr
        return False

    def _fix_brbr(self, el):
        """If element contains <br><br>, split parts into multiple elements"""
        if not self._contains_brbr(el):
            return [el]

        def new_block():
            b = lxml.html.HtmlElement()
            b.tag = 'div' if el.tag == 'body' else el.tag
            return b

        curr_block = new_block()
        curr_block.text = el.text
        blocks = [curr_block]

        children = list(el)
        prev_br = []
        for c in children:
            is_br = c.tag == 'br'
            tail = c.tail and c.tail.strip()

            if is_br and not tail:
                prev_br.append(c)
                continue

            if len(prev_br) >= 2 or (is_br and len(prev_br) >= 1):
                # close br group
                prev_br = []
                curr_block = new_block()
                blocks.append(curr_block)

                if is_br:
                    curr_block.text = tail
                    continue

            if prev_br:
                # single br is there
                curr_block.extend(prev_br)
                prev_br = []

            curr_block.append(c)

        blocks[-1].tail = el.tail
        return blocks

    def _is_block(self, el):
        return el.tag in self.LEAF_BLOCK_TAGS or el.tag in self.PARENT_BLOCK_TAGS

    def _flatten_leaf(self, el):
        # print("--- FLATTEN_LEAF ---")
        # print(fragments_to_string([el]))

        children = list(el)
        single_child = children[0] if len(children) == 1 else None
        has_text = el.text and el.text.strip()

        if single_child is None or has_text or (single_child.tail and single_child.tail.strip()):
            return el

        if single_child.tag == 'span':
            # yield child <span> as <p> instead, this effectively means
            # <p><span>foo</span></p> --> <p>foo</p>
            children[0].tag = el.tag
            children[0].tail = el.tail
            return children[0]

        if single_child.tag == 'br':
            return single_child

        return el

    def _flatten_parent(self, el):
        blocks = []
        children = list(el)
        text_content = el.text and el.text.strip()
        text_el = None
        if text_content:
            text_el = lxml.html.HtmlElement()
            text_el.tag = 'div' if el.tag == 'body' else el.tag
            text_el.text = text_content
            blocks.append(text_el)

        before_first_block = True
        for c in children:
            # print("--- CHILDREN ---")
            # print(fragments_to_string([c]))

            if self._is_block(c):
                before_first_block = False
                tail_content = c.tail and c.tail.strip()
                if tail_content:
                    c.tail = None
                blocks.extend(self._flatten(c))
                if tail_content:
                    tail_el = lxml.html.HtmlElement()
                    tail_el.tag = c.tag
                    tail_el.text = tail_content
                    blocks.append(tail_el)
            else:
                if text_el is not None and before_first_block:
                    text_el.append(c)
                else:
                    blocks.append(c)

        tail_content = el.tail and el.tail.strip()
        if tail_content:
            if blocks[-1].tail:
                tail_el = lxml.html.HtmlElement()
                tail_el.tag = 'div' if el.tag == 'body' else el.tag
                tail_el.text = tail_content
                blocks.append(tail_el)
            else:
                blocks[-1].tail = tail_content
        return blocks

    def _flatten(self, el):
        for block in self._fix_brbr(el):
            # print("--- BLOCK ---")
            # print(fragments_to_string([block]))

            if block.tag in self.LEAF_BLOCK_TAGS:
                yield self._flatten_leaf(block)
                continue

            if block.tag in self.PARENT_BLOCK_TAGS:
                children = list(block)
                if any(self._is_block(c) for c in children):
                    yield from self._flatten_parent(block)
                else:
                    yield self._flatten_leaf(block)
                continue

            yield block

    def _fix_wrapped_br(self, el):
        def wrapped_br(div):
            children = list(el)
            single_child = children[0] if len(children) == 1 else None
            has_text = el.text and el.text.strip()

            is_wrapped_br = (
                single_child is not None and
                single_child.tag == 'br' and
                not has_text and
                not (single_child.tail and single_child.tail.strip())
            )
            return single_child if is_wrapped_br else None

        # first map chilren
        mapped = [self._fix_wrapped_br(c) for c in el]
        el[:] = mapped

        # self test must be after chilren because of nested <br>
        br = wrapped_br(el)
        if br is None:
            return el
        else:
            br.tail = el.tail
            return br

    def _top_level_cleanup(self, el):
        if el.tag == 'br':
            tail = el.tail and el.tail.strip()
            if tail:
                p = lxml.html.HtmlElement()
                p.tag = 'p'
                p.text = tail
                return p
            return None
        return el

    def normalize(self, fragments):
        for el in fragments:
            for c in el.cssselect('label,legend'):
                c.tag = 'span'

        fragments = [self._fix_wrapped_br(el) for el in fragments]

        result = []
        for fragment in fragments:
            for block in self._flatten(fragment):
                block = self._top_level_cleanup(block)
                if block is not None:
                    result.append(block)

        # for el in result:
        #     print("---- RESULT BLOCK ---")
        #     print(fragments_to_string([el]))

        return result

    def get_effetive_lines(self, s):
        """Remove comments and split to lines"""
        # remove all occurance streamed comments (/*COMMENT */) from string
        s = self.REGEX_COMMENT_MULTILINE.sub("", s)
        # remove all occurance singleline comments (//COMMENT\n ) from string
        for line in s.split('\n'):
            if line.startswith('//'):
                continue
            # line = self.REGEX_COMMENT_ONELINE.sub(r"\1", s)
            line = line.rstrip()
            if line:
                yield line

    def flatten_rules(self):
        rules = []
        context = []
        props = {}
        prev_indent = 0

        def parse_property(line):
            if ': ' in line:
                prop, value = line.split(':', maxsplit=1)
                d = {}
                d[prop.strip()] = value.strip()
                return d

        def flatten_context(context):
            parts = context[0].parts
            if len(context) == 1:
                yield from parts
            else:
                for prod in product(parts, flatten_context(context[1:])):
                    yield ' '.join(prod)

        def normalize_part(part):
            return part.strip()

        def create_rule(props, context):
            return Rule(props, ', '.join(flatten_context(context)))

        for line in self.get_effetive_lines(self.rules):
            m = self.REGEX_SPACE.match(line)
            indent = m.end()

            if indent and not context:
                raise ValueError("Wrong indent. Line: {}".format(line))

            selector = line[indent:]
            prop = parse_property(line)

            if prop:
                if props:
                    if prev_indent != indent:
                        raise ValueError("Wrong indent. Line: {}".format(line))
                else:
                    if prev_indent == indent:
                        raise ValueError("Wrong indent. Line: {}".format(line))
                props.update(prop)
            else:
                if context and prev_indent >= indent:
                    rules.append(create_rule(props, context))

                    props = {}
                    while context and context[-1].indent >= indent:
                        context.pop()

                parts = selector.split(',')
                context.append(NestingLevel(indent, map(normalize_part, parts)))

            prev_indent = indent

        if context:
            rules.append(create_rule(props, context))

        return rules

    def cssselect_with_slice(self, root, selector):
        result = []
        for plain_selector in selector.split(','):
            plain_selector = plain_selector.strip()
            # replace "div [0]" to "div *[0]"
            plain_selector = re.sub(r"\s(\[\d)", r" *\1", plain_selector)

            items = re.split(r"(\[\d[:\d]*\])", plain_selector)
            items = [x for x in items if x]
            if len(items) > 2:
                raise ValueError("Only one slice is currently allowed ({})".format(plain_selector))

            elements = root.cssselect(items[0])
            if len(items) == 2:
                m = re.match(r"\[(\d*)(:)?(\d*)\]", items[1])
                assert m, "Second token should be slice"
                b1 = int(m.group(1)) if m.group(1) else None
                b2 = int(m.group(3)) if m.group(3) else None
                if m.group(2) == ':':
                    sl = slice(b1, b2)
                else:
                    sl = slice(b1, b1 + 1)

                elements = elements[sl]
            result.extend(elements)

        return result

    def _getprop(self, el, name):
        return self.props[el].get(name)

    def _getattrprops(self, el):
        for prop, value in self.props[el].items():
            m = self.REGEX_ATTR_PROP.match(prop)
            if m:
                yield (m.group(1), value)

    def _strip_attibutes(self, el):
        if el.tag == 'img':
            preserve = {'title', 'src', 'alt', 'srcset', 'sizes'}
        elif el.tag == 'a':
            preserve = {'title', 'href'}
        else:
            preserve = {'title'}

        for attr in el.attrib.keys():
            if attr not in preserve:
                del el.attrib[attr]
            elif attr == 'href' and el.attrib[attr].startswith('javascript'):
                del el.attrib[attr]

    def _prune(self, el):
        def reverse_enumerate(arr):
            size = len(arr)
            for i, n in enumerate(arr):
                yield size - i - 1, n

        tag = self._getprop(el, 'tag')
        if tag and tag != 'auto':
            el.tag = tag.lower()
        elif el.tag == 'form' or el.tag == 'fieldset':
            el.tag = 'div'

        self._strip_attibutes(el)
        for attr, value in self._getattrprops(el):
            try:
                if value == 'none':
                    del el.attrib[attr]
                elif value == 'force-https':
                    el.attrib[attr] = re.sub('http://', 'https://', el.attrib[attr])
            except KeyError:
                pass

        for child in list(el):
            tag = self._getprop(child, 'tag')
            if tag == 'none':
                # remove element (and may be be replaced with content in
                # subtree which is marked for inclusion
                i = el.index(child)
                tail = el[i].tail
                del el[i]
                for subchild in reversed(self._find_elements(child)):
                    subchild.tail = ''
                    el.insert(i, subchild)
                if tail:
                    try:
                        el[i].tail = (el[i].tail or '') + tail
                    except (IndexError, TypeError):
                        if el.text is None:
                            el.text = tail
                        else:
                            el.text += tail
            else:
                self._prune(child)

    def _find_elements(self, root):
        tag = self._getprop(root, 'tag')
        if tag and tag != 'none':
            self._prune(root)
            return [root]

        elements = []
        for child in root:
            elements.extend(self._find_elements(child))
        return elements

    def _print(self, htmltree, label="HTML tree"):
        """Debug helper"""
        print("──────────────── {} ────────────────".format(label))
        print(etree.tostring(htmltree, pretty_print=True).decode('utf-8'))
        print("────────────────────────────────")

    def _print_tree(self, htmltree, indent=''):
        """Debug helper"""
        print(htmltree.tag)
        for child in htmltree:
            self._print_tree(child, indent + '  ')
