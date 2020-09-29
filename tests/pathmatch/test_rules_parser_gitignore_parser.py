from unittest import TestCase
from ContentFS.pathmatch.rules_parser import gitignore_parser
from ContentFS.pathmatch.matchers.basic_matchers.component_matcher import CompMatcher
from ContentFS.pathmatch.matchers.basic_matchers.double_asterisk_matcher import DoubleAsteriskMatcher
from ContentFS.cpaths.cpath import CPath


class TestGitignore_parser(TestCase):
    def test_gitignore_parser__negative(self):
        """Tests whether a negative rule passed come out as a negative path matcher"""
        self.assertTrue(
            gitignore_parser("!a")[0].is_negative
        )

        self.assertTrue(
            gitignore_parser("!a/b/c")[0].is_negative
        )

    def test_gitignore_parser__directories_only(self):
        """Tests whether a pattern that is only for directories come out as directories only path matcher"""

        self.assertTrue(
            gitignore_parser("a/")[0].directories_only
        )

        self.assertTrue(
            gitignore_parser("!/z/a/")[0].directories_only
        )

    def test_gitignore_parser__root_relative(self):
        """Tests whether a rule that is root relative come out as root relative path matcher"""
        self.assertTrue(
            gitignore_parser("/a/c/b")[0].is_root_relative
        )

        self.assertFalse(
            gitignore_parser("a**b")[0].is_root_relative
        )

    def test_gitignore_parser__root_relative_prepended_slash(self):
        "Prepending something with just a slash that is just a single directory will make it root relative"
        self.assertTrue(
            gitignore_parser("/a.*")[0].is_root_relative
        )

    def test_gitignore_parser__root_relative_appended_slash(self):
        "But appending something with just a slash that is just a single directory will not make it root relative"
        self.assertFalse(
            gitignore_parser("a/")[0].is_root_relative
        )

    def test_gitignore_parser__matches_negative(self):
        """Tests whether negative matching works properly"""
        self.assertTrue(
            gitignore_parser("!a")[0].matches(CPath("b"))
        )

        self.assertFalse(
            gitignore_parser("!a")[0].matches(CPath("a"))
        )

    def test_gitignore_parser__matches_directories_only(self):
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

    def test_gitignore_parser__matches_root_relative(self):
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

    def test_gitignore_parser__matchers_double_asterisks(self):
        path_rule1 = gitignore_parser("a/**/b")[0]
        self.assertEqual(
            len(path_rule1.matchers), 3
        )
        self.assertIsInstance(
            path_rule1.matchers[1], DoubleAsteriskMatcher
        )
        self.assertIsInstance(
            path_rule1.matchers[0], CompMatcher
        )

    def test_gitignore_parser__matchers_literal_double_asterisks(self):
        """
        From gitignore doc:
                Two consecutive asterisks ("**") in patterns matched against full pathname may have special meaning:

                    A leading "**" followed by a slash means match in all directories. For example, "**/foo" matches file or directory "foo" anywhere, the same as pattern "foo". "**/foo/bar" matches file or directory "bar" anywhere that is directly under directory "foo".

                    A trailing "/**" matches everything inside. For example, "abc/**" matches all files inside directory "abc", relative to the location of the .gitignore file, with infinite depth.

                    A slash followed by two consecutive asterisks then a slash matches zero or more directories. For example, "a/**/b" matches "a/b", "a/x/b", "a/x/y/b" and so on.

                    Other consecutive asterisks are considered regular asterisks and will match according to the previous rules.
        I am up for the Other... port here
        """
        path_rule1 = gitignore_parser("a**b")[0]
        self.assertEqual(
            len(path_rule1.matchers), 1
        )
        self.assertIsInstance(
            path_rule1.matchers[0], CompMatcher
        )


