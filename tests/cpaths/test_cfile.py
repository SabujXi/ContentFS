from unittest import TestCase
from ContentFS.cpaths.cfile import CFile, CPath
from ContentFS.exceptions import CFSExceptionInvalidPathName


class TestCFile(TestCase):
    def test_init_empty_file_path(self):
        cfile_creation = lambda: CFile("", 1, 1)
        self.assertRaises(CFSExceptionInvalidPathName, cfile_creation)

    def test_init_without_size_mtime(self):
        self.assertRaises(TypeError, lambda: CFile("a.txt"))

    def test_is_file(self):
        cpath = CPath('/a')
        cfile = CFile('/a', 1, 1)
        self.assertEqual(cpath.is_file(), cfile.is_file())

    def test_is_dir(self):
        cpath = CPath('/a/')
        cfile = CFile('/a/', 1, 1)
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
        self.assertTrue(cfile1.equals_by_path(cfile2))

    def test_equals_by_size(self):
        cfile1 = CFile('a', 2, 3)
        cfile2 = CFile('a', 2, 3)
        self.assertTrue(cfile1.equals_by_size(cfile2))

    def test_equals_by_size_timestamp(self):
        cfile1 = CFile('a', 2, 3)
        cfile2 = CFile('a', 2, 3)
        self.assertTrue(cfile1.equals_by_size_timestamp(cfile2))

    def test_to_dict(self):
        cfile1 = CFile('a', 2, 3)
        self.assertEqual({
            'type': 'FILE',
            'names': ('a',),
            'path': 'a',
            'mtime': 2,
            'size': 3
        }, cfile1.to_dict())
