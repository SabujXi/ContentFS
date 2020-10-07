from unittest import TestCase
from ContentFS.cpaths import CPath, CDir, CFile
from ContentFS.utils import CPathUtils
from ContentFS.exceptions import CFSException


class TestCPathUtils(TestCase):
    def test_is_ancestor(self):
        # root dir root cannot play ancestor
        self.assertFalse(CPathUtils.is_ancestor(CDir(""), CDir("")))
        # ancestor must be dir
        self.assertRaises(CFSException, lambda: CPathUtils.is_ancestor(CPath("a"), CPath("a/b/c/d")))  # TODO: create proper exception
        self.assertRaises(CFSException, lambda: CPathUtils.is_ancestor(CFile("a", 1, 2), CPath("a/b/c/d")))
        # a dir is ancestor
        self.assertTrue(CPathUtils.is_ancestor(CPath("a/"), CPath("a/b/c/d")))
        # parent is also an ancestor
        self.assertTrue(CPathUtils.is_ancestor(CPath("a/b/c/"), CPath("a/b/c/d")))
        # not ancestor
        self.assertFalse(CPathUtils.is_ancestor(CDir("a/b"), CFile("x/y", 1, 1)))

    def test_is_parent(self):
        # root dir root cannot play parent child
        self.assertFalse(CPathUtils.is_parent(CDir(""), CDir("")))
        # parent must be dir
        self.assertRaises(CFSException, lambda: CPathUtils.is_parent(CPath("a"), CPath("a/b")))
        self.assertRaises(CFSException, lambda: CPathUtils.is_parent(CFile("a", 1, 2), CPath("a/b/")))
        # a dir is parent
        self.assertTrue(CPathUtils.is_parent(CPath("a/"), CPath("a/b")))
        self.assertTrue(CPathUtils.is_parent(CPath("a/b/"), CPath("a/b/c.txt")))
        # not parent
        self.assertFalse(CPathUtils.is_ancestor(CDir("a/b"), CFile("x/y", 1, 1)))

