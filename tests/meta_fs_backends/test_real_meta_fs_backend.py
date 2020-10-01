from unittest import TestCase
from ContentFS.meta_fs_backends.real_fs_backend_meta import RealMetaFileSystemBackend
from ContentFS.cpaths.cpath import CPath
from tests.utils import get_data_dir, join_base
import os


class TestRealMetaFileSystemBackend(TestCase):
    def setUp(self) -> None:
        self.this_test_dir_name = "real_fs_test_data"
        self.file_1_name = f"{self.this_test_dir_name}/test_file_for_hash"
        self.file_1_sha1_hash = "A053DC84FE753C3E9187B97923F7A57BB7F44299"
        self.file_1_cpath = CPath(self.file_1_name)
        self.real_fs = RealMetaFileSystemBackend().set_base_path(get_data_dir())

    def test_exists(self):
        cpath_1 = CPath(f"{self.this_test_dir_name}/subdir/afile")
        cpath_2 = CPath(f"{self.this_test_dir_name}/file-does-not-exists")
        self.assertTrue(self.real_fs.exists(cpath_1))
        self.assertFalse(self.real_fs.exists(cpath_2))

    def test_is_file(self):
        cpath = CPath(f"{self.this_test_dir_name}/subdir/afile")
        fs_is_file = self.real_fs.is_file(cpath)
        self.assertTrue(fs_is_file)

    def test_is_dir(self):
        cpath = CPath(f"{self.this_test_dir_name}/subdir")
        fs_is_dir = self.real_fs.is_dir(cpath)
        self.assertTrue(fs_is_dir)

    def test_listdir(self):
        os_dir_list = os.listdir(join_base(self.this_test_dir_name))
        fs_dir_list = self.real_fs.listdir(CPath(self.this_test_dir_name))
        self.assertEqual(os_dir_list, fs_dir_list)

    def test_getmtime(self):
        os_mtime = os.path.getmtime(join_base(self.file_1_name))
        self.assertEqual(os_mtime, self.real_fs.getmtime(self.file_1_cpath))

    def test_getsize(self):
        os_size = os.path.getsize(join_base(self.file_1_name))
        self.assertEqual(os_size, self.real_fs.getsize(self.file_1_cpath))

    def test_gethash(self):
        self.assertNotEqual(self.file_1_sha1_hash, self.real_fs.gethash(self.file_1_cpath))
        self.assertEqual(self.file_1_sha1_hash.lower(), self.real_fs.gethash(self.file_1_cpath))
