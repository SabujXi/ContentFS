from typing import List
from ContentFS.pathmatch.matchers.path_matcher import PathMatcher
from ContentFS.pathmatch.rules_parser import gitignore_parser
from ContentFS.cpaths.cpath import CPath
import abc


class AbcFsMatcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def include(self, cpath: CPath) -> bool:
        pass

    @abc.abstractmethod
    def exclude(self, cpath: CPath) -> bool:
        pass


class FsMatcherGitignore(AbcFsMatcher):
    def __init__(self, text):
        self.__path_matchers: List[PathMatcher] = gitignore_parser(text)

    def include(self, cpath: CPath) -> bool:
        return not self.exclude(cpath)

    def exclude(self, cpath: CPath) -> bool:
        return self.ignore(cpath)

    def ignore(self, cpath: CPath) -> bool:
        assert cpath.is_rel, "Programmer's Error - you passed absolute path"
        ignored = False
        for matcher in self.__path_matchers:
            if not matcher.is_negative:
                if matcher.matches(cpath):
                    ignored = True
                    # negation pattern consideration
                    #   when the path matcher is a directory pattern then no negation pattern will work
                    #     it will be ignored outright
                    if matcher.directories_only:  # no need of keeping track of directories list that are ignored
                        # bail out - for performance reason imposed by gitignore doc
                        break
                    else:
                        # but I have yet to see whether it will be negated by a negation pattern
                        pass
            else:
                if matcher.matches_simple(cpath):
                    ignored = False

        return ignored

