from json import dumps

from ContentFS.cpaths.cpath import CPath
from ContentFS.cpaths.cdirtree import CDirTree
from ContentFS.cpaths.cfile import CFile
from ContentFS.cpaths.cfile_hashed import CFileHashed
from ContentFS.cdiff import CDiff
from ContentFS.pathmatch.fsignore import FsIgnorer as Ignorer
from ContentFS.contracts.meta_fs_backend_contract import BaseMetaFsBackendContract
from ContentFS.meta_fs_backends.real_fs_backend_meta import RealMetaFileSystemBackend


class CRootDirTree(CDirTree):
    def __init__(self, base_path, ignorer: Ignorer = None, fs: BaseMetaFsBackendContract = None):
        super().__init__("")
        self.__base_path = base_path
        self.__ignorer = ignorer
        if fs is None:
            fs = RealMetaFileSystemBackend()
        self.__fs = fs
        self.__fs.set_base_path(self.__base_path)
        self.__loaded = False

    @property
    def base_path(self):
        return self.__base_path

    def __list(self, parent: CPath, do_hash=False):
        assert isinstance(parent, CDirTree)
        path_names = self.__fs.listdir(parent)
        parent_names = parent.names
        for path_name in path_names:
            names = (*parent_names, path_name)
            child_cpath = CPath(names)
            if self.__fs.is_file(child_cpath):
                mtime = self.__fs.getmtime(child_cpath)
                cpath = CFile(names, mtime, self.__fs.getsize(child_cpath))

                if do_hash:
                    hash_value = self.__fs.gethash(cpath)
                    cpath = CFileHashed(cpath.names, cpath.mtime, cpath.size, hash_value)
            else:
                cpath = CDirTree(names)

            if self.__ignorer and self.__ignorer.ignore(cpath):
                continue
            if cpath.is_dir():
                self.__list(cpath, do_hash=do_hash)
            parent.add_child(cpath)

    def load(self, do_hash=False):
        if self.__loaded:
            raise Exception("Can load only once")
        self.__list(self, do_hash=do_hash)
        self.__loaded = True

    def diff(self, another_root):
        root1 = self
        root2 = another_root
        descendant_map1 = {}
        descendant_map2 = {}

        for cpath in root1.get_descendants():
            descendant_map1[cpath.path] = cpath

        for cpath in root2.get_descendants():
            descendant_map2[cpath.path] = cpath

        diff_obj = CDiff()

        for cpath1 in descendant_map1.values():
            path1 = cpath1.path
            if path1 not in descendant_map2:
                diff_obj.add_deleted(cpath1)
            else:
                cpath2 = descendant_map2[path1]
                if not cpath1.equals(cpath2):
                    diff_obj.add_modified(cpath1)

        for cpath2 in descendant_map2.values():
            path2 = cpath2.path
            if path2 not in descendant_map1:
                diff_obj.add_new(cpath2)

        return diff_obj

    def to_dict(self):
        raise NotImplemented()

    def to_list(self):
        return [child.to_dict() for child in self.get_children()]

    def to_json(self):
        return dumps(self.to_list())
