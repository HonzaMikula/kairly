import unittest
import re
import os.path
import lxml.html

from sources.parser import ArticleParser, split_article_to_perex_and_content
from sources.parser import fragments_to_string  # NOQA


def split_test_file(name):
    path = os.path.join(os.path.dirname(__file__), name)
    with open(path) as f:
        file_content = f.read()

    rules_start_idx = file_content.index('<parser-rules>')
    rules_end_idx = file_content.index('</parser-rules>')
    perex_start_idx = file_content.index('<expected-perex>')
    perex_end_idx = file_content.index('</expected-perex>')
    content_start_idx = file_content.index('<expected-content>')
    content_end_idx = file_content.index('</expected-content>')

    source = file_content[:rules_start_idx].strip()
    rules = file_content[rules_start_idx + len('<parser-rules>'):rules_end_idx].strip()
    perex = file_content[perex_start_idx + len('<expected-perex>'):perex_end_idx].strip()
    content = file_content[content_start_idx + len('<expected-content>'):content_end_idx].strip()

    source = lxml.html.document_fromstring(source).cssselect("body")[0]
    return source, rules, perex, content


class ArticleParsersTest(unittest.TestCase):

    maxDiff = None
    SPACE_REGEXP = re.compile(r'(\s)\s+')

    def assertHtmlEqual(self, a, b):
        def normalize(s):
            return self.SPACE_REGEXP.sub(r'\1', s).strip()\
                .replace('\n', ' ').replace('> ', '>').replace(' <', '<')
        self.assertEqual(normalize(a), normalize(b))

    def verify_testcase_file(self, path, perex_size=100):
        source, rules, expected_perex, expected_content = split_test_file(path)

        parser = ArticleParser(rules)
        fragments = parser.parse(source)
        # print(fragments_to_string(fragments))
        fragments = parser.normalize(fragments)
        # print(fragments_to_string(fragments))
        perex, content = split_article_to_perex_and_content(fragments, perex_size)

        self.assertHtmlEqual(perex, expected_perex)
        self.assertHtmlEqual(content, expected_content)

    def test_brbr(self):
        self.verify_testcase_file('test-data/brbr.html')

    def test_dangerous(self):
        self.verify_testcase_file('test-data/dangerous.html')

    def test_empty_p(self):
        self.verify_testcase_file('test-data/empty_p.html')

    def test_flatten(self):
        self.verify_testcase_file('test-data/flatten.html')

    def test_flatten_p(self):
        self.verify_testcase_file('test-data/flatten_p.html')

    def test_h1(self):
        self.verify_testcase_file('test-data/h1.html')

    def test_split(self):
        self.verify_testcase_file('test-data/split.html')

    def test_tag_manipulation(self):
        self.verify_testcase_file('test-data/tag_manipulation.html')

    def test_attr_manipulation(self):
        self.verify_testcase_file('test-data/attr_manipulation.html')
