from ContentFS.pathmatch.matchers.basic_matchers.abstract_base_matchers import AbcSubCompMatcher
import re


class SubCompStringMatcher(AbcSubCompMatcher):
    def __init__(self, sub_pat: str):
        assert sub_pat
        self.__sub_pat = sub_pat

        self.__regex_pat = re.escape(self.__sub_pat)

    def matches(self, sub_comp: str) -> bool:
        return self.__sub_pat == sub_comp

    @property
    def regex_pat(self) -> str:
        return self.__regex_pat
