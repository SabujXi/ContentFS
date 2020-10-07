from typing import Union
from collections import OrderedDict
from ContentFS.pathmatch.fsmatchergroup import FsMatcherGroup
from ContentFS.pathmatch.fsmatchers import AbcFsMatcher
from ContentFS.cpaths import CPath, CDir
from ContentFS.pathmatch.util_matchers import dev_matcher


class FsMatcherRootGroup:
    def __init__(self):
        self.__matcher_groups = OrderedDict()

    def add(self, matcher: AbcFsMatcher, host_cdir: CDir):
        matcher_group = self.__matcher_groups.get(host_cdir.names, None)
        if matcher_group is None:
            matcher_group = FsMatcherGroup(host_cdir)
            self.__matcher_groups[host_cdir.names] = matcher_group
        matcher_group.add(matcher)
        return self

    def with_dev_matcher(self):
        return self.add(dev_matcher.DevFsMatcher(), CDir(""))

    def should_include(self, cpath: CPath):
        assert cpath.is_rel
        assert cpath.names_count > 0
        # does the parent dir matcher group exist
        parent_cdir = CDir(cpath.names[:-1])
        parent_matcher_group: Union[FsMatcherRootGroup, None] = self.__matcher_groups.get(parent_cdir.names, None)
        if parent_matcher_group is not None:
            # if parent says to exclude then look nothing beyond
            if parent_matcher_group.should_exclude(cpath):
                return False
        else:
            # look if any ancestor say that you should not match
            ancestor_cdir = parent_cdir
            while True:
                ancestor_cdir = CDir(ancestor_cdir.names[:-1])  # TODO: performace boost by passing trusted processed CPathNames object so that processing do not take palce to make cpath as they are already processed.
                ancestor_matcher_group: Union[FsMatcherGroup, None] = self.__matcher_groups.get(ancestor_cdir.names, None)
                if ancestor_matcher_group is not None:
                    if ancestor_matcher_group.should_exclude(cpath):
                        return False

                if ancestor_cdir.is_root():
                    break

        # No group asked to exclude, then include it
        return True

    def should_exclude(self, cpath: CPath):
        return not self.should_include(cpath)
