from typing import List
from ContentFS.pathmatch.matchers.path_matcher import PathMatcher
from ContentFS.pathmatch.rules_parser import gitignore_parser
from ContentFS.cpaths.cpath import CPath


class FsIgnorer:
    def __init__(self, text):
        self.__path_matchers: List[PathMatcher] = gitignore_parser(text)

    def ignore(self, cpath: CPath) -> bool:
        ignored = False
        print('-----')
        for matcher in self.__path_matchers:
            if not matcher.is_negative:
                if matcher.matches(cpath):
                    ignored = True
                    print(f'CPath: {cpath.path} - ignored by - ' + matcher.raw_rule)
                    # negation pattern consideration
                    #   when the path matcher is a directory pattern then no negation pattern will work
                    #     it will be ignored outright
                    if matcher.directories_only:  # no need of keeping track of directories list that are ignored
                        # bail out - for performance reason imposed by gitignore doc
                        print("Bail out for git performance issue")
                        break
                    else:
                        # but I have yet to see whether it will be negated by a negation pattern
                        pass
            else:
                if matcher.matches_simple(cpath):
                    ignored = False
                    print(f'CPath: {cpath.path} - included by - ' + matcher.raw_rule)

        return ignored


# if cpath.name == '.git' and cpath.is_dir():
#     return True
# return False
