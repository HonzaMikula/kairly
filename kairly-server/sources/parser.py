import re
from collections import namedtuple
from itertools import product

from lxml.etree import tostring

Rule = namedtuple('Rule', ['props', 'selector'])
NestingLevel = namedtuple('NestingLevel', ['indent', 'parts'])


class ArticleParser:

    REGEX_MULTI = re.compile("/\*.*?\*/", re.DOTALL)
    REGEX_ONLINE = re.compile("//.*?\n")
    REGEX_SPACE = re.compile("\s*")

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

    def parse(self, htmltree):
        result = []

        for rule in self.flatten_rules():
            wrap_into = rule.props.get('as')
            for el in self.cssselect_with_slice(htmltree, rule.selector, rule.props.get('slice')):
                if wrap_into == 'img':
                    result.append('<img alt="{alt}" title="{title}" src="{src}" />'.format(
                        alt=el.attrib.get('alt'),
                        title=el.attrib.get('title'),
                        src=el.attrib.get('src')))
                else:
                    # content = el.text_content().strip()
                    content = tostring(el, encoding='utf-8').decode('utf-8')
                    if wrap_into:
                        result.append("<{tag}>{content}</{tag}>".format(tag=wrap_into, content=content))
                    else:
                        result.append(content)
        return '\n\n'.join(result)

    def cssselect_with_slice(self, htmltree, selector, slice_prop):
        sl = None
        if slice_prop:
            m = re.match(r"\[(\d*)(:)?(\d*)\]", slice_prop)
            if m:
                b1 = int(m.group(1)) if m.group(1) else None
                b2 = int(m.group(3)) if m.group(3) else None
                if m.group(2) == ':':
                    sl = slice(b1, b2)
                else:
                    sl = slice(b1, b1 + 1)
        elements = htmltree.cssselect(selector)
        if sl:
            return elements[sl]
        return elements
