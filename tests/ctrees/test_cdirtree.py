from unittest import TestCase
from ContentFS.ctrees.cdirtree import CDirTree
from ContentFS.cpaths.cdir import CDir
from ContentFS.cpaths.cpath import CPath


class TestCDirTree(TestCase):
    def test_is_sub(self):
        tree1 = CDirTree("")
        self.assertFalse(tree1.is_sub())

        tree2 = CDirTree("")
        subtree = tree2.add(CDir("a/b/c"))
        self.assertTrue(subtree.is_sub())
        "Let's check if the rule of the universe still holds"
        self.assertEqual(('a', 'b', 'c'), subtree.names)

    def test_as_cdir(self):
        tree1 = CDirTree("")
        self.assertIsInstance(tree1, CDir)
        self.assertIs(tree1.as_cdir.__class__, CDir)
        self.assertEqual(tuple(), tree1.names)

        tree2 = CDirTree("a/b/c")
        etree = tree2.add(CDir('a/b/c/d/e'))
        self.assertEqual(('a', 'b', 'c', 'd', 'e'), etree.names)

    def test_is_empty(self):
        tree1 = CDirTree("")
        self.assertTrue(tree1.is_empty)

    def test_add(self):
        tree1 = CDirTree("a/b/c")
        etree = tree1.add(CDir('a/b/c/d/e'))
        self.assertEqual(etree.path, 'a/b/c/d/e/')

        ddir = tree1.get(CPath("a/b/c/d/"))
        self.assertEqual(('a', 'b', 'c', 'd'), ddir.names)

        ddir2 = tree1.get(CPath("a/b/c/d"))
        self.assertIsNone(ddir2)

    def test_get(self):
        tree1 = CDirTree("a/b/c")
        ftree = tree1.add(CDir('a/b/c/d/e/f'))
        self.assertEqual(('a', 'b', 'c', 'd', 'e', 'f'), ftree.names)
        ddir = tree1.get(CPath('a/b/c/d/'))
        self.assertEqual('a/b/c/d/', ddir.path)

    def test_exists(self):
        tree1 = CDirTree("a/b/c")
        ftree = tree1.add(CDir('a/b/c/d/e/f'))

        # Notice this FALSE
        self.assertFalse(tree1.exists(('a', 'b')))
        self.assertTrue(tree1.exists(('d', )))

    def test_visit(self):
        self.fail()

    def test_get_children(self):
        self.fail()

    def test_get_children_cpaths(self):
        self.fail()

    def test_get_descendant_cpaths(self):
        self.fail()

    def test_diff(self):
        self.fail()

    def test_to_dict(self):
        self.fail()

    def test_equals(self):
        self.fail()


class TestCDirTreeDiff(TestCase):
    def test_deleted(self):
        self.fail()

    def test_modified(self):
        self.fail()

    def test_new(self):
        self.fail()

    def test_changed(self):
        self.fail()

    def test_to_dict(self):
        self.fail()
