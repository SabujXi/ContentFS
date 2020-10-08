from json import dumps
from typing import Union, List, Tuple

from ContentFS.cpaths import CPathComponentsInfo, CPathInfo
from ContentFS.cpaths.cpath_type import CPathType
from ContentFS.exceptions import CFSException


class CPath:
    @staticmethod
    def to_path_comps_info(path_or_comp_string: str) -> CPathComponentsInfo:
        return CPathComponentsInfo(path_or_comp_string)

    @staticmethod
    def to_cpath_info(path: Union[str, bytes, List[str], Tuple[str, ...]]) -> CPathInfo:
        return CPathInfo(path)

    def __init__(self, names: Union['CPath', CPathInfo, str, bytes, List[str], List[bytes], Tuple[str, ...], Tuple[bytes, ...]], is_dir=None, is_abs=None):
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
            self.__cpath_info = names.get_cpath_info()
            self.__type = names.get_type()
            self.__is_abs = names.is_abs
        else:
            if isinstance(names, CPathInfo):
                cpath_info: CPathInfo = names
            elif isinstance(names, (str, bytes, list, tuple)):
                # cpath info
                cpath_info = self.to_cpath_info(names)
            else:
                raise CFSException(f"Invalid data type of names: {type(names)}")

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

    # FUNDAMENTAL METHODS
    @property
    def names(self):
        return self.__cpath_info.names

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

    def get_type(self) -> CPathType:
        return self.__type

    def get_type_str(self) -> str:
        return self.__type.value

    # HELPER METHODS
    def get_cpath_info(self) -> CPathInfo:
        return self.__cpath_info

    def get_parent(self) -> Union['CPath', None]:
        cpath_info = self.__cpath_info
        if not cpath_info.has_parent():
            return None
        return CPath(cpath_info.get_parent())

    def has_parent(self) -> bool:
        return self.__cpath_info.has_parent()

    @property
    def names_count(self):
        return len(self.__cpath_info.names)

    def is_file(self):
        return self.__type is CPathType.FILE

    def is_dir(self):
        return self.__type is CPathType.DIR

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
        return self.get_type() == another.get_type() and \
               self.names == another.names and \
               self.is_rel == another.is_rel

    def equals_by_path_only(self, another: 'CPath'):
        """Equals by path only"""
        return self.path == another.path
