import re
import json
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


class CPathComponentsInfo:
    def __init__(self, drive: str, names: List[str], last_char: str):
        self._drive = drive
        self._names = tuple(names)
        self._last_char = last_char

    @property
    def drive(self) -> str:
        """
        Drive letter with colon or unix root.
        """
        return self._drive

    @property
    def names(self) -> Tuple[str, ...]:
        return self._names

    @property
    def last_char(self) -> str:
        return self._last_char

    @property
    def has_drive(self) -> bool:
        return self._drive != ''

    @property
    def has_non_unix_drive(self) -> bool:
        """
        It is not necessary that it will have to be windows drive, it can be file:// drive or even network one.
        """
        return self._drive != '/'

    @property
    def has_unix_root(self) -> bool:
        return self._drive == '/'

    def to_dict(self) -> dict:
        return {
            'drive': self._drive,
            'names': self._names,
            'last_char': self._last_char
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class CPathInfo(CPathComponentsInfo):
    """Should consider this as read only and use such. Only to_path_info() should return it's instance."""
    def __init__(self, drive: str, names: List[str], last_char: str):
        super().__init__(drive, names, last_char)


class CPath:
    SPLIT_RE = re.compile(r'[/\\]+')
    DRIVE_PATH_RE = re.compile(r'^(?P<drive>[a-z]+:|/)?(?P<path>.*)')  # for extracting drive and path
    SPACE_ONLY_PATH_RE = re.compile(r'^[ \t\n\r]+$')  # spaces

    @staticmethod
    def to_path_comps_info(path_or_comp_string: str) -> CPathComponentsInfo:
        """
        Full path string or path comp (from array) to Components Info

        * It doesn't check whether this contains white spaces at the beginning or at the end.
          It assumes that such invalid stuff will not be passed to it.
        """
        last_char = ''
        components = []
        drive = ''

        if path_or_comp_string == "":
            return CPathComponentsInfo('', [], '')

        if CPath.SPACE_ONLY_PATH_RE.match(path_or_comp_string):
            raise CFSExceptionInvalidPathName(f"Path string provided  `{path_or_comp_string}` - that is empty or contains only spaces")

        path_or_comp_string = path_or_comp_string.replace("\\", "/")

        _m = CPath.DRIVE_PATH_RE.match(path_or_comp_string)
        drive = _m.group('drive') if _m.group('drive') is not None else ''
        path = _m.group('path')

        if len(path) > 0:
            last_char = path[-1]

        cleaned_path_string = path.strip("/")
        # for '/' -> '' thus spliting that path results in one [''] instead of ['', '']
        # re.split('/', '//')
        # -> ['', '', ''] with r stripping it becomes ['']
        # re.split('/', '//') -> ['', 'a']
        _comps = [comp for comp in CPath.SPLIT_RE.split(cleaned_path_string) if comp]

        components.extend(_comps)

        return CPathComponentsInfo(drive, components, last_char)

    @staticmethod
    def to_cpath_info(path: Union[str, bytes, List[str], Tuple[str, ...]]) -> CPathInfo:
        # TODO: unittest -_- (should write unittest first)
        """
        Will linerize name components or iterable.
        """
        names: Union[List[str], Tuple[str, ...]] = []
        drive: str = ''  # None
        last_char: str = ''  # None
        # when a string of path instead of an iterable of names is provided.
        #   or when byte string is provided
        if isinstance(path, (str, bytes)):
            comps_info = CPath.to_path_comps_info(path)

            names = comps_info.names
            drive = comps_info.drive  # str(path[0]) if len(path) > 0 else ''
            last_char = comps_info.last_char  # str(path[-1]) if len(path) > 0 else ''
        # when an iterable of path component strings is provided
        #   but as those strings might have slashes between then
        elif isinstance(path, (list, tuple)):
            for i, name in enumerate(path):
                assert isinstance(name, (str, bytes)), f"Invalid data type of name inside names: {type(name)}"

                comps_info = CPath.to_path_comps_info(name)
                # first name
                if i == 0:
                    # take first char of only the first comp info & discard others
                    drive = comps_info.drive
                else:
                    if comps_info.has_drive and comps_info.has_non_unix_drive:  # drive not in ['', '/']:
                        # so, that is a windows/no-unix/url/file/etc. drive and living in the middle of the components.
                        # Err.
                        raise CFSExceptionInvalidPathName(f'Path: {path} is invalid due to having a non / `drive` in the middle of the path')
                # last name
                if i == len(path) - 1:
                    # take last char of only the last comp info, discard others
                    last_char = comps_info.last_char

                names.extend(comps_info.names)
        else:
            raise CFSException(f"Invalid type passed: {type(path)}")

        # # exclude empty names
        # #   A good use case is when this is a tree-root path it will be empty string as path and we don't keep that.
        # #   It is assumed that there is no possibility of having empty string except the only root path one where
        # #   there is only one path component and that is empty
        # _names = list(a_name for a_name in _names if a_name)

        return CPathInfo(drive, names, last_char)

    def __init__(self, names: Union['CPath', str, bytes, List[str], List[bytes], Tuple[str, ...], Tuple[bytes, ...]], is_dir=None, is_abs=None):
        """
        names can be string/byte path or list/tuple of string/byte paths.
        :param names: names of the
        """
        # ---- declarations ----
        self.__cpath_info: CPathInfo
        self.__type: CPathType
        self.__is_abs: bool
        #      cached results
        self.__cached_path: Union[str, None] = None

        # ---- process names ----
        if isinstance(names, CPath):
            self.__cpath_info = names.cpath_info
            self.__type = names.get_type()
            self.__is_abs = names.is_abs

        elif isinstance(names, (str, bytes, list, tuple)):
            # cpath info
            cpath_info = self.to_cpath_info(names)
            self.__cpath_info = cpath_info

            # type
            if len(cpath_info.names) == 0:
                self.__type = CPathType.DIR
            else:
                # path ends with slash or not, it can be a directory. but path ends with a slash cannot be a file path.
                #   check whether it is a dir or file looking at the end of the `names`
                # self.__is_dir
                if is_dir is None:
                    # let's calculate
                    if len(cpath_info.names) == 0:  # tree root
                        self.__type = CPathType.DIR
                    else:
                        if cpath_info.last_char == "/":
                            self.__type = CPathType.DIR
                        else:
                            self.__type = CPathType.FILE
                else:
                    self.__type = CPathType.DIR if is_dir else CPathType.FILE

            # is_abs
            _is_abs_calculated = True if cpath_info.drive else False
            #       is_abs final calculation
            if is_abs is None:
                self.__is_abs = _is_abs_calculated
            else:
                assert is_abs == _is_abs_calculated, f"is_abs: {is_abs}, but calculated _is_abs_calculated: {_is_abs_calculated}"
                self.__is_abs = is_abs
        else:
            raise CFSException(f"Invalid data type of names: {type(names)}")

    @property
    def cpath_info(self) -> CPathInfo:
        return self.__cpath_info

    @property
    def drive(self) -> str:
        return self.__cpath_info.drive

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
        if len(self.names) == 0:
            return ''
        return self.names[-1]

    @property
    def names(self):
        return self.__cpath_info.names

    @property
    def names_count(self):
        return len(self.__cpath_info.names)

    @property
    def path(self):
        """
        If this is a dir then a forward slash will be prepended with the result
            EXCEPT for the root dir with zero path components.
        """
        if self.__cached_path is None:
            self.__cached_path = "/".join(self.names)
            if self.names:  # instead of self.__cached_path
                # without checking this introduced bug: empty string created a / for directory making that root path
                #   and misguiding os.path.join in real meta fs listing method
                self.__cached_path += '' if self.is_file() else '/'
            # for absolute path
            if self.__is_abs:
                self.__cached_path = (self.__cpath_info.drive if self.__cpath_info.drive != '/' else '/') + self.__cached_path
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
