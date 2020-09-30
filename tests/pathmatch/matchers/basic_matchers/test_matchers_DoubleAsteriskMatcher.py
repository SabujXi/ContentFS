from unittest import TestCase
from ContentFS.pathmatch.matchers.basic_matchers import DoubleAsteriskMatcher


class TestDoubleAsteriskMatcher(TestCase):
    def test_matches(self):
        matcher = DoubleAsteriskMatcher("**")
        self.assertRaises(Exception, lambda : matcher.matches("aaa", []))
