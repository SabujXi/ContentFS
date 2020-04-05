import abc
import typing
from ContentFS.cpaths.cpath import CPath
from collections import deque


class AbcMatcher(metaclass=abc.ABCMeta):
    def matches(self, *params):
        pass


class CompMatcher(AbcMatcher):
    def __init__(self, comp):
        self.__comp = comp

    def matches(self, path_comp):
        pass


class DoubleAsteriskMatcher(AbcMatcher):
    def __init__(self, comp):
        self.__comp = comp

    def matches(self, current_path_comp, path_components, matchers):
        # hard part
        if len(matchers) == 0:
            # zero or more paths eaten by current double asterisks
            path_components.clear()
            # this last double asterisks matches the rest of the path components.
            return True
        else:
            next_matcher: CompMatcher = matchers.popleft()
            next_path_comp = current_path_comp  # double asterisk can match zero path comp, that's why the current path
            # comp is taken into consideration.
            next_matched = False
            while len(path_components) > 0:  # the target is to engulf the path components by next matcher.
                if next_matcher.matches(next_path_comp):
                    # the work of double asterisk ends here. next patterns please.
                    next_matched = True
                    break
                else:
                    # let's match the next path component. with the matcher.
                    next_path_comp = path_components.popleft()
            if next_matched:
                return True
            else:
                return False


class PathMatcher:
    def __init__(self, matchers: typing.List, line_original: str, is_negative: bool, only_directories: bool, is_root_relative: bool):
        self.__matchers = matchers
        self.__line_original = line_original
        self.__is_negative = is_negative
        self.__only_directories = only_directories
        self.__is_root_relative = is_root_relative

    @property
    def line(self):
        return self.__line_original

    @property
    def is_negative(self):
        return self.__is_negative

    @property
    def directories_only(self):
        return self.__only_directories

    @property
    def is_root_relative(self):
        return self.__is_root_relative

    def match(self, cpath: CPath):
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
            path_comp = path_components.popleft()

            if isinstance(matcher, CompMatcher):
                if matcher.matches(path_comp):
                    continue
                else:
                    matched = False
                    break
            else:
                assert isinstance(matcher, DoubleAsteriskMatcher), "Programmer Error"
                # hard part
                double_asterisk_matched = matcher.matches(path_comp, path_components, matchers)
                if double_asterisk_matched:
                    continue
                else:
                    break

        if self.is_negative:
            return not matched
        else:
            return matched
