from unittest import TestCase
from ContentFS.cpaths import CPathType, CFile, CPath, CDir
from ContentFS.exceptions import CFSExceptionInvalidPathName


class TestCFile(TestCase):
    def test_init_empty_file_path(self):
        cfile_creation = lambda: CFile("", 1, 1)
        self.assertRaises(CFSExceptionInvalidPathName, cfile_creation)

    def test_init_by_cdir(self):
        cdir = CDir("a")
        self.assertRaises(CFSExceptionInvalidPathName, lambda: CFile(cdir, 1, 1))

    def test_path_with_slash_at_the_end(self):
        self.assertRaises(CFSExceptionInvalidPathName, lambda: CFile("a/v/", 1, 1))

    def test_init_without_size_mtime(self):
        self.assertRaises(TypeError, lambda: CFile("a.txt"))

    def test_get_type(self):
        cpath = CPath("a/v")
        self.assertEqual(cpath.get_type(), CPathType.FILE)
        cfile = CFile("a/v", 1, 1)
        self.assertEqual(cfile.get_type(), CPathType.FILE)

    def test_is_file(self):
        cpath = CPath('/a')
        cfile = CFile('/a', 1, 1)
        self.assertEqual(cpath.is_file(), cfile.is_file())

    def test_is_dir(self):
        cpath = CPath('/a/')
        cfile = CFile('/a', 1, 1)
        self.assertNotEqual(cpath.is_dir(), cfile.is_dir())

    def test_equals(self):
        cfile1 = CFile('a', 2, 3)
        cfile2 = CFile('a', 2, 3)
        self.assertTrue(cfile1.equals(cfile2))

    def test_equals_by_path(self):
        cfile1 = CFile('a', 2, 3)
        cfile2 = CFile('a', 4, 6)
        # NOT Equal
        self.assertFalse(cfile1.equals(cfile2))
        # But equal by path
        self.assertTrue(cfile1.equals_by_path_only(cfile2))

    def test_equals_by_size(self):
        cfile1 = CFile('a', 2, 3)
        cfile2 = CFile('a', 2, 3)
        self.assertTrue(cfile1.equals_with_size(cfile2))

    def test_equals_by_size_timestamp(self):
        cfile1 = CFile('a', 2, 3)
        cfile2 = CFile('a', 2, 3)
        self.assertTrue(cfile1.equals_with_size_timestamp(cfile2))

    def test_to_dict(self):
        cfile1 = CFile('a', 2, 3)
        self.assertEqual({
            'type': 'FILE',
            'names': ('a',),
            'path': 'a',
            'mtime': 2,
            'size': 3
        }, cfile1.to_dict())
