from collections import OrderedDict

from ContentFS.cpaths.cpath import CPath


class CTree(CPath):
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
                cdir = CTree([*_parent.names, *_to_create_target_names])
                _parent.add_child(cdir)
                _parent = cdir
                # continue
        # assert cdir is not None

        # while _to_create_target_names:
        #     name = _to_create_target_names.pop(0)
        #     new_child = CTree([*cdir.names, name])
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
        dct['children'] = tuple([child.to_dict() for child in self.get_children()])
        return dct

    def to_path_dict(self):
        pdct = super().to_path_dict()
        pdct['type'] = 'DIR'
        pdct['children'] = tuple([child.to_path_dict() for child in self.get_children()])
        return pdct

    def equals(self, another):
        return another.is_dir() and super().equals(another)