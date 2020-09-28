import abc
import typing
import re
from ContentFS.cpaths.cpath import CPath
from collections import deque


class AbcMatcher(metaclass=abc.ABCMeta):
    """
    Abstract base class for matchers.
    """
    def matches(self, *params):
        pass


class CompMatcher(AbcMatcher):
    def __init__(self, comp):
        assert comp, "Programmer Error"
        self.__comp = comp
        self.__pat = None
        _pats = []
        chars = deque(self.__comp)
        while len(chars) > 0:
            char = chars.popleft()
            if char == '*':
                "Consecutive double asterisks are literal couple of double asterisk when this couple are not standing "
                " alone like **/z, a/** or a/**/z but standing inside a component like a/x**X/z"
                "Let's forward check it."
                if len(chars) != 0 and chars[0] == "*":
                    "Boom... double literal asterisk detected"
                    "Let's remove this dumbass that will help the loop move forward discarding this stupid"
                    chars.popleft()
                    _pats.append(re.escape("**"))
                else:
                    "Only single asterisk or the asterisk that could not make couple - like the third one in *** - "
                    " are the kings, the patterns"
                    _pats.append(r'.*?')
            elif char == '?':
                _pats.append(r'.{1}')
            elif char == '[':
                if len(chars) == 0:
                    _pats.append(re.escape(char))
                elif len(chars) == 1 and "".join(chars[0:2]) == '[!':
                    _pats.append(re.escape('[!'))
                    chars.clear()
                elif ']' not in chars:
                    _pats.append(re.escape(''.join(chars)))
                    chars.clear()
                else:
                    range_chars = []
                    # TODO: validate that the chars inside [..] or [!..] are valid range chars
                    next_char = chars.popleft()
                    is_negative = False
                    if next_char == '!':
                        is_negative = True
                    else:
                        range_chars.append(next_char)
                    while len(chars) > 0:
                        next_char = chars.popleft()
                        if next_char == ']':
                            break
                        else:
                            range_chars.append(next_char)
                    if is_negative:
                        range_chars.insert(0, '^')
                    _pats.append(f'[{"".join(range_chars)}]')
            else:
                _pats.append(re.escape(char))
        self.__pat = re.compile(f"^{''.join(_pats)}$")

    def matches(self, path_comp: str):
        return bool(self.__pat.match(path_comp))


class DoubleAsteriskMatcher(AbcMatcher):
    def __init__(self, comp):
        assert comp == '**'
        self.__comp = comp

    def matches(self, path_components, matchers):
        # hard part
        if len(matchers) == 0:
            # zero or more paths eaten by current double asterisks
            path_components.clear()
            # this last double asterisks matches the rest of the path components.
            return True
        else:
            next_matcher: CompMatcher = matchers.popleft()
            # double asterisk can match zero path comp, that's why the current path
            # comp is taken into consideration.
            next_matched = False
            while len(path_components) > 0:  # the target is to engulf the path components by next matcher.
                next_path_comp = path_components.popleft()
                if next_matcher.matches(next_path_comp):
                    # the work of double asterisk ends here. next patterns in the path matcher please.
                    next_matched = True
                    break
                else:
                    # let's match the next path component. with the matcher.
                    pass
            if next_matched:
                return True
            else:
                return False


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
