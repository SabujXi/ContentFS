from unittest import TestCase
from ContentFS.pathmatch.matchers.basic_matchers.sub_comp_matchers import SubCompCharClassMatcher


class TestSubCompCharClassMatcher(TestCase):
    def setUp(self) -> None:
        self.matcher = SubCompCharClassMatcher(['a', 'b', 'c', 'd'], False)
        # TODO: more sophistication needed when constructing char class and then this tests

    def test_matches(self):
        self.assertTrue(
            self.matcher.matches("d")
        )

    def test_regex_pat(self):
        self.assertEqual('[abcd]', self.matcher.regex_pat)
