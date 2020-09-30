from unittest import TestCase
from ContentFS.pathmatch.rules_parser import gitignore_parser
from ContentFS.pathmatch.matchers.path_matcher import PathMatcher
from ContentFS.cpaths.cpath import CPath


class TestPathMatcher(TestCase):
    def test_raw_rule(self):
        path_matcher1 = gitignore_parser("!a/**/b/*?l/x.txt/")[0]
        self.assertEqual(path_matcher1.raw_rule, "!a/**/b/*?l/x.txt/")

    def test_matchers(self):
        "Consecutive double asterisks will be counted as single double asterisk and non stand alone double asterisks \
        are literal strings"
        path_matcher1 = gitignore_parser("!a/**/**/b/*?l/**/**/**/**x.txt/")[0]
        self.assertEqual(len(path_matcher1.matchers), 6)

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

    def test_matches_simple__negative(self):
        path_matcher1 = gitignore_parser("!a")[0]
        self.assertTrue(
            path_matcher1.matches_simple(CPath("a"))
        )

        self.assertTrue(
            path_matcher1.matches_simple(CPath("z/a"))
        )

        self.assertFalse(
            path_matcher1.matches_simple(CPath("b"))
        )

    def test_matches(self):
        path_matcher1 = gitignore_parser("!a")[0]
        self.assertFalse(
            path_matcher1.matches(CPath("a"))
        )

        self.assertFalse(
            path_matcher1.matches(CPath("z/a"))
        )

        self.assertFalse(
            path_matcher1.matches(CPath("b"))
        )

    def test_matches__negative(self):
        """Tests whether negative matching works properly"""
        self.assertFalse(
            gitignore_parser("!a")[0].matches(CPath("b"))
        )

        self.assertFalse(
            gitignore_parser("!a")[0].matches(CPath("a"))
        )

    def test_matches__directories_only(self):
        """Tests whether directories only rule matchers properly"""
        path_rule1 = gitignore_parser("z/?u*ns/")[0]
        "This is a directories only rule"
        self.assertTrue(
            path_rule1.directories_only
        )
        "And it matches as it should be"
        self.assertTrue(
            path_rule1.matches(
                CPath("z/humans/")
            )
        )

        path_rule2 = gitignore_parser("z/?uman")[0]
        "This is NOT a directories only rule"
        self.assertFalse(
            path_rule2.directories_only
        )
        "But it matches as it should be"
        self.assertTrue(
            path_rule2.matches(CPath("z/human"))
        )
        "It matches both filesCpath (above) and directories (below)"
        self.assertTrue(
            path_rule2.matches(CPath("z/human/"))
        )

    def test_matches__root_relative(self):
        """Tests whether the produced rule behaves well when it is root relative"""
        path_rule1 = gitignore_parser("a/*/z")[0]
        self.assertTrue(
            path_rule1.is_root_relative
        )
        "It matches a path that is root relative"
        self.assertTrue(
            path_rule1.matches(CPath("a/b/z"))
        )
        "But it doesn't match inner path"
        self.assertFalse(
            path_rule1.matches(CPath("1/a/b/z"))
        )

        "But if the rule is not root relative"
        path_rule2 = gitignore_parser("a*z")[0]

        self.assertTrue(
            path_rule2.matches(CPath("ayz"))
        )

    def test_matches__critical_double_asterisks(self):
        # TODO: make many rules for critial double asterisks - including within it all other kinds of rules
        path_matcher1 = gitignore_parser("**/a/**/**/m/z/z/z/z")[0]
        self.assertFalse(
            path_matcher1.matches(CPath("a/m/z"))
        )

        self.assertTrue(
            path_matcher1.matches(CPath("l/a/z/a/m/z/z/z/z"))
        )
