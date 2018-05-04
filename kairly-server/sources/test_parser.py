import unittest

from .parser import ArticleParser, Rule

RULES = """
.perex

/* comma is applied after slicing !!! */
aside
  p, img[0]

div#content
  p, h3
    as: p
    foo: bar
"""


class ArticleParserTest(unittest.TestCase):

    def test_flatten(self):
        p = ArticleParser(RULES)
        self.assertEqual(p.flatten_rules(), [
            Rule({}, ['.perex']),
            Rule({}, ['aside p', 'aside img [0]']),
            Rule({
                'as': 'p',
                'foo': 'bar'
            }, ['div#content p', 'div#content h3'])
        ])
