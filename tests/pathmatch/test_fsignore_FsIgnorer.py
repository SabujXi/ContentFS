from unittest import TestCase
from ContentFS.pathmatch.fsignore import FsIgnorer
from ContentFS.cpaths.cpath import CPath


class TestFsIgnorer(TestCase):
    def test_ignore(self):
        self.assertTrue(
            FsIgnorer("a")
                .ignore(CPath("a"))
        )
        self.assertTrue(
            FsIgnorer("a")
                .ignore(CPath("a/"))
        )
        self.assertFalse(
            FsIgnorer("a/")
                .ignore(CPath("a"))
        )

        self.assertTrue(
            FsIgnorer("a/*/z")
                .ignore(CPath("a/b/z"))
        )

        self.assertFalse(
            FsIgnorer("a/[!0-8]z")
                .ignore(CPath("a/8z"))
        )

        self.assertTrue(
            FsIgnorer("a/[!0-8]z")
                .ignore(CPath("a/9z"))
        )

        self.assertFalse(
            FsIgnorer("a/[!0-8]z")
                .ignore(CPath("a/09z"))
        )

        self.assertTrue(
            FsIgnorer("m/**")
                .ignore(CPath("m/n/o9z"))
        )

        self.assertTrue(
            FsIgnorer("a/**/z")
                .ignore(CPath("a/b/c/d/z"))
        )

        self.assertTrue(
            FsIgnorer("a/**/[!0-8]z")
                .ignore(CPath("a/b/c/d/9z"))
        )

        self.assertFalse(
            FsIgnorer("a/**/[!0-8]z")
                .ignore(CPath("a/b/c/d/8z"))
        )

        self.assertTrue(
            FsIgnorer("a/**/z")
                .ignore(CPath("a/z"))
        )

        self.assertFalse(
            FsIgnorer("a/**/z")
                .ignore(CPath("a/b/z/c/z"))
        )

        self.assertFalse(
            FsIgnorer("a/**/z")
                .ignore(CPath("a/b/z/c/z"))
        )

        self.assertFalse(
            FsIgnorer("a/**/z/q/z")
                .ignore(CPath("a/b/z/c/z"))
        )
