from typing import List
from ContentFS.pathmatch.matchers import PathMatcher
from ContentFS.pathmatch.rules_parser import gitignore_parser


class FsIgnorer:
    def __init__(self, text):
        self.__path_matchers: List[PathMatcher] = gitignore_parser(text)
        self.__ignored_dirs = []

    def ignore(self, cpath) -> bool:
        matched = False
        for matcher in self.__path_matchers:
            if matcher.matches(cpath):
                matched = True
                break
        return matched


# if cpath.name == '.git' and cpath.is_dir():
#     return True
# return False
