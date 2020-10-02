from json import dumps
from typing import List
from ContentFS.cpaths.cpath import CPath
from ContentFS.ctrees.cdirtree import CDirTree
from ContentFS.cpaths.cfile import CFile
from ContentFS.cpaths.cdir import CDir
from ContentFS.cpaths.cfile_hashed import CFileHashed
from ContentFS.pathmatch.fsmatchers import AbcFsMatcher, FsMatcherGitignore
from ContentFS.contracts.meta_fs_backend_contract import BaseMetaFsBackendContract
from ContentFS.meta_fs_backends.real_fs_backend_meta import RealMetaFileSystemBackend


class CRootDirTree(CDirTree):
    def __init__(self, base_path, root_fs_matcher: AbcFsMatcher = None, fs: BaseMetaFsBackendContract = None):
        super().__init__()
        self.__base_path = base_path
        self.__root_fs_matcher = root_fs_matcher
        if fs is None:
            fs = RealMetaFileSystemBackend().set_base_path(self.__base_path)
        self.__fs = fs
        self.__loaded = False

    @property
    def base_path(self):
        return self.__base_path

    def __list(self, parent: CDirTree, do_hash=False):
        assert isinstance(parent, CDirTree)
        path_names: List[str] = self.__fs.listdir(parent)
        parent_names: List[str] = parent.names
        for path_name in path_names:
            names = (*parent_names, path_name)
            child_cpath = CPath(names)
            if self.__fs.is_file(child_cpath):
                mtime = self.__fs.getmtime(child_cpath)
                child_cpath = CFile(names, mtime, self.__fs.getsize(child_cpath))

                if do_hash:
                    hash_value = self.__fs.gethash(child_cpath)
                    child_cpath = CFileHashed(child_cpath.names, child_cpath.mtime, child_cpath.size, hash_value)
            else:
                child_cpath = CDir(names)

            if self.__root_fs_matcher and self.__root_fs_matcher.exclude(child_cpath):
                continue
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
        return dumps(self.to_list())
