import re
import typing
from collections import deque

from ContentFS.pathmatch.matchers.basic_matchers.abstract_base_matchers import AbcMatcher, AbcSubCompMatcher
from ContentFS.pathmatch.matchers.basic_matchers.sub_comp_matchers import (
    SubCompStringMatcher,
    SubCompWildcardMatcher,
    SubCompOptionMatcher,
    SubCompCharClassMatcher
)


class CompMatcher(AbcMatcher):
    def __init__(self, comp):
        assert comp, "Programmer Error"
        self.__comp = comp

        _sub_comps: typing.List[AbcSubCompMatcher] = []
        # _pats = []
        chars = deque(self.__comp)
        while len(chars) > 0:
            char = chars.popleft()
            if char == '*':
                # wildcard or literal double asterisk couple
                "Consecutive double asterisks are literal couple of double asterisk when this couple are not standing "
                " alone like **/z, a/** or a/**/z but standing inside a component like a/x**X/z"
                "Let's forward check it."
                if len(chars) != 0 and chars[0] == "*":
                    "Boom... double literal asterisk detected"
                    "Let's remove this dumbass that will help the loop move forward discarding this stupid"
                    chars.popleft()
                    # _pats.append(re.escape("**"))
                    _sub_comps.append(
                        SubCompStringMatcher("**")
                    )
                else:
                    "Only single asterisk or the asterisk that could not make couple - like the third one in *** - "
                    " are the kings, the patterns"
                    # _pats.append(r'.*?')
                    _sub_comps.append(
                        SubCompWildcardMatcher("*")
                    )
            elif char == '?':
                # option
                # _pats.append(r'.{1}')
                _sub_comps.append(
                    SubCompOptionMatcher('?')
                )
            elif char == '[':
                if len(chars) == 0:
                    # _pats.append(re.escape(char))
                    _sub_comps.append(
                        SubCompStringMatcher(char)
                    )
                elif len(chars) == 1 and "".join(chars[0:2]) == '[!':
                    # _pats.append(re.escape('[!'))
                    _sub_comps.append(
                        SubCompStringMatcher('[!')
                    )
                    chars.clear()
                elif ']' not in chars:
                    # _pats.append(re.escape(''.join(chars)))
                    _sub_comps.append(
                        SubCompStringMatcher(''.join(chars))
                    )
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
                    # if is_negative:
                    #     range_chars.insert(0, '^')
                    # _pats.append(f'[{"".join(range_chars)}]')
                    _sub_comps.append(
                        SubCompCharClassMatcher(range_chars, is_negative)
                    )
            else:
                # _pats.append(re.escape(char))
                _sub_comps.append(
                    SubCompStringMatcher(char)
                )

        self.__regex_pat = ''.join(sub_comp.regex_pat for sub_comp in _sub_comps)
        self.__regex = re.compile(f"^{ self.__regex_pat }$")

    def matches(self, path_comp: str):
        return bool(self.__regex.match(path_comp))

    # @property
    # def regex_pat(self) -> str:
    #     return self.__regex_pat
