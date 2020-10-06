from unittest import TestCase
from ContentFS.ctrees.cdirtree import CDirTreeDiff, CDirTree
from ContentFS.cpaths import CPath, CFile, CDir


class TestCDirTreeDiff(TestCase):
    def setUp(self) -> None:
        root_tree1 = CDirTree()
        root_tree1.add(CFile("d1/a.txt", 1, 2))
        root_tree1.add(CDir("d2/"))
        root_tree1.add(CDir("d3/p/q/r"))
        root_tree1.add(CFile("d3/p/x.txt", 1, 5))

        root_tree2 = CDirTree()
        root_tree2.add(CFile("d1/a.txt", 1, 2))
        # root_tree2.add(CDir("dir2/"))  - deleted
        root_tree2.add(CDir("d3/p/q/r"))
        root_tree2.add(CFile("d3/p/x.txt", 1, 5))
        root_tree2.add(CFile("d3/p/y.txt", 1, 5))  # new

        # TODO: test in real file system too, with hash

        self.root_tree1 = root_tree1
        self.root_tree2 = root_tree2

        self.diff = self.root_tree1.diff(root_tree2)

    def test_deleted(self):
        self.assertIsNotNone(self.diff.deleted.get(CPath("d2")))

    def test_modified(self):
        self.assertEqual(0, len(self.diff.modified.get_descendant_cpaths()))

    def test_new(self):
        self.assertEqual(1, len(self.diff.new.get_leaves()))
        self.assertIsNotNone(self.diff.new.get(CPath("d3/p/y.txt")))

    def test_changed(self):
        self.assertTrue(self.diff.changed())

    def test_to_dict(self):
        self.skipTest("Will test after completing more critical ones")  # TODO: write test
