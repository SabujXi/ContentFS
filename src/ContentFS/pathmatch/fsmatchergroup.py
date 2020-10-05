from typing import List, Union
from .contracts import AbcFsMatcher
from ..cpaths import CPath
from .exceptions import PathMatchError
from .util_matchers.dev_matcher import DevFsMatcher


class FsMatcherGroup:
    def __init__(self, *fsmatchers: AbcFsMatcher):
        self.__fs_matchers: List[AbcFsMatcher] = []
        self.__fs_matchers.extend(fsmatchers)

    def should_include(self, cpath: CPath) -> bool:
        if len(self.__fs_matchers) == 0:
            # default action is including
            # primary/main intention is including.
            return True

        do_include: bool = True  # default action is inclde.
        for fsmatcher in self.__fs_matchers:
            matches = fsmatcher.matches(cpath)
            if matches:
                if fsmatcher.is_includer():
                    do_include = True
                else:
                    do_include = False
            else:
                # then default behavior is inclusion.
                # if matcher is not an includer then I will not take decisions from that when that does not match.
                do_include = True
        return do_include

        # if not excluded then you must include it

    def should_exclude(self, cpath: CPath) -> bool:
        return not self.should_include(cpath)

    def add(self, fsmatcher: AbcFsMatcher):
        if fsmatcher in self.__fs_matchers:
            raise PathMatchError("Cannot add the same matcher object twice.")
        self.__fs_matchers.append(fsmatcher)
        return self

    def with_dev_matcher(self):
        return self.add(DevFsMatcher())

    def get_matchers(self):
        return tuple(self.__fs_matchers)
