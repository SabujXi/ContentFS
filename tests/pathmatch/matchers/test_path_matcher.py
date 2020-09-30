from unittest import TestCase
from ContentFS.pathmatch.rules_parser import gitignore_parser
from ContentFS.pathmatch.matchers.path_matcher import PathMatcher
from ContentFS.cpaths.cpath import CPath


class TestPathMatcher(TestCase):
    def test_raw_rule(self):
        self.fail()

    def test_matchers(self):
        self.fail()

    def test_is_negative(self):
        self.fail()

    def test_directories_only(self):
        self.fail()

    def test_is_root_relative(self):
        self.fail()

    def test_matches_simple__parent_dir_exclusion(self):
        path_matcher1 = gitignore_parser("logs")[0]
        "File will be excluded"
        self.assertTrue(
            path_matcher1.matches_simple(CPath("logs"))
        )
        "So does directory"
        self.assertTrue(
            path_matcher1.matches_simple(CPath("logs/"))
        )
        "And any file inside that dire"
        self.assertTrue(
            path_matcher1.matches_simple(CPath("logs/important.log"))
        )
        "And again any dir inside that dir"
        self.assertTrue(
            path_matcher1.matches_simple(CPath("logs/important.log/"))
        )

    def test_matches_simple__parent_dir_exclusion___dir_only(self):
        path_matcher2 = gitignore_parser("logs/")[0]
        "Notice here that it will not match"
        "Dir only pattern will not match file"
        self.assertFalse(
            path_matcher2.matches_simple(CPath("logs"))
        )
        "But will match dirs as usual"
        self.assertTrue(
            path_matcher2.matches_simple(CPath("logs/"))
        )
        "Subdirs will match as before"
        self.assertTrue(
            path_matcher2.matches_simple(CPath("logs/important.log/"))
        )
        "And also anything inside that dir pattern"
        self.assertTrue(
            path_matcher2.matches_simple(CPath("logs/important.log"))
        )

    def test_matches(self):
        self.fail()
