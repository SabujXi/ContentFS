from unittest import TestCase
from ContentFS.cpaths.cpath import CPath
from tests.utils import get_data_dir


class TestCPath(TestCase):
    def test_path_to_names(self):
        path = "/firstdir/seconddir/thirdfile"
        names = CPath.path_to_names(path)
        self.assertEqual(['', 'firstdir', 'seconddir', 'thirdfile'], names)  # TODO: should this be changed to tuple from list?

        path_2 = r"firstdir\seconddir/thirdfile"
        names_2 = CPath.path_to_names(path_2)
        self.assertEqual(['firstdir', 'seconddir', 'thirdfile'], names_2)

        path_3 = r"firstdir\\\seconddir\thirdfile/"
        names_3 = CPath.path_to_names(path_3)
        self.assertEqual(['firstdir', 'seconddir', 'thirdfile'], names_3)

        path_4 = "/firstdir/seconddir/thirdfile/"
        names_4 = CPath.path_to_names(path_4)
        self.assertEqual(['', 'firstdir', 'seconddir', 'thirdfile'], names_4)

    def test_name(self):
        path = "firstdir/seconddir/thirdfile/"
        cpath = CPath(path)
        self.assertEqual('thirdfile', cpath.name)

    def test_names(self):
        path_1 = "firstdir/seconddir/thirdfile"
        cpath_1 = CPath(path_1)
        self.assertEqual(('firstdir', 'seconddir', 'thirdfile'), cpath_1.names)

        path_2 = "firstdir/seconddir/thirdfile"
        cpath_2 = CPath(path_2)
        self.assertEqual(('firstdir', 'seconddir', 'thirdfile'), cpath_2.names)
        self.assertNotEqual(('', 'firstdir', 'seconddir', 'thirdfile'), cpath_2.names)

    def test_path(self):
        path_1 = "firstdir/seconddir/thirdfile"
        cpath_1 = CPath(path_1)
        self.assertEqual('firstdir/seconddir/thirdfile', cpath_1.path)

        path_2 = "/firstdir/seconddir/thirdfile"
        cpath_2 = CPath(path_2)
        self.assertEqual('/firstdir/seconddir/thirdfile', cpath_2.path)
        self.assertNotEqual('firstdir/seconddir/thirdfile', cpath_2.path)

        path_3 = "/firstdir/seconddir/thirdfile/"
        cpath_3 = CPath(path_3)
        self.assertEqual('/firstdir/seconddir/thirdfile/', cpath_3.path)

    def test_is_file(self):
        self.assertFalse(CPath("/firstdir/seconddir/thirdfile/").is_file())
        self.assertTrue(CPath("/firstdir/seconddir/thirdfile").is_file())
        self.assertTrue(CPath("firstdir/seconddir/thirdfile").is_file())

    def test_is_dir(self):
        self.assertTrue(CPath("/firstdir/seconddir/thirdfile/").is_dir())
        self.assertTrue(CPath("firstdir/seconddir/thirdfile/").is_dir())

        self.assertTrue(CPath("/").is_dir())

    def test_get_type(self):
        self.assertEqual('DIR', CPath("/").get_type())
        self.assertEqual('FILE', CPath("/a").get_type())

    def test_to_dict(self):
        path_1 = r"firstdir/seconddir\\\thirdfile"
        cpath_1 = CPath(path_1)
        self.assertEqual({
            'names': ('firstdir', 'seconddir', 'thirdfile'),
            'type': 'FILE',
            'path': 'firstdir/seconddir/thirdfile'
        }, cpath_1.to_dict())

    def test_equals(self):
        self.assertTrue(CPath("a/b//c").equals(CPath(r"a/b\c")))
