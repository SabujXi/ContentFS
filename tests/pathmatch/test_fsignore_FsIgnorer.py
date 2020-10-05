from unittest import TestCase
from ContentFS.pathmatch.fsmatchers import FsMatcherGitignore
from ContentFS.cpaths.cpath import CPath


class TestFsIgnorer(TestCase):
    def test_ignore__non_root_relative(self):
        self.assertTrue(
            FsMatcherGitignore("*.log")._ignore(CPath("important/trace.log"))
        )

    def test_ignore__single_path_rule_root_relative(self):
        self.assertFalse(
            FsMatcherGitignore("/a")._ignore(CPath("b/a"))
        )

    def test_ignore__single_path_n_pattern(self):
        self.assertTrue(
            FsMatcherGitignore("a")._ignore(CPath("a"))
        )
        self.assertTrue(
            FsMatcherGitignore("a")._ignore(CPath("a/"))
        )
        self.assertFalse(
            FsMatcherGitignore("a/")._ignore(CPath("a"))
        )

    def test_ignore__wildcard_middle(self):
        self.assertTrue(
            FsMatcherGitignore("a/*/z")._ignore(CPath("a/b/z"))
        )

    def test_ignore__char_class(self):
        self.assertFalse(
            FsMatcherGitignore("a/[!0-8]z")._ignore(CPath("a/8z"))
        )

        self.assertTrue(
            FsMatcherGitignore("a/[!0-8]z")._ignore(CPath("a/9z"))
        )

        self.assertFalse(
            FsMatcherGitignore("a/[!0-8]z")._ignore(CPath("a/09z"))
        )

    def test_ignore__double_asterisk(self):
        self.assertTrue(
            FsMatcherGitignore("m/**")._ignore(CPath("m/n/o9z"))
        )

        self.assertTrue(
            FsMatcherGitignore("a/**/z")._ignore(CPath("a/b/c/d/z"))
        )

        self.assertTrue(
            FsMatcherGitignore("a/**/z")._ignore(CPath("a/z"))
        )

        self.assertTrue(
            FsMatcherGitignore("a/**/z")._ignore(CPath("a/b/z/c/z"))
        )

        self.assertFalse(
            FsMatcherGitignore("a/**/z/q/z")._ignore(CPath("a/b/z/c/z"))
        )

    def test_ignore__double_asterisk_w_char_class(self):
        self.assertTrue(
            FsMatcherGitignore("a/**/[!0-8]z")._ignore(CPath("a/b/c/d/9z"))
        )

        self.assertFalse(
            FsMatcherGitignore("a/**/[!0-8]z")._ignore(CPath("a/b/c/d/8z"))
        )

    def test_ignore__negation(self):
        """
        Rules:
            *.log
            !important.log

        Matches:
            debug.log
            trace.log
        but not
            important.log
            logs/important.log
        """
        fs_ignore = FsMatcherGitignore("*.log\n!important.log")
        # will match
        self.assertTrue(
            fs_ignore._ignore(CPath("debug.log"))
        )
        self.assertTrue(
            fs_ignore._ignore(CPath("trace.log"))
        )
        # will not match
        self.assertFalse(
            fs_ignore._ignore(CPath("important.log"))
        )
        self.assertFalse(
            fs_ignore._ignore(CPath("logs/important.log"))
        )

    def test_ignore__negation_re_ignore(self):
        """
        Rules:
            *.log
            !important/*.log
            trace.*
        Matches:
            debug.log
            important/trace.log
        but not:
            important/debug.log
        """
        fs_ignore = FsMatcherGitignore("*.log\n!important/*.log\ntrace.*")
        self.assertTrue(
            fs_ignore._ignore(CPath("debug.log"))
        )
        self.assertTrue(
            fs_ignore._ignore(CPath("important/trace.log"))
        )
        self.assertFalse(
            fs_ignore._ignore(CPath("important/debug.log"))
        )

    def test_ignore__negation_directory(self):
        """
        Rules:
            logs/
            !logs/important.log
        Will ignore (inspite of !...):
            logs/debug.log
            logs/important.log
        This is due to the performance reason git do not re-include when a parent directory is ignored.
        """
        fs_ignore = FsMatcherGitignore("logs/\n!logs/important.log")
        self.assertTrue(
            fs_ignore._ignore(CPath("logs/debug.log"))
        )
        self.assertTrue(
            fs_ignore._ignore(CPath("logs/important.log"))
        )

    def test_ignore__everything_inside_dir(self):
        fs_ignore = FsMatcherGitignore("logs/")
        self.assertTrue(
            fs_ignore._ignore(CPath("logs/a"))
        )
        self.assertTrue(
            fs_ignore._ignore(CPath("logs/b.txt"))
        )

    def test_ignore__dot_git(self):
        fs_ignore = FsMatcherGitignore(".git/")
        self.assertTrue(fs_ignore._ignore(CPath(".git/")))
