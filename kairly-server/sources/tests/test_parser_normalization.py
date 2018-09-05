# import unittest
# import lxml.html
#
# from sources.parser import ArticleParser, fragments_to_string
#
# RULES_ALL_PARAGRAPHS = """
# p
# """
#
#
# class ArticleParserNormalizationTest(unittest.TestCase):
#
#     def test_perex_split(self):
#         doc = """
# <body>
#     <p>abcdefghij</p>
#     <p>klmnopqrst</p>
#     <p>uvwxz12345</p>
#     <p>67890ABCDE</p>
#     <p>FGHIJKLMNO</p>
# </body>"""
