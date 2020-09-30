from unittest import TestCase
from ContentFS.pathmatch.matchers.basic_matchers.sub_comp_matchers.string_sub_comp_matcher import SubCompStringMatcher
import re


class TestSubCompStringMatcher(TestCase):
    def setUp(self) -> None:
        self.matcher = SubCompStringMatcher("my *")

    def test_matches(self):
        self.assertTrue(
            self.matcher.matches("my *")
        )

    def test_regex_pat(self):
        self.assertEqual(
            re.escape("my *"), self.matcher.regex_pat
        )
