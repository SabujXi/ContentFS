import re
from json import dumps


class CPath:
    SPLIT_RE = re.compile(r'[/\\]+')
    @staticmethod
    def path_to_names(path_string):
        path_string = path_string.rstrip("/").rstrip("\\")
        path_string = path_string.replace("\\", "/")
        return CPath.SPLIT_RE.split(path_string)

    def __init__(self, names):
        self.__names = tuple(names)

    @property
    def name(self):
        return self.__names[-1]

    @property
    def names(self):
        return self.__names

    @property
    def path(self):
        return "/".join(self.__names)

    def is_file(self):
        raise NotImplemented()

    def is_dir(self):
        raise NotImplemented()

    def __str__(self):
        return "CPath: " + self.path

    def to_dict(self):
        return {
            'names': self.names
        }

    def to_path_dict(self):
        return {
            'path': self.path
        }

    def to_json(self):
        return dumps(self.to_dict())

    def to_path_json(self):
        return dumps(self.to_path_dict())

    def equals(self, another):
        return self.names == another.names