import re
from collections import defaultdict

from lxml import etree
from django.core.exceptions import ValidationError

from .rules import parse_rules
from .normalize import normalize


class ArticleParser:
    REGEX_ATTR_PROP = re.compile(r"\[(\w+)\]")

    DANGEROUS_ELEMENTS = set([
        'script',
        'style',
        'iframe', 'applet', 'object', 'canvas',
        'audio', 'input', 'textarea', 'button', 'select', 'datalist', 'meter',
        'output', 'progress'
    ])

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

        for instr in htmltree.xpath('//processing-instruction()'):
            parent = instr.getparent()
            if parent is not None:
                parent.remove(instr)

        for rule in parse_rules(self.rules):
            if rule.selector == '*':
                elements = [htmltree]
            elif rule.engine == 'xpath':
                elements = list(htmltree.xpath(rule.selector))
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
                    # TODO fix case when moved element has tail
                    el.getparent().remove(el)
                    parent = move_after.getparent()
                    parent.insert(parent.index(move_after) + 1, el)

        elements = self._find_elements(htmltree)

        # Do not select text outside root elements
        for el in elements:
            el.tail = None

        self.props = None
        return elements

    def normalize(self, fragments):
        return normalize(fragments)

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

        attrib = el.attrib
        for attr in list(attrib.keys()):  # use list RuntimeError: dictionary changed size during iteration
            if el.tag == 'img' and attr == 'data-src' and not attrib.get('src'):
                attrib['src'] = attrib['data-src']
            if attr not in preserve:
                del attrib[attr]
            elif attr == 'href' and attrib[attr].startswith('javascript'):
                del attrib[attr]

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

        for attr, value in self._getattrprops(el):
            try:
                if value == 'none':
                    del el.attrib[attr]
                elif value == 'force-https':
                    el.attrib[attr] = re.sub('http://', 'https://', el.attrib[attr])
                elif value.startswith('rename '):
                    new_attr = value[6:].lstip()
                    el.attrib[new_attr] = el.attrib[attr]
                    del el.attrib[attr]
            except KeyError:
                pass
        self._strip_attibutes(el)

        mapped_children = []

        for child in el:
            is_dangerous = child.tag in self.DANGEROUS_ELEMENTS
            tag = self._getprop(child, 'tag')

            if tag == 'none' or is_dangerous:
                # remove element (and may be be replaced with content in
                # subtree which is marked for inclusion
                tail = child.tail

                if not is_dangerous:
                    mapped_children.extend(self._find_elements(child))

                if tail:
                    if mapped_children:
                        last = mapped_children[-1]
                        last.tail = (last.tail or '') + tail
                    else:
                        el.text = (el.text or '') + tail

            else:
                self._prune(child)
                mapped_children.append(child)

        el[:] = mapped_children

    def _find_elements(self, el):
        if el.tag in self.DANGEROUS_ELEMENTS:
            return []

        tag = self._getprop(el, 'tag')
        if tag and tag != 'none':
            self._prune(el)
            el.tail = None
            return [el]

        elements = []
        for child in el:
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


def validate_rules(value):
    try:
        parse_rules(value)
    except Exception as e:
        raise ValidationError(str(e)) from e
