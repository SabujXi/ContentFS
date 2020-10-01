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
        assert cpath.is_rel, "Programmer's Error - you passed absolute cpath"
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
        New strategy failed:
            It works best for non root relative but not for root relative and directory
        
        Next strategy:
            ...
        """
        # if cpath.is_file() and self.directories_only:
        # -> here is the bug when it was not acting accordingly: logs/ pattern also ignores logs/important.log
        #       <- coz it's parent ignored
        #     # path to be matched is a file but this pattern will only match directories
        #     return False
        if len(cpath.names) == 0:  # TODO: are cpath with zero comp valid?
            return False

        # initial assumption that it matched the path - you have to prove it wrong by setting False where possible
        matched = True
        path_components = deque(cpath.names)
        matchers: typing.Deque[AbcMatcher] = deque(self.__matchers)

        while True:
            # no condition on while as we have some nested checks and state changes that will be done at the beginning
            #   of the loop.

            # pull out the left most matcher
            matcher = matchers.popleft()
            if isinstance(matcher, CompMatcher):
                path_comp = path_components.popleft()
                if not matcher.matches(path_comp):
                    if self.is_root_relative:
                        matched = False
                        break  # no more conditions (at the end) or something. it ends here. it will not match.
                    else:
                        # let's try until the end - as this rule/pattern/matcher is not tied to the root.
                        _finally_matched = False
                        while path_components:
                            path_comp = path_components.popleft()
                            if matcher.matches(path_comp):
                                _finally_matched = True
                        matched = _finally_matched
                        if matched is False:
                            break  # we tried till the last blood, but it doesn't matter, didn't match. so no condition at the end.
            else:
                assert isinstance(matcher, DoubleAsteriskMatcher), "Programmer's Error"

                # keep going forward until a CompMatcher matches
                # check if current path comp matches with any next path comp matcher

                # get the next rule that is CompMatcher
                if len(matchers) > 0:
                    comp_matcher: CompMatcher
                    while isinstance(matcher, DoubleAsteriskMatcher):
                        # using while loop to get single element - instead of using `if`
                        comp_matcher = matcher = matchers.popleft()
                        assert isinstance(comp_matcher, CompMatcher), 'Programmer\'s Error - consecutive double ' \
                                                                 'asterisk pairs are not eliminated in rules parser'
                    # which of the right path comps matches with this matcher?
                    _next_path_comp_matched = False
                    while len(path_components) > 0:
                        path_comp = path_components.popleft()
                        if comp_matcher.matches(path_comp):
                            _next_path_comp_matched = True
                            break

                    if not _next_path_comp_matched:
                        matched = False
                        break  # bail out, nothing matters now.
                else:
                    # everything to the left is engulfed by this double asterisk
                    path_components.clear()

            assert matched is True, "No way to reach here unless matched is true. Programmer's Error."

            # all matchers are done

            if len(path_components) == 0 or len(matchers) == 0:
                # path's subdirectory matches pattern - no matter if path_coms exhausted
                # and no matter root relative or not
                if len(matchers) == 0:
                    if len(path_components) == 0 and cpath.is_file() and self.directories_only:
                        # check if cpath is a file but the pattern was only for directories
                        # e.g.: logs/ won't match CPath('logs')
                        matched = False
                        break
                    else:
                        # no matter whether all paths are exhausted or not.
                        # logs/ -> logs/a, logs/a/
                        break

                if any([path_components, matchers]):  # if any of them are non empty.
                    # all the paths were not consumed and thus the match is not completed.
                    matched = False
                break
        return matched

    def matches(self, cpath: CPath):
        matched = self.matches_simple(cpath)
        if matched and self.is_negative:
            return not matched
        return matched
