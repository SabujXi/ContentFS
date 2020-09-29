from unittest import TestCase
from ContentFS.pathmatch.matchers.basic_matchers.component_matcher import CompMatcher


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

    def test_matches__literal_double_asterisk(self):
        "Single asterisk is a wildcard"
        self.assertTrue(
            CompMatcher("a*z").matches("a****z")
        )

        "Two consecutive couple asterisk is just a literal pair of asterisk"
        self.assertFalse(
            CompMatcher("a**z").matches("a****z")
        )

        "Make them uneven and bring a third asterisk and the third one will act as wildcard where the first two are in "
        " love as common ordinary people, the couple"
        self.assertTrue(
            CompMatcher("a***z").matches("a**123z")
        )
        "And obviously the first two cannot act as the pattern"
        self.assertFalse(
            CompMatcher("a***z").matches("a123z")
        )

        "Ordinary people - the loving couples, the literal couple asterisks - matches ordinary couple"
        self.assertTrue(
            CompMatcher("a**z").matches("a**z")
        )
