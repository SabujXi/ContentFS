import os
from json import dumps

from ContentFS.cpaths.cpath import CPath
from ContentFS.cpaths.cdirtree import CDirTree
from ContentFS.cpaths.cfile import CFile
from ContentFS.cdiff import CDiff
from ContentFS.ignorer import Ignorer
from ContentFS.contracts.meta_fs_backend_contract import BaseMetaFsBackendContract


class CRootDirTree(CDirTree):
    def __init__(self, base_path, ignorer: Ignorer, fs: BaseMetaFsBackendContract):
        super().__init__("")
        self.__base_path = base_path
        self.__ignorer = ignorer
        self.__fs = fs
        self.__loaded = False

    @property
    def base_path(self):
        return self.__base_path

    def __list(self, parent: CPath):
        assert isinstance(parent, CDirTree)
        path_names = self.__fs.listdir(parent)
        parent_names = parent.names
        for path_name in path_names:
            names = (*parent_names, path_name)
            child_cpath = CPath(names)
            if self.__fs.is_file(child_cpath):
                mtime = self.__fs.getmtime(child_cpath)
                cpath = CFile(names, mtime, self.__fs.getsize(child_cpath))
            else:
                cpath = CDirTree(names)

            if self.__ignorer.ignore(cpath):
                continue

            if cpath.is_dir():
                self.__list(cpath)
            parent.add_child(cpath)

    def load(self):
        if self.__loaded:
            raise Exception("Can load only once")
        self.__list(self)
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

    def load_from_path_dicts(self, paths_dict_list):
        if self.__loaded:
            raise Exception("Can load only once")

        for path_dict in paths_dict_list:
            child_dict = path_dict
            path = child_dict['path']
            names = self.path_to_names(path)

            # print(f"Path       : {path}")
            parent_cdir = self.get_or_create_descendant_cdir(names[:-1])
            # print(f"Parent Path: {parent_cdir.path}")
            type = child_dict['type']
            if type == 'FILE':
                mtime = child_dict['mtime']
                size = child_dict['size']
                child_cpath = CFile(names, mtime, size)
            else:
                child_cpath = CDirTree(names)
            parent_cdir.add_child(child_cpath)
        self.__loaded = True

    def to_dict(self):
        raise NotImplemented()

    def to_list(self):
        return [child.to_dict() for child in self.get_children()]

    def to_json(self):
        return dumps(self.to_list())
