import unittest

from sources.directives import parse


class DirectivesTest(unittest.TestCase):

    def test_valid(self):
        conf = 'skip domain seznam.cz\nskip domain centrum.cz'
        directives = parse(conf)
        assert len(directives) == 2

    def test_comments(self):
        conf = '# test\n\n\nskip domain seznam.cz'
        directives = parse(conf)
        assert len(directives) == 1

    def test_bad_arg(self):
        conf = 'skip foo seznam.cz\nskip domain centrum.cz'
        with self.assertRaises(ValueError):
            parse(conf)

    def test_bad_directove(self):
        conf = 'foo'
        with self.assertRaises(ValueError):
            parse(conf)
