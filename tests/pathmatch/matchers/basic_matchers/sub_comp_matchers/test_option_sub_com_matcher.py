from unittest import TestCase
from ContentFS.pathmatch.matchers.basic_matchers.sub_comp_matchers.option_sub_com_matcher import SubCompOptionMatcher


class TestSubCompOptionMatcher(TestCase):
    def setUp(self) -> None:
        self.matcher = SubCompOptionMatcher("?")

    def test_matches(self):
        self.assertTrue(
            self.matcher.matches("+")
        )

        self.assertFalse(
            self.matcher.matches('/')
        )

    def test_regex_pat(self):
        self.assertEqual(
            self.matcher.regex_pat, "[^/]"
        )
