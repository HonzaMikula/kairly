import unittest

from sources.parser import ArticleParser, Rule

RULES = """
.perex

/* some comment */
aside
  p, img
    slice: [0]

div#content
  p, h3
    as: p
    foo: bar
"""


class ArticleParserTest(unittest.TestCase):

    def test_flatten(self):
        p = ArticleParser(RULES)
        self.assertEqual(p.flatten_rules(), [
            Rule({}, '.perex'),
            Rule({'slice': '[0]'}, 'aside p, aside img'),
            Rule({
                'as': 'p',
                'foo': 'bar'
            }, 'div#content p, div#content h3')
        ])
