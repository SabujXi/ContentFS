from unittest import TestCase
from ContentFS.pathmatch.matchers import CompMatcher


class TestCompMatcher(TestCase):
    def test_matches(self):
        self.assertRaises(AssertionError, lambda: CompMatcher(""))
        self.assertTrue(CompMatcher("a").matches("a"))
        self.assertTrue(CompMatcher("a?c").matches("abc"))
        self.assertFalse(CompMatcher("a?c").matches("ac"))

        self.assertTrue(CompMatcher("a*c").matches("ac"))
        self.assertTrue(CompMatcher("a*c").matches("abc"))
        self.assertFalse(CompMatcher("a*c").matches("abd"))

        self.assertTrue(CompMatcher("a*").matches("abdfertewtrt"))

        # range test
        self.assertTrue(CompMatcher("[a-x]z").matches("xz"))
        self.assertFalse(CompMatcher("[!a-x]z").matches("xz"))
        self.assertTrue(CompMatcher("[!1-9]").matches("p"))
