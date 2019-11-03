import os
import re
from collections import OrderedDict
from json import dumps
from .ignorer import Ignorer
from .diff import Diff


class CPath:
    SPLIT_RE = re.compile(r'[/\\]+')
    @staticmethod
    def path_to_names(path_string):
        path_string = path_string.rstrip("/").rstrip("\\")
        path_string = path_string.replace("\\", "/")
        return CPath.SPLIT_RE.split(path_string)

    def __init__(self, names):
        self.__names = tuple(names)

    @property
    def name(self):
        return self.__names[-1]

    @property
    def names(self):
        return self.__names

    @property
    def path(self):
        return "/".join(self.__names)

    def is_file(self):
        raise NotImplemented()

    def is_dir(self):
        raise NotImplemented()

    def __str__(self):
        return "CPath: " + self.path

    def to_dict(self):
        return {
            'names': self.names
        }

    def to_path_dict(self):
        return {
            'path': self.path
        }

    def to_json(self):
        return dumps(self.to_dict())

    def to_path_json(self):
        return dumps(self.to_path_dict())

    def equals(self, another):
        return self.names == another.names


class CDir(CPath):
    def __init__(self, names):
        super().__init__(names)
        self._child_map = OrderedDict()

    def add_child(self, cpath: CPath):
        assert isinstance(cpath, CPath)
        assert cpath.names[:-1] == self.names, f"cpath.names {cpath.names} cpath.names[:-1] {cpath.names[:-1]}, self.names {self.names}"
        assert cpath.name not in self._child_map, "Cannot add a child twice"
        self._child_map[cpath.name] = cpath

    def find_child(self, name):
        return self._child_map.get(name, None)

    def has_child(self, name):
        return self.find_child(name) is not None

    def find_descendant(self, names):
        names = list(names)
        name = names.pop(0)
        child_cpath = self._child_map.get(name, None)
        if child_cpath is None:
            return None
        else:
            if len(names) == 0:
                return child_cpath
            else:
                return child_cpath.find_descendant(names)

    def get_or_create_descendant_cdir(self, names):
        # TODO: create unit test.
        if not names:
            return self

        _parent = self
        _target_names = list(names)
        _to_create_target_names = []
        # cdir = None
        while _target_names:
            _name = _target_names.pop(0)
            cdir = _parent.find_child(_name)
            if cdir is not None:
                _parent = cdir
                # break
            else:
                _to_create_target_names.append(_name)
                cdir = CDir([*_parent.names, *_to_create_target_names])
                _parent.add_child(cdir)
                _parent = cdir
                # continue
        # assert cdir is not None

        # while _to_create_target_names:
        #     name = _to_create_target_names.pop(0)
        #     new_child = CDir([*cdir.names, name])
        #     cdir.add_child(new_child)
        #     cdir = new_child
        return _parent

    def get_children(self):
        return tuple(self._child_map.values())

    def get_descendants(self):
        descendants = []
        for cpath in self.get_children():
            descendants.append(cpath)
            if cpath.is_dir():
                descendants.extend(cpath.get_descendants())
        return tuple(descendants)

    def is_file(self):
        return False

    def is_dir(self):
        return not self.is_file()

    def __str__(self):
        return super().__str__() + '\n' + str(self.get_children())

    def to_dict(self):
        dct = super().to_dict()
        dct['type'] = 'DIR'
        dct['children'] = tuple([child.to_dict() for child in self.get_children()])
        return dct

    def to_path_dict(self):
        pdct = super().to_path_dict()
        pdct['type'] = 'DIR'
        pdct['children'] = tuple([child.to_path_dict() for child in self.get_children()])
        return pdct

    def equals(self, another):
        return another.is_dir() and super().equals(another)


class CFile(CPath):
    def __init__(self, names, mtime, size, file_hash=None):
        super().__init__(names)
        self.__size = size
        self.__mtime = mtime
        self.__hash = file_hash

    @property
    def size(self):
        return self.__size

    @property
    def mtime(self):
        return self.__mtime

    @property
    def hash(self):
        return self.__hash

    def is_file(self):
        return True

    def is_dir(self):
        return not self.is_file()

    def equals(self, another):
        return another.is_file() and super().equals(another) and self.mtime == another.mtime and self.size == another.size

    def to_dict(self):
        dct = super().to_dict()
        dct['type'] = 'FILE'
        dct['mtime'] = self.mtime
        dct['size'] = self.size
        return dct

    def to_path_dict(self):
        pdct = super().to_path_dict()
        pdct['type'] = 'FILE'
        pdct['mtime'] = self.mtime
        pdct['size'] = self.size
        return pdct

    def __str__(self):
        return super().__str__()


class CRoot(CDir):
    def __init__(self, base_path, ignorer: Ignorer):
        super().__init__("")
        self.__base_path = base_path
        self.__ignorer = ignorer
        self.__loaded = False

    @property
    def base_path(self):
        return self.__base_path

    # def add_child(self, cpath: CPath):
    #     assert isinstance(cpath, CPath)
    #     assert cpath.name not in self._child_map, "Cannot add a child twice in root"
    #     self._child_map[cpath.name] = cpath

    def __list(self, parent):
        assert isinstance(parent, CDir)
        path_names = os.listdir(os.path.join(self.base_path, *parent.names))
        parent_names = parent.names
        for path_name in path_names:
            names = (*parent_names, path_name)
            abs_path = os.path.join(self.__base_path, *names)
            if os.path.isfile(abs_path):
                mtime = os.path.getmtime(abs_path)
                cpath = CFile(names, mtime, os.path.getsize(abs_path))
            else:
                cpath = CDir(names)

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

        diff_obj = Diff()

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
                child_cpath = CDir(names)
            parent_cdir.add_child(child_cpath)
        self.__loaded = True

    def to_dict(self):
        raise NotImplemented()

    def to_list(self):
        return [child.to_path_dict() for child in self.get_children()]

    def to_json(self):
        return dumps(self.to_list())

