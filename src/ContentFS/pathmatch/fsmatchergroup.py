from typing import List, Union
from .contracts import AbcFsMatcher
from ..cpaths import CPath
from .exceptions import PathMatchError
from .util_matchers.dev_matcher import DevFsMatcher
from ContentFS.cpaths import CDir


class FsMatcherGroup:
    def __init__(self, host_dir: CDir, *fsmatchers: AbcFsMatcher):
        self.__host_dir: CDir = host_dir
        self.__fs_matchers: List[AbcFsMatcher] = []

        self.__fs_matchers.extend(fsmatchers)

    @property
    def host_dir(self) -> CDir:
        return self.__host_dir

    def should_include(self, cpath: CPath) -> bool:
        if len(self.__fs_matchers) == 0:
            # default action is including
            # primary/main intention is including.
            return True

        include_decisions = []

        for fsmatcher in self.__fs_matchers:
            matches = fsmatcher.matches(cpath)
            if matches:
                if fsmatcher.is_includer():
                    # including decision only from includer only when includer matches
                    include_decisions.append(True)
                else:
                    # excluder decision only from excluder only when excluder matches
                    include_decisions.append(False)

        # decision making
        if not include_decisions:  # none gave any decision, then include
            return True
        else:  # so now take the last decision
            return include_decisions[-1]

    def should_exclude(self, cpath: CPath) -> bool:
        return not self.should_include(cpath)

    def add(self, fsmatcher: AbcFsMatcher):
        if fsmatcher in self.__fs_matchers:
            raise PathMatchError("Cannot add the same matcher object twice.")
        # decision making where to position the matcher in the group
        if fsmatcher.is_includer():
            # if it is an includer then put it at the end
            self.__fs_matchers.append(fsmatcher)
        else:
            # put it after the last excluder, if not present then insert at the beginning
            last_excluder_idx = -1
            for idx, fm in enumerate(self.__fs_matchers):
                if not fm.is_includer():
                    last_excluder_idx = idx
            if last_excluder_idx == -1:
                # no excluder exist already
                self.__fs_matchers.insert(0, fsmatcher)
            else:
                # put the fs matcher after the last excluder
                self.__fs_matchers.insert(last_excluder_idx + 1, fsmatcher)
        return self

    def with_dev_matcher(self):
        return self.add(DevFsMatcher())

    def get_matchers(self):
        return tuple(self.__fs_matchers)
