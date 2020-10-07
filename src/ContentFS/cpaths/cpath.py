import re
import enum
from json import dumps
from typing import Union, List, Tuple
from ContentFS.exceptions import CFSException, CFSExceptionInvalidPathName


class CPathType(enum.Enum):
    DIR = 'DIR'
    FILE = 'FILE'

    def __str__(self):
        return f'CPathType.{self.name}'

    def __repr__(self):
        return self.__str__()


class CPathInfo:
    """Should consider this as read only and use such. Only to_path_info() should return it's instance."""
    def __init__(self, names: List[str], first_char: str, last_char: str):
        self.names = names
        self.names_count = len(names)
        self.first_char = first_char
        self.last_char = last_char


class CPathComponentsInfo:
    def __init__(self, first_char, components, last_char):
        self.first_char = first_char
        self.components = components
        self.last_char = last_char


class CPath:
    SPLIT_RE = re.compile(r'[/\\]+')
    WIN_PATH_DRIVE_PATTERN = re.compile(r'^[a-z]:$', re.IGNORECASE)
    SPACE_ONLY_PATH_RE = re.compile(r'^[ \t\n\r]+$')  # spaces

    @staticmethod
    def to_path_comps_info(path_or_comp_string: str) -> CPathComponentsInfo:
        """
        Full path string or path comp (from array) to Components Info

        * It doesn't check whether this contains white spaces at the beginning or at the end.
          It assumes that such invalid stuff will not be passed to it.
        """
        first_char = ''
        last_char = ''
        components = []

        if path_or_comp_string == "":
            return CPathComponentsInfo('', [], '')

        if CPath.SPACE_ONLY_PATH_RE.match(path_or_comp_string):
            raise CFSExceptionInvalidPathName(f"Path string provided  `{path_or_comp_string}` - that is empty or contains only spaces")

        path_or_comp_string = path_or_comp_string.replace("\\", "/")

        if len(path_or_comp_string) > 0:
            first_char = path_or_comp_string[0]
            last_char = path_or_comp_string[-1]

        cleaned_path_string = path_or_comp_string.strip("/")
        # for '/' -> '' thus spliting that path results in one [''] instead of ['', '']
        # re.split('/', '//')
        # -> ['', '', ''] with r stripping it becomes ['']
        # re.split('/', '//') -> ['', 'a']

        components.extend(CPath.SPLIT_RE.split(cleaned_path_string))

        return CPathComponentsInfo(first_char, components, last_char)

    @staticmethod
    def to_cpath_info(path: Union[str, bytes, List[str], Tuple[str, ...]]) -> CPathInfo:
        # TODO: unittest -_- (should write unittest first)
        """
        Will linerize name components or iterable.
        """
        _names: List[str] = []
        _first_char: str = ''  # None
        _last_char: str = ''  # None
        # when a string of path instead of an iterable of names is provided.
        #   or when byte string is provided
        if isinstance(path, (str, bytes)):
            comps_info = CPath.to_path_comps_info(path)
            _names = comps_info.components
            _first_char = comps_info.first_char  # str(path[0]) if len(path) > 0 else ''
            _last_char = comps_info.last_char  # str(path[-1]) if len(path) > 0 else ''
        # when an iterable of path component strings is provided
        #   but as those strings might have slashes between then
        elif isinstance(path, (list, tuple)):
            for i, name in enumerate(path):
                assert isinstance(name, (str, bytes)), f"Invalid data type of name inside names: {type(name)}"

                comps_info = CPath.to_path_comps_info(name)
                # first name
                if i == 0:
                    # take first char of only the first comp info & discard others
                    _first_char = comps_info.first_char   # str(name[0]) if len(name) > 0 else ''
                # last name
                if i == len(path) - 1:
                    # take last char of only the last comp info, discard others
                    _last_char = comps_info.last_char # str(name[-1]) if len(name) > 0 else ''

                _names.extend(comps_info.components)  # removing empty components
        else:
            raise CFSException(f"Invalid type passed: {type(path)}")

        # # exclude empty names
        # #   A good use case is when this is a tree-root path it will be empty string as path and we don't keep that.
        # #   It is assumed that there is no possibility of having empty string except the only root path one where
        # #   there is only one path component and that is empty
        # _names = list(a_name for a_name in _names if a_name)

        return CPathInfo(_names, _first_char, _last_char)

    def __init__(self, names: Union['CPath', str, bytes, List[str], List[bytes], Tuple[str, ...], Tuple[bytes, ...]], is_dir=None, is_abs=None):
        """
        names can be string/byte path or list/tuple of string/byte paths.
        :param names: names of the
        """
        # ---- declarations ----
        self.__names: Tuple[str, ...]
        self.__type: CPathType
        self.__is_abs: bool
        # cached results
        self.__cached_path: Union[str, None] = None

        # ---- process names ----
        if isinstance(names, CPath):
            self.__names = names.names
            self.__type = names.get_type()
            self.__is_abs = names.is_abs

        elif isinstance(names, (str, bytes, list, tuple)):
            cpath_info = self.to_cpath_info(names)

            _names = cpath_info.names
            _first_char = cpath_info.first_char
            _last_char = cpath_info.last_char

            if len(_names) == 0:
                self.__names = tuple(_names)
                self.__type = CPathType.DIR
                self.__is_abs = True if _first_char == '/' else False
            else:
                _first_comp = _names[0]

                # calculating from path if it is absolute path or not before stripping out that data
                _is_abs_calculated = True \
                    if _first_char == '/' or self.WIN_PATH_DRIVE_PATTERN.match(_first_comp)\
                        else False

                self.__names = tuple(_names)

                # path ends with slash or not, it can be a directory. but path ends with a slash cannot be a file path.
                #   check whether it is a dir or file looking at the end of the `names`
                # self.__is_dir
                if is_dir is None:
                    if len(self.__names) == 0:  # tree root
                        self.__type = CPathType.DIR
                    else:
                        if _last_char == "/":
                            self.__type = CPathType.DIR
                        else:
                            self.__type = CPathType.FILE
                else:
                    self.__type = CPathType.DIR if is_dir else CPathType.FILE

                # self.__is_abs
                if is_abs is None:
                    self.__is_abs = _is_abs_calculated
                else:
                    assert is_abs == _is_abs_calculated, f"is_abs: {is_abs}, but calculated _is_abs_calculated: {_is_abs_calculated}"
                    self.__is_abs = is_abs
        else:
            raise CFSException(f"Invalid data type of names: {type(names)}")

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
        return self.__type is CPathType.FILE

    def is_dir(self):
        return self.__type is CPathType.DIR

    def get_type_str(self) -> str:
        return self.__type.value

    def get_type(self) -> CPathType:
        return self.__type

    def __str__(self):
        return f"CPath({self.get_type().value}): " + self.path

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        dct = {
            'names': self.names,
            'type': self.get_type_str(),
            'path': self.path
        }
        return dct

    def to_json(self):
        return dumps(self.to_dict())

    def equals(self, another):
        return self.names == another.names and self.get_type() == another.get_type() and self.is_abs == another.is_abs

    def equals_by_path(self, another: 'CPath'):
        """Equals by path only"""
        return self.path == another.path
