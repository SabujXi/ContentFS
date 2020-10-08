from json import dumps
from collections import OrderedDict
from typing import List, Tuple
from ContentFS.cpaths.cpath import CPath
from ContentFS.ctrees.cdirtree import CDirTree
from ContentFS.cpaths.cfile import CFile
from ContentFS.cpaths.cdir import CDir
from ContentFS.cpaths.cfile_hashed import CFileHashed
from ContentFS.pathmatch.fsmatchers import FsMatcherGitignore, UniMetaFsIncluder, UniMetaFsExcluder
from ContentFS.pathmatch.contracts import AbcFsMatcher
from ContentFS.contracts.meta_fs_backend_contract import BaseMetaFsBackendContract
from ContentFS.meta_fs_backends.real_fs_backend_meta import RealMetaFileSystemBackend
from ..pathmatch.fsmatchergroup import FsMatcherGroup
from ContentFS.exceptions import CFSException
from ContentFS.pathmatch.fsmatcherrootgroup import FsMatcherRootGroup
from ContentFS.pathmatch import FsMatcherMapper


class CRootDirTree(CDirTree):
    def __init__(self, base_path, fs: BaseMetaFsBackendContract = None):
        super().__init__()
        self.__base_path = base_path
        if fs is None:
            fs = RealMetaFileSystemBackend().set_base_path(self.__base_path)
        self.__fs = fs
        self.__loaded = False

        # fs matchers.
        self.__fs_matcher_root_group = FsMatcherRootGroup()

    def add_matcher(self, fsmatcher: AbcFsMatcher, parent_cdir: CDir):
        self.__fs_matcher_root_group.add(fsmatcher, parent_cdir)
        return self

    def with_dev_matcher(self) -> 'CRootDirTree':
        self.__fs_matcher_root_group.with_dev_matcher()
        return self

    @property
    def base_path(self):
        return self.__base_path

    def __list(self, parent: CDirTree, do_hash=False):
        assert isinstance(parent, CDirTree)
        path_names: List[str] = self.__fs.listdir(parent)
        parent_names: Tuple[str] = parent.names

        # transform path into cpath, but don't do hash because: the file might already be ignored by a fs matcher
        #   config file. hash in listing block
        child_cpaths = []
        for path_name in path_names:
            names = (*parent_names, path_name)
            child_cpath = CPath(names)
            if self.__fs.is_file(child_cpath):
                mtime = self.__fs.getmtime(child_cpath)
                size = self.__fs.getsize(child_cpath)
                child_cpath = CFile(names, mtime, size)
            else:
                child_cpath = CDir(names)
            child_cpaths.append(child_cpath)

        # matcher file finding block
        # search for fs matcher config files
        for child_cpath in child_cpaths:
            if self.__fs.is_real_fs() and child_cpath.is_file():
                if FsMatcherMapper.exists(child_cpath.name):
                    matcher_cfile = child_cpath
                    # check includer or excluder
                    # TODO: read content of fs matcher files (e.g. gitignore) and then match further relative to that.
                    # make a fs matcher and attache it to the parent.
                    content = ""
                    with self.__fs.open(matcher_cfile, "r", encoding="utf-8") as f:
                        content = f.read()
                    fs_matcher: AbcFsMatcher
                    fs_matcher = FsMatcherMapper.get(matcher_cfile.name)(content)
                    # group will decide where to place includer and where excluder.
                    # root group will forward to appropriate matcher group
                    self.__fs_matcher_root_group.add(fs_matcher, parent)

        # now list & hash if not ignored
        for child_cpath in child_cpaths:
            if not self.__fs_matcher_root_group.should_include(child_cpath):
                continue

            if child_cpath.is_file() and do_hash:
                hash_value = self.__fs.gethash(child_cpath)
                child_cpath = CFileHashed(child_cpath.names, child_cpath.mtime, child_cpath.size, hash_value)

            if child_cpath.is_dir():
                last_subtree = parent.add(child_cpath)
                self.__list(last_subtree, do_hash=do_hash)
            else:
                parent.add(child_cpath)

    def load(self, do_hash=False):
        if self.__loaded:
            raise Exception("Can load only once")
        self.__list(self, do_hash=do_hash)
        self.__loaded = True

    def to_dict(self):
        return {
            'cpaths': self.to_list()
        }

    def to_list(self):
        return [child.to_dict() for child in self.get_children()]

    def to_json(self):
        return dumps(self.to_dict())
