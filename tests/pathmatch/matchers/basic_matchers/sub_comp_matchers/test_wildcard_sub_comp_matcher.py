from unittest import TestCase
from ContentFS.pathmatch.matchers.basic_matchers.sub_comp_matchers.wildcard_sub_comp_matcher import SubCompWildcardMatcher


class TestSubCompWildcardMatcher(TestCase):
    def setUp(self) -> None:
        self.matcher = SubCompWildcardMatcher("*")

    def test_matches(self):
        self.assertTrue(
            self.matcher.matches(" anything ***** !")
        )

    def test_regex_pat(self):
        self.assertEqual(
            "[^/]*?", self.matcher.regex_pat
        )
