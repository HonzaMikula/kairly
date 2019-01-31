import re
from collections import namedtuple
from itertools import product

__all__ = ['Rule', 'parse_rules']

Rule = namedtuple('Rule', ['engine', 'props', 'selector'])
NestingLevel = namedtuple('NestingLevel', ['engine', 'indent', 'parts'])

# REGEX_COMMENT_MULTILINE = re.compile(r"/\*.*?\*/", re.DOTALL)
REGEX_SPACE = re.compile(r"\s*")


def parse_rules(source):
    rules = []
    context = []
    props = {}
    prev_indent = 0

    for line in get_effetive_lines(source):
        m = REGEX_SPACE.match(line)
        indent = m.end()

        if indent and not context:
            raise ValueError("Wrong indent. Line: {}".format(line))

        selector = line[indent:]

        if selector.startswith('@xpath '):
            prop = None
            if indent:
                raise ValueError("XPath selector is allowed only on top level")
            selector = selector[len('@xpath '):]
            engine = 'xpath'
            # context.append(NestingLevel('xpath', indent, parts=[selector]))
        else:
            engine = 'css'
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
            if indent and context[0].engine != 'css':
                raise ValueError("Only CSS can be nested")

            if context and prev_indent >= indent:
                rules.append(create_rule(props, context))

                props = {}
                while context and context[-1].indent >= indent:
                    context.pop()

            if engine == 'css':
                parts = selector.split(',')
                context.append(NestingLevel(engine, indent, map(normalize_part, parts)))
            else:
                context.append(NestingLevel(engine, indent, [selector]))

        prev_indent = indent

    if context:
        rules.append(create_rule(props, context))

    return rules


def get_effetive_lines(source):
    """Remove comments and split to lines"""
    # remove all occurance streamed comments (/*COMMENT */) from string
    # there is problem with XPath rules which may contains rule //*[foo]
    # rather don't use /* comments at all */
    # s = self.REGEX_COMMENT_MULTILINE.sub("", s)

    for line in source.split('\n'):
        if line.startswith('//'):
            continue
        line = line.rstrip()
        if line:
            yield line


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
    if context[0].engine == 'xpath':
        assert len(context) == 1
        assert len(context[0].parts) == 1
        return Rule('xpath', props, context[0].parts[0])
    else:
        return Rule('css', props, ', '.join(flatten_context(context)))
