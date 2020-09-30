from ContentFS.pathmatch.matchers.basic_matchers.abstract_base_matchers import AbcMatcher
from ContentFS.pathmatch.matchers.basic_matchers.component_matcher import CompMatcher


class DoubleAsteriskMatcher(AbcMatcher):
    def __init__(self, comp):
        assert comp == '**'
        self.__comp = comp

    def matches(self, path_components, matchers):
        raise Exception("This method must not be used - path matcher handles double asterisk stuffs")
