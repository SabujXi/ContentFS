from unittest import TestCase
from .serialized_data import fs_dict
from ContentFS.meta_fs_backends.dict_fs_backend_meta import DictMetaFileSystemBackend


class TestDictMetaFileSystemBackend(TestCase):
    def setUp(self) -> None:
        self.dict_fs = DictMetaFileSystemBackend(fs_dict)

    def test_exists(self):
        self.dict_fs.exists()

    def test_is_file(self):
        self.fail()

    def test_is_dir(self):
        self.fail()

    def test_listdir(self):
        self.fail()

    def test_getmtime(self):
        self.fail()

    def test_getsize(self):
        self.fail()

    def test_gethash(self):
        self.fail()

    def test_is_real_fs(self):
        self.fail()


class Test_visit_dict_fs(TestCase):
    def test_visit_dict_fs(self):
        self.fail()
