import unittest
import lxml.html

from sources.parser import split_article_to_perex_and_content

RULES_ALL_PARAGRAPHS = """
p
"""


class ArticleParserSplitTest(unittest.TestCase):

    def test_perex_split(self):
        doc = "<body><p>abcdefghij</p><p>klmnopqrst</p><p>uvwxz12345</p><p>67890ABCDE</p><p>FGHIJKLMNO</p></body>"
        fragments = list(lxml.html.fromstring(doc))

        perex, content = split_article_to_perex_and_content(fragments, 20)
        self.assertEqual(perex, '<p>abcdefghij</p><p>klmnopqrst</p>')
        self.assertEqual(content, '<p>uvwxz12345</p><p>67890ABCDE</p><p>FGHIJKLMNO</p>')

        perex, content = split_article_to_perex_and_content(fragments, 21)
        self.assertEqual(perex, '<p>abcdefghij</p><p>klmnopqrst</p>')
        self.assertEqual(content, '<p>uvwxz12345</p><p>67890ABCDE</p><p>FGHIJKLMNO</p>')

        # aleways put at leas on fragment
        perex, content = split_article_to_perex_and_content(fragments, 1)
        self.assertEqual(perex, '<p>abcdefghij</p>')
        self.assertEqual(content, '<p>klmnopqrst</p><p>uvwxz12345</p><p>67890ABCDE</p><p>FGHIJKLMNO</p>')

        perex, content = split_article_to_perex_and_content(fragments, 100)
        self.assertEqual(perex, '<p>abcdefghij</p><p>klmnopqrst</p><p>uvwxz12345</p><p>67890ABCDE</p><p>FGHIJKLMNO</p>')
        self.assertEqual(content, '')

    def test_ignore_headers(self):
        doc = "<body><h1>Title</h1><p>abcdefghij</p><p>klmnopqrst</p></body>"
        fragments = list(lxml.html.fromstring(doc))

        perex, content = split_article_to_perex_and_content(fragments, 12)
        self.assertEqual(perex, '<p>abcdefghij</p>')
        self.assertEqual(content, '<p>klmnopqrst</p>')

        doc = "<body><p>abcdefghij</p><h1>Title</h1><p>klmnopqrst</p></body>"
        fragments = list(lxml.html.fromstring(doc))

        perex, content = split_article_to_perex_and_content(fragments, 12)
        self.assertEqual(perex, '<p>abcdefghij</p>')
        self.assertEqual(content, '<h1>Title</h1><p>klmnopqrst</p>')
