from ContentFS.utils.json_utils import json_encode
import re
from typing import Tuple

from ContentFS.exceptions import CFSExceptionInvalidPathName


class CPathComponentsInfo:
    """
    Content Path Component Information
    Splits a path string into individual components
    - names: the path components separated by separator '\' or '/'
    """
    SPLIT_RE = re.compile(r'[/\\]+')  # regular expression for splitting paths
    DRIVE_PATH_RE = re.compile(r'^(?P<drive>[a-z]+:|/)?(?P<path>.*)', re.I)  # for extracting drive and path
    # SPACE_ONLY_PATH_RE = re.compile(r'^[ \t\n\r]+$')  # spaces

    def __init__(self, path_or_comp_string: str):
        """
        Full path string or path comp (from array) to Content Path Components Info
        :param path_or_comp_string: a full path or a component of the path
        """

        last_char = ''
        components = []
        drive = ''

        # if CPathComponentsInfo.SPACE_ONLY_PATH_RE.match(path_or_comp_string):
        #     raise CFSExceptionInvalidPathName(f"Path string provided  `{path_or_comp_string}` - that is empty or contains only spaces")

        path_or_comp_string = re.sub(r"[\\/]{2,}", path_or_comp_string, '/').lstrip('/')

        _m = CPathComponentsInfo.DRIVE_PATH_RE.match(path_or_comp_string)
        drive = _m.group('drive') if _m.group('drive') is not None else ''
        path = _m.group('path')

        if len(path) > 0:
            last_char = path[-1]

        cleaned_path_string = path.strip("/")
        # for '/' -> '' thus spliting that path results in one [''] instead of ['', '']
        # re.split('/', '//')
        # -> ['', '', ''] with r stripping it becomes ['']
        # re.split('/', '//') -> ['', 'a']
        _comps = [comp for comp in CPathComponentsInfo.SPLIT_RE.split(cleaned_path_string) if comp]

        components.extend(_comps)

        self.__drive: str = drive
        self.__components: tuple = tuple(components)
        self.__last_char: str = last_char

    # FUNDAMENTAL METHODS
    @property
    def drive(self) -> str:
        """
        Drive letter with colon or unix root.
        """
        return self.__drive

    @property
    def names(self) -> Tuple[str, ...]:
        return self.__components

    @property
    def last_char(self) -> str:
        """
        Keeps a backup of the last character so that we can take decisions when we need to know what was the real last
        character.

        Note: this does not include the drive char. For example a path is '/' then the last char is empty string ''
        """
        return self.__last_char

    # HELPER METHODS
    def make_path(self):
        if self.has_drive:
            res = f"{self.drive}://{'/'.join(self.names)}"
        else:
            res = f"{'/'.join(self.names)}"

    def get_parent(self):
        pass

    @property
    def has_drive(self) -> bool:
        return self.__drive != ''

    @property
    def has_non_unix_drive(self) -> bool:
        """
        It is not necessary that it will have to be windows drive, it can be file:// drive or even network one.
        """
        return self.__drive != "" and  self.__drive != '/'

    @property
    def has_unix_root(self) -> bool:
        return self.__drive == '/'

    def to_dict(self) -> dict:
        return {
            'drive': self.drive,
            'names': self.names,
            'last_char': self.last_char
        }

    def to_json(self) -> str:
        return json_encode(self.to_dict())


class Component:
    """
    A path component
    """
    def __init__(self, comp_str: str, as_last_comp_ends_with_slash: bool = False):
        """
        :param comp_str: component as string
        :param as_last_comp_ends_with_slash: if this component is the last component and it also ended with a slash
        """
        # invalid path or component checks
        validity_result = _invalid_path_comp_check(comp_str)
        if validity_result != "":
            raise CFSExceptionInvalidPathName(validity_result)
        self.__name = comp_str
        self.__as_last_comp_ends_with_slash = as_last_comp_ends_with_slash

    @property
    def name(self) -> str:
        return self.__name

    @property
    def as_last_comp_ends_with_slash(self) -> bool:
        """
        This is the last component, and it ends with a slash
        """
        return self.__as_last_comp_ends_with_slash


class Drive:
    """
    Drive or drive letter.
    Example:
        C:
        /
        file:
    """
    def __int__(self, drive: str):
        if not re.match("^[a-z]+:$", drive, re.I):
            raise CFSExceptionInvalidPathName(f"Invalid drive: {drive}")
        self.__drive = drive

    @property
    def drive(self):
        return self.__drive


def _invalid_path_comp_check(path_or_comp: str):
    """
    Will check if a path compoenent is valid or not
    :param path_or_comp: a path or component
    :return: a string, if the string is empty then no error found.
    """
    EMPTY_PATH_COMP_RE = re.compile(r'^\s+|$')  # spaces or empty string
    DOT_PATH_COMP_RE = re.compile(r'^(\.|\s)+$')  # one or more dots
    PATH_SEP = re.compile(r'[\\/]')

    if EMPTY_PATH_COMP_RE.match(path_or_comp):
        return "Path component cannot be empty or space characters only"
    elif DOT_PATH_COMP_RE.match(path_or_comp):
        return "Path component cannot be one or more dots or dot and space character collection"
    elif PATH_SEP.search(path_or_comp):
        return "Path component cannot contain path separator"
    else:
        return ""


