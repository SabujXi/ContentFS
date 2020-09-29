from ContentFS.pathmatch.matchers.basic_matchers.abstract_base_matchers import AbcSubCompMatcher
import typing
import re


class SubCompCharClassMatcher(AbcSubCompMatcher):
    def __init__(self, range_chars: typing.List[str], is_negative: bool):
        self.__range_chars = range_chars
        self.__is_negative = is_negative
        self.__regex_pat = f"[{'^' if self.__is_negative else '' }{''.join(range_chars)}]"
        self.__regex = re.compile(f'^{self.__regex_pat}$')

    def matches(self, sub_comp) -> bool:
        return bool(self.__regex.match(sub_comp))

    @property
    def regex_pat(self) -> str:
        return self.__regex_pat
