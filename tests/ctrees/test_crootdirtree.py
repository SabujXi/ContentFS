from unittest import TestCase
from ContentFS.ctrees.crootdirtree import CRootDirTree
from ContentFS.cpaths.cpath import CPath
from ContentFS.cpaths.cfile import CFile
from ContentFS.cpaths.cdir import CDir
import json


class TestCRootDirTree(TestCase):
    def test_base_path(self):
        self.fail()

    def test_load(self):
        self.fail()

    def test_to_dict(self):
        self.fail()

    def test_to_list(self):
        self.fail()

    def test_to_json(self):
        self.fail()

    def test__should_include(self):
        tree = CRootDirTree("/abc").with_dev_matcher()
        self.assertFalse(tree._should_include(CPath(".git/")))
        self.assertFalse(tree._should_include(CPath(".git/a.txt")))
        self.assertTrue(tree._should_include(CPath(".gitt/")))
        # print(" ====" + CPath("").path + "+")

    def test_to_dict_to_json_equal(self):
        tree = CRootDirTree("anything")
        tree.add(CFile("a path", 1, 23))
        tree.add(CDir("b path/"))

        tree_dict = json.loads(json.dumps( tree.to_dict() ))  # for converting tuples into list inside

        self.assertEqual(tree_dict, json.loads(tree.to_json()))
