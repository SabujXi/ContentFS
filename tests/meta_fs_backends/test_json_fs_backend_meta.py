from unittest import TestCase
from ContentFS.meta_fs_backends.dict_fs_backend_meta import DictMetaFileSystemBackend
from ContentFS.meta_fs_backends.json_fs_backend_meta import JsonMetaFileSystemBackend
from tests.meta_fs_backends.serialized_data import fs_dict, fs_json
import json


class TestJsonMetaFileSystemBackend(TestCase):
    def test_init(self):
        dict_fs = DictMetaFileSystemBackend(fs_dict)

        json_fs = JsonMetaFileSystemBackend(fs_json)

        # does dict meta fs contain the same as the serialized dict.
        fs_dict_list = json.loads(json.dumps(fs_dict['cpaths']))  # list tuple inconsistency fix
        get_list = json.loads(json.dumps(dict_fs._get_dict_list()))
        self.assertEqual(fs_dict_list, get_list)

        # does dict fs & json fs dict contain the same list of cpaths
        self.assertEqual(json.loads(json.dumps(json_fs._get_dict_list())), json.loads(json.dumps(dict_fs._get_dict_list())))
