from unittest import TestCase
from ContentFS.pathmatch.rules_parser import gitignore_parser
from ContentFS.pathmatch.matchers.basic_matchers.component_matcher import CompMatcher
from ContentFS.pathmatch.matchers.basic_matchers.double_asterisk_matcher import DoubleAsteriskMatcher


class TestGitignore_parser(TestCase):
    def test_gitignore_parser__count_rules(self):
        path_matchers = gitignore_parser("""
        # this is a comment - don't count.
        # the following is invalid, don't count
        /
        **
        /**
        a/v
        """)
        self.assertEqual(len(path_matchers), 3)

    def test_gitignore_parser__negative(self):
        """Tests whether a negative rule passed come out as a negative path matcher"""
        path_matcher1 = gitignore_parser("!a")[0]
        self.assertTrue(
            path_matcher1.is_negative
        )

        path_matcher2 = gitignore_parser("!a/b/c")[0]
        self.assertTrue(
            path_matcher2.is_negative
        )

    def test_gitignore_parser__literal_negation_sign(self):
        "Literal starting bang !"
        path_matcher3 = gitignore_parser(r"\!a/b/c")[0]
        self.assertFalse(
            path_matcher3.is_negative
        )

    def test_gitignore_parser__directories_only(self):
        """Tests whether a pattern that is only for directories come out as directories only path matcher"""
        path_matcher1 = gitignore_parser("a/")[0]
        self.assertTrue(
            path_matcher1.directories_only
        )

        path_matcher2 = gitignore_parser("!/z/a/")[0]
        self.assertTrue(
            path_matcher2.directories_only
        )

    def test_gitignore_parser__root_relative(self):
        """Tests whether a rule that is root relative come out as root relative path matcher"""
        path_matcher1 = gitignore_parser("/a/c/b")[0]
        self.assertTrue(
            path_matcher1.is_root_relative
        )

        path_matcher2 = gitignore_parser("a**b")[0]
        self.assertFalse(
            path_matcher2.is_root_relative
        )

    def test_gitignore_parser__prepended_slash_root_relative(self):
        "Prepending something with just a slash that is just a single directory will make it root relative"
        self.assertTrue(
            gitignore_parser("/a.*")[0].is_root_relative
        )

    def test_gitignore_parser__appended_slash_non_root_relative(self):
        "But appending something with just a slash that is just a single directory will not make it root relative"
        self.assertFalse(
            gitignore_parser("a/")[0].is_root_relative
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

        path_rule2 = gitignore_parser("/a/**/b/**/b/b/")[0]
        self.assertEqual(
            len(path_rule2.matchers), 6
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
