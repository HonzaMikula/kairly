import re
from collections import namedtuple
from itertools import product

Rule = namedtuple('Rule', ['props', 'selectors'])
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
                prop, value = line.split(':')
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
            part = part.strip()
            return re.sub('(\w)\[', '\\1 [', part)

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
                    rules.append(Rule(props, list(flatten_context(context))))

                    props = {}
                    while context and context[-1].indent >= indent:
                        context.pop()

                parts = selector.split(',')
                context.append(NestingLevel(indent, map(normalize_part, parts)))

            prev_indent = indent

        if context:
            rules.append(Rule(props, list(flatten_context(context))))

        return rules
