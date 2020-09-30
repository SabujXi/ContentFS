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

    def matches_simple(self, cpath: CPath):
        """
        This method does not take into consideration whether the pattern is a negative pattern
        """

        """
        New strategy:
            To solve `test_ignore__negation_directory`
            And to make things more future proof.
            * Matching of path with pattern will start from the end of the path and pattern instead of the beginning.
            Look: when paths are not root relative, I start checking from the beginning of the path and go to the end.
                But, I could stop at the end when the end did not match, it will also make the path matcher performant.
                It will also solve confusion with double asterisk with putting some conditions.
        """
        if cpath.is_file() and self.directories_only:
            # path to be matched is a file but this pattern will only match directories
            return False
        if len(cpath.names) == 0:  # TODO: are cpath with zerom comp valid?
            return False

        # initial assumption that it matched the path - you have to prove it wrong by setting False where possible
        matched = True
        path_components = deque(cpath.names)
        matchers: typing.Deque[AbcMatcher] = deque(self.__matchers)

        while True:
            # no condition on while as we have some nested checks and state changes that will be done at the beginning
            #   of the loop.

            # pull out the right most matcher
            matcher = matchers.pop()
            if isinstance(matcher, CompMatcher):
                path_comp = path_components.pop()
                if not matcher.matches(path_comp):
                    matched = False
            else:
                assert isinstance(matcher, DoubleAsteriskMatcher), "Programmer's Error"

                # keep going backward until a CompMatcher matches
                # check if current path comp matches with any previous path comp matcher

                # get the next left rule that is CompMatcher
                if len(matchers) > 0:
                    while isinstance(matcher, DoubleAsteriskMatcher):
                        # using while loop to get single element - instead of using `if`
                        matcher = matchers.pop()
                        assert isinstance(matcher, CompMatcher), 'Programmer\'s Error - consecutive double ' \
                                                                 'asterisk pairs are not eliminated in rules parser'
                    # which of the left path comps matches with this matcher?
                    _a_left_path_comp_matched = False
                    while len(path_components) > 0:
                        path_comp = path_components.pop()
                        if matcher.matches(path_comp):
                            _a_left_path_comp_matched = True
                            break

                    if not _a_left_path_comp_matched:
                        matched = False
                else:
                    # everything to the left is engulfed by this double asterisk
                    path_components.clear()

            if len(path_components) == 0 or len(matchers) == 0:
                if len(matchers) == 0 \
                        and matched is True \
                        and not self.is_root_relative:
                    # matchers are exhausted | no matter if path_components left or not.
                    # none said that it was not a match
                    # it is non root relative

                    # it is matched no matter there is any path components left or not
                    # matched = True holds
                    ...
                elif any([path_components, matchers]):  # if any of them are non empty.
                    # all the paths were not consumed and thus the match is not completed.
                    matched = False
                break
        return matched

    def matches(self, cpath: CPath):
        matched = self.matches_simple(cpath)
        if matched and self.is_negative:
            return not matched
        return matched

    def matches_parent_dir(self, cpath: CPath):
        assert self.directories_only, "Programmer's Error"
