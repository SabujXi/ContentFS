from unittest import TestCase
from ContentFS.cpaths import CPathType, CPath, CDir, CFile
from ContentFS.exceptions import CFSExceptionInvalidPathName


class TestCDir(TestCase):
    def test_init_by_cfile(self):
        cfile = CFile("a", 1, 2)
        self.assertRaises(CFSExceptionInvalidPathName, lambda: CDir(cfile))

    def test_is_file(self):
        self.assertFalse(CDir('').is_file())

    def test_is_dir(self):
        self.assertTrue(CDir('').is_dir())

    def test_get_type(self):
        cpath = CPath("a/")
        cdir = CDir("a")
        self.assertEqual(cpath.get_type(), cdir.get_type())

    def test_to_dict(self):
        cdir = CDir('')
        self.assertEqual(
            {
                'names': tuple(),
                'path': '',
                'type': 'DIR'
            },
            cdir.to_dict()
        )

    def test_equals(self):
        cdir1 = CDir('a/b')
        cdir2 = CDir('a/b/')

        self.assertTrue(cdir1.equals(cdir2))

    def test_equals_by_path(self):
        cdir1 = CDir('a/b')
        cdir2 = CDir('a/b/')

        self.assertTrue(cdir1.equals_by_path_only(cdir2))

    def test_equals_abs_rel(self):
        cdir1 = CDir('a/b')
        cdir2 = CDir('/a/b')

        self.assertFalse(cdir1.equals(cdir2))
