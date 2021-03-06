from unittest import TestCase
from ContentFS.cpaths.cpath import CPath
from tests.utilities import get_data_dir
from ContentFS.exceptions import CFSException, CFSExceptionInvalidPathName


class TestCPath(TestCase):
    def test_path_to_names__windows_drive(self):
        self.skipTest("Will have to write later")  # TODO: win drive letter: c:\\xyz

    def test_path_to_names__file_uri(self):
        self.skipTest("Will have to write later")  # TODO: file://host/xyz. file:///c:/abc

    def test_path_to_names__fs_root_path_name(self):
        path1 = "/"
        comp_info = CPath.to_path_comps_info(path1)
        self.assertEqual(tuple([]), comp_info.names)
        self.assertTrue(comp_info.drive == '/')

    def test_path_to_names__empty_path_string(self):
        path1 = ""
        self.assertEqual(tuple(), CPath.to_path_comps_info(path1).names)

    def test_path_to_names__spaces_only_path_string(self):
        path2 = "                      \n    "
        self.assertRaises(CFSExceptionInvalidPathName, lambda: CPath.to_path_comps_info(path2))

    def test_path_to_names(self):
        path = "\\firstdir/seconddir/thirdfile"
        comps_info = CPath.to_path_comps_info(path)
        names = comps_info.names
        self.assertEqual(('firstdir', 'seconddir', 'thirdfile'), names)  # TODO: should this be changed to tuple from list?
        self.assertEqual(comps_info.drive, '/')

        path_2 = r"firstdir\seconddir/thirdfile"
        names_2 = CPath.to_path_comps_info(path_2).names
        self.assertEqual(('firstdir', 'seconddir', 'thirdfile'), names_2)

        path_3 = r"firstdir\\\seconddir\thirdfile/"
        names_3 = CPath.to_path_comps_info(path_3).names
        self.assertEqual(('firstdir', 'seconddir', 'thirdfile'), names_3)

        path_4 = "/firstdir/seconddir/thirdfile/"
        names_4 = CPath.to_path_comps_info(path_4).names
        self.assertEqual(('firstdir', 'seconddir', 'thirdfile'), names_4)

    def test_path_to_names__linux_root(self):
        path = '/'
        comps_info = CPath.to_path_comps_info(path)
        names = comps_info.names
        self.assertSequenceEqual([], names)
        self.assertTrue(comps_info.drive == '/')

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

    def test_is_dir__empty_path_string__is_dir(self):
        cpath = CPath("")
        self.assertTrue(cpath.is_dir())
        self.assertEqual(tuple([]), cpath.names)

    def test_get_type(self):
        self.assertEqual('DIR', CPath("/").get_type_str())
        self.assertEqual('FILE', CPath("/a").get_type_str())

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

    def test_equals_by_path(self):
        self.assertTrue(CPath("a/b//c").equals_by_path_only(CPath(r"a/b\c")))

    def test_equals_abs_rel(self):
        cpath1 = CPath('a/b')
        cpath2 = CPath('/a/b')

        self.assertFalse(cpath1.equals(cpath2))

    def test_is_abs(self):
        cpath = CPath('/')
        self.assertTrue(cpath.is_abs)
