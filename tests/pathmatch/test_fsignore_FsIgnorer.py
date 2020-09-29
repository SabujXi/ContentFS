from unittest import TestCase
from ContentFS.pathmatch.fsignore import FsIgnorer
from ContentFS.cpaths.cpath import CPath


class TestFsIgnorer(TestCase):
    def test_ignore(self):
        self.assertTrue(
            FsIgnorer("*.log").ignore(CPath("important/trace.log"))
        )
        self.assertTrue(
            FsIgnorer("a").ignore(CPath("a"))
        )
        self.assertTrue(
            FsIgnorer("a").ignore(CPath("a/"))
        )
        self.assertFalse(
            FsIgnorer("a/").ignore(CPath("a"))
        )

        self.assertTrue(
            FsIgnorer("a/*/z").ignore(CPath("a/b/z"))
        )

        self.assertFalse(
            FsIgnorer("a/[!0-8]z").ignore(CPath("a/8z"))
        )

        self.assertTrue(
            FsIgnorer("a/[!0-8]z").ignore(CPath("a/9z"))
        )

        self.assertFalse(
            FsIgnorer("a/[!0-8]z").ignore(CPath("a/09z"))
        )

        self.assertTrue(
            FsIgnorer("m/**").ignore(CPath("m/n/o9z"))
        )

        self.assertTrue(
            FsIgnorer("a/**/z").ignore(CPath("a/b/c/d/z"))
        )

        self.assertTrue(
            FsIgnorer("a/**/[!0-8]z").ignore(CPath("a/b/c/d/9z"))
        )

        self.assertFalse(
            FsIgnorer("a/**/[!0-8]z").ignore(CPath("a/b/c/d/8z"))
        )

        self.assertTrue(
            FsIgnorer("a/**/z").ignore(CPath("a/z"))
        )

        self.assertFalse(
            FsIgnorer("a/**/z").ignore(CPath("a/b/z/c/z"))
        )

        self.assertFalse(
            FsIgnorer("a/**/z").ignore(CPath("a/b/z/c/z"))
        )

        self.assertFalse(
            FsIgnorer("a/**/z/q/z").ignore(CPath("a/b/z/c/z"))
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
        fs_ignore = FsIgnorer("*.log\n!important.log")
        # will match
        self.assertTrue(
            fs_ignore.ignore(CPath("debug.log"))
        )
        self.assertTrue(
            fs_ignore.ignore(CPath("trace.log"))
        )
        # will not match
        self.assertFalse(
            fs_ignore.ignore(CPath("important.log"))
        )
        self.assertFalse(
            fs_ignore.ignore(CPath("logs/important.log"))
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
        fs_ignore = FsIgnorer("*.log\n!important/*.log\ntrace.*")
        self.assertTrue(
            fs_ignore.ignore(CPath("debug.log"))
        )
        self.assertTrue(
            fs_ignore.ignore(CPath("important/trace.log"))
        )
        self.assertFalse(
            fs_ignore.ignore(CPath("important/debug.log"))
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
        fs_ignore = FsIgnorer("logs/\n!logs/important.log")
        self.assertTrue(
            fs_ignore.ignore(CPath("logs/debug.log"))
        )
        self.assertTrue(
            fs_ignore.ignore(CPath("logs/important.log"))
        )
