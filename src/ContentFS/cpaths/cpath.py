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

        # check whether it is a dir or file looking at the end of the `names`
        self.__is_dir = False
        if len(self.__names) == 0:
            self.__is_dir = True
        else:
            end_char = None
            if isinstance(names, (str, bytes)):
                end_char = names[-1]
            else:
                end_char = names[-1][-1]
            if end_char in ("\\", "/"):
                self.__is_dir = True
        # cached results
        self.__cached_path = None

    @property
    def name(self):
        return self.__names[-1]

    @property
    def names(self):
        return self.__names

    @property
    def path(self):
        if self.__cached_path is None:
            self.__cached_path = "/".join(self.__names) + '' if self.is_file() else '/'
        return self.__cached_path

    def is_file(self):
        return not self.__is_dir

    def is_dir(self):
        return self.__is_dir

    def get_type(self) -> str:
        return 'FILE' if self.is_file() else 'DIR'

    def __str__(self):
        return "CPath: " + self.path

    def to_dict(self):
        dct = {
            'names': self.names,
            'type': self.get_type()
        }
        return dct

    def to_path_dict(self):
        return {
            'path': self.path,
            'type': self.get_type()
        }

    def to_json(self):
        return dumps(self.to_dict())

    def to_path_json(self):
        return dumps(self.to_path_dict())

    def equals(self, another):
        return self.names == another.names
