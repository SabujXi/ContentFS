from unittest import TestCase
from ContentFS.pathmatch.rules_parser import gitignore_parser


class TestGitignore_parser(TestCase):
    def test_gitignore_parser(self):
        self.assertTrue(
            gitignore_parser("!a")[0].is_negative
        )

        self.assertTrue(
            gitignore_parser("a/")[0].directories_only
        )

        self.assertTrue(
            gitignore_parser("/a/c/b")[0].is_root_relative
        )
