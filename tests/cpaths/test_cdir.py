from unittest import TestCase
from ContentFS.cpaths.cdir import CDir


class TestCDir(TestCase):
    def test_is_file(self):
        self.assertFalse(CDir('').is_file())

    def test_is_dir(self):
        self.assertTrue(CDir('').is_dir())

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
