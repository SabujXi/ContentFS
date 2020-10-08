import json
import re
from typing import Tuple

from ContentFS.exceptions import CFSExceptionInvalidPathName


class CPathComponentsInfo:
    SPLIT_RE = re.compile(r'[/\\]+')
    DRIVE_PATH_RE = re.compile(r'^(?P<drive>[a-z]+:|/)?(?P<path>.*)')  # for extracting drive and path
    SPACE_ONLY_PATH_RE = re.compile(r'^[ \t\n\r]+$')  # spaces

    def __init__(self, path_or_comp_string: str):
        """
        Full path string or path comp (from array) to Components Info

        * It doesn't check whether this contains white spaces at the beginning or at the end.
          It assumes that such invalid stuff will not be passed to it.
        """
        last_char = ''
        components = []
        drive = ''

        if path_or_comp_string != "":
            if CPathComponentsInfo.SPACE_ONLY_PATH_RE.match(path_or_comp_string):
                raise CFSExceptionInvalidPathName(f"Path string provided  `{path_or_comp_string}` - that is empty or contains only spaces")

            path_or_comp_string = path_or_comp_string.replace("\\", "/")

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

        self.__drive = drive
        self.__components = tuple(components)
        self.__last_char = last_char

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
        return self.__last_char

    # HELPER METHODS
    @property
    def has_drive(self) -> bool:
        return self.__drive != ''

    @property
    def has_non_unix_drive(self) -> bool:
        """
        It is not necessary that it will have to be windows drive, it can be file:// drive or even network one.
        """
        return self.__drive != '/'

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
        return json.dumps(self.to_dict())
