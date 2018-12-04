import re
from collections import namedtuple, defaultdict
from itertools import product

import lxml
from lxml import etree

Rule = namedtuple('Rule', ['props', 'selector'])
NestingLevel = namedtuple('NestingLevel', ['indent', 'parts'])


def fragments_to_string(fragments):
    return ''.join(etree.tostring(el, encoding='utf-8').decode('utf-8') for el in fragments)


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

        element_size = len(el.text_content())
        # for each image inside add 200 chars comensation
        # nice to have, calculated image height and add exact compensation
        element_size += len(el.cssselect('img')) * 200

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

    REGEX_MULTI = re.compile(r"/\*.*?\*/", re.DOTALL)
    REGEX_ONLINE = re.compile("//.*?\n")
    REGEX_SPACE = re.compile(r"\s*")
    REGEX_ATTR_PROP = re.compile(r"\[(\w+)\]")

    DANGEROUS_ELEMENTS = ', '.join((
        'script', 'noscript',
        'style',
        'iframe', 'applet', 'object', 'canvas',
        'audio', 'input', 'textarea', 'button', 'select', 'datalist', 'meter',
        'output'
    ))

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

        for el in htmltree.xpath('//p'):
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

    def normalize(self, fragments):
        def fix_brbr(p):
            """If paragraph contains <br><br>, split parts into paragraphs
            Fixes eg. larryarnhart source.
            """
            needs_fix = False
            prev = None
            for node in p.xpath("child::node()"):
                curr = getattr(node, 'tag', None)
                if prev == 'br' and curr == 'br':
                    needs_fix = True
                    break
                prev = curr

            if not needs_fix:
                yield p
                return

            fixed = re.sub(r'<br\s*/?>\s*<br\s*/?>', '</p><p>', fragments_to_string([p]))
            yield from iter(lxml.html.fromstring(fixed))

            # version without parsing but too complicated

            # part = lxml.html.HtmlElement()
            # part.tag = 'p'
            # last = None
            # prev_br = None
            # for node in p.xpath("child::node()"):
            #     tag = getattr(node, 'tag', None)
            #     if tag == 'br':
            #         if prev_br is None:
            #             prev_br = node
            #             continue
            #
            #         yield part
            #         part = lxml.html.HtmlElement('p')
            #         part.tag = 'p'
            #         last = None
            #         prev_br = None
            #         continue
            #
            #     if prev_br is not None:
            #         # only single br
            #         part.append(prev_br)
            #         last = prev_br
            #
            #     prev_br = None
            #
            #     if isinstance(node, str):
            #         if last is None:
            #             part.text = str(node)
            #         else:
            #             last.tail = str(node)
            #
            #     else:
            #         part.append(node)
            #         last = node
            #
            # if len(part) or part.text:
            #     yield part

        def flatten_tree(htmltree, yield_self=True):
            children = list(htmltree)
            if children:
                for el in children:
                    if el.tag in ('div', 'article', 'main', 'aside', 'section', 'header', 'footer', 'nav'):
                        if el.text.strip():
                            result = list(flatten_tree(el, yield_self=False))
                            if result:
                                result[0].text = (el.text or '') + '\n' + (result[0].text or '')
                                yield from result
                                continue
                            else:
                                # flatten_tree returns nothing, this is element with text only
                                yield el
                                continue
                        else:
                            yield from flatten_tree(el)
                            continue
                    if el.tag in ('p', 'h2', 'h3', 'h4', 'h5', 'h6'):
                        children = list(el)
                        if len(children) == 1 and children[0].tag == 'span':
                            if not el.text or not el.text.strip():
                                # yield child <span> as <p> instead, this effectively means
                                # <p><span>foo</span></p> --> <p>foo</p>
                                children[0].tag = el.tag
                                yield children[0]
                                continue
                    yield el
            else:
                if yield_self:
                    yield htmltree

        result = []
        for el in fragments:
            for block in flatten_tree(el):
                if block.tag == 'p':
                    result.extend(fix_brbr(block))
                else:
                    result.append(block)
        return result

    def remove_comments(self, s):
        # remove all occurance streamed comments (/*COMMENT */) from string
        s = self.REGEX_MULTI.sub("", s)
        # remove all occurance singleline comments (//COMMENT\n ) from string
        s = self.REGEX_ONLINE.sub("", s)
        return s

    def flatten_rules(self):
        rules = []
        context = []
        props = {}
        prev_indent = 0

        def parse_property(line):
            if ':' in line:
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

        for line in self.remove_comments(self.rules).split('\n'):
            line = line.rstrip()
            if not line:
                continue

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
