import re
from ContentFS.pathmatch.matchers.basic_matchers.abstract_base_matchers import AbcSubCompMatcher


class SubCompWildcardMatcher(AbcSubCompMatcher):
    def __init__(self, sub_pat: str):
        assert sub_pat == '*'
        self.__sub_pat = sub_pat

        self.__regex_pat = r'[^/]*?'
        self.__regex = re.compile(f'^{self.__regex_pat}$')

    def matches(self, sub_comp) -> bool:
        return True if self.__regex.match(sub_comp) else False

    @property
    def regex_pat(self) -> str:
        return self.__regex_pat
