import unittest
import lxml.html

from sources.parser import ArticleParser, Rule, fragments_to_string


class ArticleParserRulesTest(unittest.TestCase):

    def test_flatten(self):
        rules = """
.perex

/* some comment */
aside
  p, img
    blabla: xyz

div#content
  p, h3
    tag: p
    foo: bar
"""
        parser = ArticleParser(rules)
        self.assertEqual(parser.flatten_rules(), [
            Rule({}, '.perex'),
            Rule({'blabla': 'xyz'}, 'aside p, aside img'),
            Rule({
                'tag': 'p',
                'foo': 'bar'
            }, 'div#content p, div#content h3')
        ])

    def test_flatten_slicing(self):
        rules = """
a, b[0]
  tag: p
"""
        parser = ArticleParser(rules)
        self.assertEqual(parser.flatten_rules(), [
            Rule({'tag': 'p'}, 'a, b[0]'),
        ])

    def test_parse_strip_element(self):
        doc = "<div><p>Hello <em>World</em>!</p><p>Bye</p></div>"
        rules = """
p

em
  tag: none
"""
        expected = "<p>Hello !</p><p>Bye</p>"

        parser = ArticleParser(rules)
        fragments = parser.parse(lxml.html.fromstring(doc))
        article = fragments_to_string(fragments)
        self.assertEqual(article, expected)

    def test_parse_rename_element(self):
        doc = "<div><p>Hello <em>World</em>!</p><p>Bye</p></div>"
        rules = """
p

em
  tag: i
"""
        expected = "<p>Hello <i>World</i>!</p><p>Bye</p>"

        parser = ArticleParser(rules)
        fragments = parser.parse(lxml.html.fromstring(doc))
        article = fragments_to_string(fragments)
        self.assertEqual(article, expected)

    def test_parse_strip_attrubutes(self):
        doc = '<p id="root">Hello <em class="ex">!</em> <a href="#">Go</a></p>'
        rules = """
p
"""
        expected = '<p>Hello <em>!</em> <a href="#">Go</a></p>'

        parser = ArticleParser(rules)
        fragments = parser.parse(lxml.html.fromstring(doc))
        article = fragments_to_string(fragments)
        self.assertEqual(article, expected)

    def test_parse_slicing(self):
        doc = '<div><p><b>1</b><b>2</b></p><b>3</b><b>4</b></div>'
        rules = """
b[0]
"""
        expected = '<b>1</b>'

        parser = ArticleParser(rules)
        fragments = parser.parse(lxml.html.fromstring(doc))
        article = fragments_to_string(fragments)
        self.assertEqual(article, expected)

    def test_parse_notroot(self):
        doc = '<div><div><b>B</b></div></div>'
        rules = """
b
"""
        expected = '<b>B</b>'

        parser = ArticleParser(rules)
        fragments = parser.parse(lxml.html.fromstring(doc))
        article = fragments_to_string(fragments)
        self.assertEqual(article, expected)
