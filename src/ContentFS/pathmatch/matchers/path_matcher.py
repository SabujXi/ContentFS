import typing
from collections import deque

from ContentFS.cpaths.cpath import CPath
from ContentFS.pathmatch.matchers.basic_matchers.abstract_base_matchers import AbcMatcher
from ContentFS.pathmatch.matchers.basic_matchers.component_matcher import CompMatcher
from ContentFS.pathmatch.matchers.basic_matchers.double_asterisk_matcher import DoubleAsteriskMatcher


class PathMatcher:
    """PathMatcher is intended to be constructed by rules_parser and not by manually/by hand"""
    def __init__(self, matchers: typing.List[AbcMatcher], line_original: str, is_negative: bool, only_directories: bool, is_root_relative: bool):
        self.__matchers: typing.Tuple[AbcMatcher] = tuple(matchers)
        self.__line_original: str = line_original
        self.__is_negative: bool = is_negative
        self.__only_directories: bool = only_directories
        self.__is_root_relative: bool = is_root_relative

    @property
    def raw_rule(self):
        """The line of text that was used"""
        return self.__line_original

    @property
    def matchers(self) -> typing.Tuple[AbcMatcher]:
        return self.__matchers

    @property
    def is_negative(self) -> bool:
        """
        this matcher was produced from a negative rule from gitignore rule that starts with a `!`
        """
        return self.__is_negative

    @property
    def directories_only(self) -> bool:
        """
        This path matcher will only match directories because the rule ended with a slash `/`
        """
        return self.__only_directories

    @property
    def is_root_relative(self) -> bool:
        """
        This path mather was produced from a gitignore rule that had a separator `/` within it that makes it count the
        rule to be applied from the root. It will not start matching from inner directories.
        """
        return self.__is_root_relative

    def matches(self, cpath: CPath):
        if cpath.is_file() and self.directories_only:
            # path to be matched is a file but this pattern will only match directories
            return False
        if len(cpath.names) == 0:
            return False

        matched = True
        path_components = deque(cpath.names)
        matchers: typing.Deque[AbcMatcher] = deque(self.__matchers)

        while True:
            # no condition here as we have some nested checks and state changes that will be done at the beginning
            # of the loop.
            if len(path_components) == 0 or len(matchers) == 0:
                if len(path_components) != 0:
                    # all the paths were not consumed and thus the match is not completed.
                    matched = False
                break
            matcher: AbcMatcher = matchers.popleft()

            if isinstance(matcher, CompMatcher):
                path_comp = path_components.popleft()
                if matcher.matches(path_comp):
                    continue
                else:
                    matched = False
                    break
            else:
                assert isinstance(matcher, DoubleAsteriskMatcher), "Programmer Error"
                # hard part
                double_asterisk_matched = matcher.matches(path_components, matchers)
                if double_asterisk_matched:
                    continue
                else:
                    matched = False
                    break

        if self.is_negative:
            return not matched
        else:
            return matched