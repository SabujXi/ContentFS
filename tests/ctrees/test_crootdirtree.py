from unittest import TestCase
from ContentFS.ctrees.crootdirtree import CRootDirTree
from ContentFS.cpaths.cpath import CPath


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
