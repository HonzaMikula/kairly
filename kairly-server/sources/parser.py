import re
from collections import namedtuple, defaultdict
from itertools import product

from lxml import etree

Rule = namedtuple('Rule', ['props', 'selector'])
NestingLevel = namedtuple('NestingLevel', ['indent', 'parts'])


class ArticleParser:

    REGEX_MULTI = re.compile("/\*.*?\*/", re.DOTALL)
    REGEX_ONLINE = re.compile("//.*?\n")
    REGEX_SPACE = re.compile("\s*")

    DANGEROUS_ELEMENTS = ', '.join((
        'script', 'noscript',
        'style',
        'iframe', 'applet', 'object', 'canvas',
        'audio', 'input', 'textarea', 'button', 'select', 'datalist', 'meter',
        'output'
    ))

    def __init__(self, rules):
        self.rules = rules

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

    def _getprop(self, el, name):
        return self.props[el].get(name)

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
                    except IndexError:
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

    def parse(self, htmltree):
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
        return ''.join(etree.tostring(el, encoding='utf-8').decode('utf-8') for el in elements)

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
