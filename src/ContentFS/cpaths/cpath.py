import re
from json import dumps
from typing import Union, List, Tuple


class CPath:
    SPLIT_RE = re.compile(r'[/\\]+')
    WIN_PATH_DRIVE_PATTERN = re.compile(r'^[a-z]:$', re.IGNORECASE)

    @staticmethod
    def path_to_names(path_string: str):
        """
        * It doesn't check whether this contains white spaces at the beginning or at the end.
          It assumes that such invalid stuff will not be passed to it.
        """
        path_string = path_string.rstrip("/").rstrip("\\")
        path_string = path_string.replace("\\", "/")
        # lstrip was not done
        return CPath.SPLIT_RE.split(path_string)

    def __init__(self, names: Union[str, bytes, List[str], List[bytes], Tuple[str], Tuple[bytes]], is_dir=None, is_abs=None):
        """
        names can be string/byte path or list/tuple of string/byte paths.
        :param names: names of the
        """
        assert isinstance(names, (str, bytes, list, tuple)), f"Invalid data type of names: {type(names)}"
        _names = []
        _first_char = None
        _last_char = None
        # when a string of path instead of an iterable of names is provided.
        #   or when byte string is provided
        if isinstance(names, (str, bytes)):
            _names = self.path_to_names(names)
            _first_char = str(names[0]) if len(names) > 0 else ''
            _last_char = str(names[-1]) if len(names) > 0 else ''
        # when an iterable of path component strings is provided
        #   but as those strings might have slashes between then
        elif isinstance(names, (list, tuple)):
            for i, name in enumerate(names):
                if i == 0:
                    _first_char = str(name[0]) if len(name) > 0 else ''
                if i == len(names) - 1:
                    _last_char = str(name[-1]) if len(name) > 0 else ''
                assert isinstance(name, (str, bytes)), f"Invalid data type of name inside names: {type(name)}"
                _names.extend(_name for _name in self.path_to_names(name) if _name)
        _first_comp = _names[0]

        # calculating from path if it is absolute path or not before stripping out that data
        _is_abs_calculated = True if _first_char and (_first_char in ('\\', '/') or self.WIN_PATH_DRIVE_PATTERN.match(_first_comp)) else False
        # exclude empty names
        #   A good use case is when this is a tree-root path it will be empty string as path and we don't keep that.
        #   It is assumed that there is no possibility of having empty string except the only root path one where
        #   there is only one path component and that is empty
        _names = filter(lambda name: True if name else False, _names)
        self.__names = tuple(_names)

        # path ends with slash or not, it can be a directory. but path ends with a slash cannot be a file path.
        #   check whether it is a dir or file looking at the end of the `names`
        # self.__is_dir
        if is_dir is None:
            if len(self.__names) == 0:  # tree root
                self.__is_dir = True
            else:
                self.__is_dir = False
                if _last_char in ("\\", "/"):
                    self.__is_dir = True
        else:
            self.__is_dir = is_dir

        # self.__is_abs
        if is_abs is None:
            self.__is_abs = _is_abs_calculated
        else:
            assert is_abs == _is_abs_calculated, f"is_abs: {is_abs}, but calculated _is_abs_calculated: {_is_abs_calculated}"
            self.__is_abs = is_abs
        # cached results
        self.__cached_path = None

    @property
    def is_abs(self) -> bool:
        """
        If this path absolute or relative
        """
        return self.__is_abs

    @property
    def is_rel(self) -> bool:
        return not self.is_abs

    @property
    def name(self) -> str:
        if len(self.__names) == 0:
            return ''
        return self.__names[-1]

    @property
    def names(self):
        return self.__names

    @property
    def names_count(self):
        return len(self.__names)

    @property
    def path(self):
        """
        If this is a dir then a forward slash will be prepended with the result
            EXCEPT for the root dir with zero path components.
        """
        if self.__cached_path is None:
            self.__cached_path = "/".join(self.__names)
            if self.__names:  # instead of self.__cached_path
                # without checking this introduced bug: empty string created a / for directory making that root path
                #   and misguiding os.path.join in real meta fs listing method
                self.__cached_path += '' if self.is_file() else '/'
            # for absolute path
            if self.__is_abs:
                if len(self.__names) == 0:
                    self.__cached_path = '/' + self.__cached_path
                else:
                    if not self.WIN_PATH_DRIVE_PATTERN.match(self.__names[0]):
                        # for linux path
                        self.__cached_path = '/' + self.__cached_path
                    else:
                        'For windows path nothing special is needed.'
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
            'type': self.get_type(),
            'path': self.path
        }
        return dct

    def to_json(self):
        return dumps(self.to_dict())

    def equals(self, another):
        return self.equals_by_path(another)

    def equals_by_path(self, another):
        return self.names == another.names and self.get_type() == another.get_type()
