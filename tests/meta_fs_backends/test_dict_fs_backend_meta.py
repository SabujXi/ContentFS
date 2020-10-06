from unittest import TestCase
from tests.meta_fs_backends.serialized_data import fs_dict
from ContentFS.meta_fs_backends.dict_fs_backend_meta import DictMetaFileSystemBackend
from ContentFS.cpaths.cpath import CPath
from ContentFS.cpaths.cdir import CDir
from ContentFS.cpaths.cfile import CFile
from ContentFS.exceptions import CFSPathDoesNotExistException


class TestDictMetaFileSystemBackend(TestCase):
    def setUp(self) -> None:
        self.dict_fs = DictMetaFileSystemBackend(fs_dict)

    def test_exists(self):
        self.assertTrue(self.dict_fs.exists(CDir("a/")))
        self.assertTrue(self.dict_fs.exists(CPath("adir/")))
        self.assertTrue(self.dict_fs.exists(CDir("dir with children")))
        self.assertTrue(self.dict_fs.exists(CDir("dir with children/empty_nested_dir")))
        self.assertTrue(self.dict_fs.exists(CDir("dir with children/nested dir with children")))
        self.assertTrue(self.dict_fs.exists(CDir("dir with children/nested dir with children/secrets")))
        self.assertTrue(self.dict_fs.exists(CDir("dir with children/nested dir with children/secrets/no secret")))
        self.assertTrue(self.dict_fs.exists(CFile("dir with children/nested dir with children/secrets/no secret/plain file", 1, 1)))
        self.assertTrue(self.dict_fs.exists(CFile("dir with children/nested dir with children/secrets/secret.txt", 1, 1)))
        self.assertTrue(self.dict_fs.exists(CFile("dir with children/x.txt", 1, 1)))
        self.assertTrue(self.dict_fs.exists(CDir("dir with files only")))
        self.assertTrue(self.dict_fs.exists(CPath("dir with files only/a.txt")))
        self.assertTrue(self.dict_fs.exists(CPath("empty_dir/")))
        self.assertTrue(self.dict_fs.exists(CPath("a.txt")))

        # not exists
        self.assertFalse(self.dict_fs.exists(CPath("readme.txt")))

    def test_exists__path_type_independent(self):
        """Does not care what you pass, cdir or cfile - it does not check the type of the path"""
        # two versions should work as exists do not depend on the type of the path.
        self.assertTrue(self.dict_fs.exists(CPath("empty_dir")))
        self.assertTrue(self.dict_fs.exists(CPath("empty_dir/")))

    def test_is_file(self):
        self.dict_fs.is_file(CPath("a.txt"))

        # does not exist file
        self.assertRaises(CFSPathDoesNotExistException, lambda: self.dict_fs.is_file(CPath("doesnotexist")))

        self.assertTrue(CPath("a"))

    def test_is_dir(self):
        self.assertTrue(self.dict_fs.is_dir(CPath("empty_dir")))

    def test_listdir(self):
        self.assertEqual(
            {'adir', 'empty_dir', 'dir with files only', 'a', 'dir with children', 'a.txt'},
            set(self.dict_fs.listdir(CPath("")))
        )

    def test_getmtime(self):
        self.skipTest("Will write test later")  # TODO: complete writing test

    def test_getsize(self):
        self.skipTest("Will write test later")  # TODO: complete writing test

    def test_gethash(self):
        self.skipTest("Will write test later")  # TODO: complete writing test

    def test_is_real_fs(self):
        self.assertFalse(self.dict_fs.is_real_fs())


class Test_visit_dict_fs(TestCase):
    def test_visit_dict_fs(self):
        self.skipTest("Will write test later")  # TODO: complete writing test
