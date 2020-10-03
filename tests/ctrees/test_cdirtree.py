from unittest import TestCase
from typing import Union
from ContentFS.ctrees.cdirtree import CDirTree
from ContentFS.cpaths.cdir import CDir
from ContentFS.cpaths.cfile import CFile
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
        root_tree = CDirTree()
        root_tree.add(CFile("dir1/a.txt", 1, 2))
        root_tree.add(CDir("dir2/"))
        root_tree.add(CDir("dir3/p/q/r"))
        root_tree.add(CFile("dir3/p/x.txt", 1, 5))

        # dir2 is a leaf dir
        dir2_is_leaf: Union[bool, None] = None

        def visitor_1(cpath, is_leaf, tree):
            nonlocal dir2_is_leaf
            if cpath.equals_by_path(CPath("dir2/")):
                dir2_is_leaf = is_leaf

        root_tree.visit(visitor_1)
        self.assertTrue(dir2_is_leaf)

        #  non depth first visit, the first cpath is dir1
        paths_2 = []

        def visitor_2(cpath, is_leaf, tree):
            nonlocal paths_2
            paths_2.append(cpath)

        root_tree.visit(visitor_2, False)
        self.assertTrue(paths_2[0].equals(CDir("dir1/")))

        # non depth first visit, the last path is
        # print(paths[-1].to_dict())
        self.assertTrue(paths_2[-1].equals(CFile("dir3/p/x.txt", 1, 5)))

        # depth first visit, the first cpath is dir1/a.txt
        paths_3 = []

        def visitor_3(cpath, is_leaf, tree):
            nonlocal paths_3
            paths_3.append(cpath)

        root_tree.visit(visitor_3, True)

        self.assertTrue(paths_3[0].equals(CFile("dir1/a.txt", 1, 2)))

        # length of paths
        paths_4 = []

        def visitor_4(cpath, is_leaf, tree):
            nonlocal paths_4
            paths_4.append(cpath)

        root_tree.visit(visitor_4, False)
        """
        Before bug fix:
            dir1/a.txt
            dir1/
            dir2/
            dir3/p/q/r/
            dir3/p/q/
            dir3/p/
            dir3/
            dir3/p/x.txt
            dir3/p/
        
        Count: 9, instead of 8
            
        dir3/p/  occurred two times due to having a file inside it and sub dir 
        """

        self.assertEqual(8, len(paths_4))

        self.assertEqual(
            {
                "dir1/",
                "dir1/a.txt",
                "dir2/",
                "dir3/p/",
                "dir3/p/x.txt",
                "dir3/p/q/",
                "dir3/p/q/r/",
                "dir3/"
            },
            set(cpath.path for cpath in paths_4)
        )

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
