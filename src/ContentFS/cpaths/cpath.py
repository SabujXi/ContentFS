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
        """
        names can be string/byte path or list/tuple of string/byte paths.
        :param names:
        """
        _names = []
        # when a string of path instead of an iterable of names is provided.
        # or when byte string is provided
        if isinstance(names, (str, bytes)):
            _names = self.path_to_names(names)
        # when an iterable of path component strings is provided
        # but as those strings might have slashes between then
        elif isinstance(names, (list, tuple)):
            for name in names:
                assert isinstance(name, (str, bytes))
                _names.extend(_name for _name in self.path_to_names(name) if _name)
        self.__names = tuple(_names)

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
