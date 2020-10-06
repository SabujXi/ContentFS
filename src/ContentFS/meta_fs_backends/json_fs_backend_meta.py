import json
from .dict_fs_backend_meta import DictMetaFileSystemBackend


class JsonMetaFileSystemBackend(DictMetaFileSystemBackend):
    def __init__(self, json_text: str):
        self.__json_text = json_text
        cpath_tree_dict = json.loads(json_text)

        super().__init__(cpath_tree_dict)
