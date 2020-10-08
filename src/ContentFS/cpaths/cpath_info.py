import json
from typing import Union, List, Tuple

from .cpath_components_info import CPathComponentsInfo
from ContentFS.exceptions import CFSExceptionInvalidPathName, CFSException


class CPathInfo:
    def __init__(self, path: Union[str, bytes, List[str], Tuple[str, ...], 'CPathInfo', Tuple[str, Tuple[str, ...], str]], ___path_is_info_tuple: bool = False):
        # TODO: unittest -_- (should write unittest first)
        """
        Will linerize name components or iterable.
        """
        if ___path_is_info_tuple:
            assert isinstance(path, tuple)
            drive, names, last_char = path

        elif not isinstance(path, CPathInfo):
            drive: str = ''  # None
            names: Union[List[str], Tuple[str, ...]] = []
            last_char: str = ''  # None
            # when a string of path instead of an iterable of names is provided.
            #   or when byte string is provided
            if isinstance(path, (str, bytes)):
                comps_info = CPathComponentsInfo(path)

                names = comps_info.names
                drive = comps_info.drive  # str(path[0]) if len(path) > 0 else ''
                last_char = comps_info.last_char  # str(path[-1]) if len(path) > 0 else ''
            # when an iterable of path component strings is provided
            #   but as those strings might have slashes between then
            elif isinstance(path, (list, tuple)):
                for i, name in enumerate(path):
                    assert isinstance(name, (str, bytes)), f"Invalid data type of name inside names: {type(name)}"

                    comps_info = CPathComponentsInfo(name)
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
        else:
            cpath_info: CPathInfo = path

            drive = cpath_info.drive
            names = cpath_info.names
            last_char = cpath_info.last_char

        self.__drive = drive
        self.__names = tuple(names)
        self.__last_char = last_char

    # FUNDAMENTAL METHODS
    @property
    def drive(self) -> str:
        return self.__drive

    @property
    def names(self) -> Tuple[str, ...]:
        return self.__names

    @property
    def last_char(self) -> str:
        return self.__last_char

    # HELPER METHODS for ancestor/descendant
    def is_root(self) -> bool:
        return len(self.__names) == 0

    def has_parent(self) -> bool:
        return len(self.names) > 0

    def get_parent(self) -> Union['CPathInfo', None]:
        if len(self.names) > 0:
            drive: str = self.__drive
            names: Tuple[str, ...] = self.__names[:-1]
            last_char: str = '/' if names else ''
            cpath_info = CPathInfo((drive, names, last_char), ___path_is_info_tuple=True)
            return cpath_info
        return None

    # HELPER METHODS
    def __len__(self):
        return len(self.__names)

    def to_dict(self) -> dict:
        return {
            'drive': self.drive,
            'names': self.names,
            'last_char': self.last_char,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
