from typing import List, Tuple, Union, OrderedDict as OrderedDictType, Callable
from collections import OrderedDict, deque

from ContentFS.cpaths.cdir import CDir
from ContentFS.cpaths.cfile import CFile
from ContentFS.cpaths.cpath import CPath


class CDirTree:
    def __init__(self, names: Union[CDir, List[str], Tuple[str], List[bytes], Tuple[bytes], None] = None):
        """Pass names None when this tree is the root tree"""
        if names is None or isinstance(names, CDir):
            self._cdir = names
        else:
            self._cdir: CDir = CDir(names)

        self.__child_cfiles_map: OrderedDictType[str, CFile] = OrderedDict()
        self.__child_cdirs_tree_map: OrderedDictType[str, CDirTree] = OrderedDict()

    @property
    def is_root(self) -> bool:
        """Is root cannot have cdir"""
        return self._cdir is None

    @property
    def is_sub(self) -> bool:
        "Is sub tree"
        return not self.is_root

    @property
    def cdir(self) -> Union[CDir, None]:
        return self._cdir

    @property
    def is_empty(self) -> bool:
        return len(self.__child_cfiles_map) == 0 and len(self.__child_cdirs_tree_map)

    def _get_child_cfiles(self):
        return self.__child_cfiles_map.values()

    def _get_child_cdirs(self):
        return (tree.cdir for tree in self.__child_cdirs_tree_map.values())

    def _get_child_cdir_trees(self):
        return self.__child_cdirs_tree_map.values()

    def _get_child_tree(self, name: str) -> Union['CDirTree', None]:
        """
        Private method.
        """
        return self.__child_cdirs_tree_map.get(name, None)

    def _get_child_file(self, name: str) -> Union[CFile, None]:
        """
        Private method.
        """
        return self.__child_cfiles_map.get(name, None)

    def _add_child(self, cpath: CPath) -> 'CDirTree':
        """
        Caution: this method does not check whether cpath belongs as 'child'
            This is a private method, never use it without knowing what you are doing, and must use this internally.
        """
        tree = self
        if isinstance(cpath, CFile):
            self.__child_cfiles_map[cpath.name] = cpath
        else:
            assert isinstance(cpath, CDir), "Programmer's Error"
            tree = CDirTree(cpath)
            self.__child_cdirs_tree_map[cpath.name] = tree
        return tree

    def add(self, cpath: CPath) -> 'CDirTree':
        """
        Add any level of descedents
        """
        assert isinstance(cpath, CPath)
        assert not isinstance(cpath, CDirTree)
        assert cpath.names[:-1] == self._cdir.names, f"cpath.names {cpath.names} cpath.names[:-1] {cpath.names[:-1]}, self.names {self.names}"
        assert cpath.is_rel, "Cannot add absolute path to a tree"
        assert cpath.names_count > self._cdir.names_count
        # assert cpath.name not in self._child_map, "Cannot add a child twice" TODO: think later whether this old check will be added in the new add check

        comp_left_names = deque(cpath.names[:self._cdir.names_count])
        comp_right_names = deque(cpath.names[self._cdir.names_count:])
        assert comp_left_names == self._cdir.names, "Root didn't match"

        target_tree = self
        _inc_right_names = []
        for dir_comp_name in comp_right_names[:-1]:
            _inc_right_names.append(dir_comp_name)
            new_target = target_tree._get_child_tree(dir_comp_name)
            if new_target is None:
                new_target = target_tree._add_child(CDir([*comp_left_names, *_inc_right_names]))
            target_tree = new_target
        target_tree._add_child(cpath)

        return target_tree

    def get(self, names: Union[CPath, List[str]]) -> Union[CFile, CDir, None]:
        if isinstance(names, CPath):
            names = names.names
        target_tree = self
        for name in names[:-1]:
            new_target = target_tree._get_child_tree(name)
            if new_target is None:
                return None
            target_tree = new_target

        if target_tree._get_child_file(names[-1]) is not None:
            return target_tree._get_child_file(names[-1])
        elif target_tree._get_child_tree(names[-1]) is not None:
            return target_tree._get_child_tree(names[-1])._cdir
        else:
            return None

    def exists(self, names: Union[CPath, List[str]]) -> bool:
        return True if self.get(names) is not None else False

    def visit(self, visitor_callable: Callable[[Union[CFile, CDir], bool, 'CDirTree'], None], depth_first=True):
        for tree in self._get_child_cdir_trees():
            # for cdir & cdirs
            cdir = tree.cdir
            if tree.is_empty:
                visitor_callable(cdir, True, tree) #cdir, is_leaf, cdir_tree
            else:
                if depth_first:
                    tree.visit(visitor_callable, depth_first=depth_first)
                    # in depth first current dir will be visited after all the depts are complete
                    visitor_callable(cdir, False, tree)  # cdir, is_leaf, cdir_tree
                else:
                    # in non depth first it will be visited before descendants
                    visitor_callable(cdir, False, tree)  # cdir, is_leaf, cdir_tree
                    tree.visit(visitor_callable, depth_first=depth_first)

            # for cfiles
            for cfile in tree._get_child_cfiles():
                visitor_callable(cfile, True, tree)  # cdir, is_leaf, cdir_tree

    def get_children(self):
        return tuple([*self._get_child_cdirs(), *self._get_child_cfiles()])

    def get_descendants(self):
        descendants = []

        def descendant_visitor(cpath: Union[CFile, CDir], is_leaf: bool, cdir_tree: 'CDirTree') -> None:
            descendants.append(cpath)
        return tuple(descendants)

    def __str__(self):
        return super().__str__() + '\n' + str(self.get_children())

    def to_dict(self):
        dct = self.cdir.to_dict()
        dct['children'] = tuple([child.to_dict() for child in self.get_children()])
        return dct

    def equals(self, another: 'CDirTree'):
        # TODO: should implement recursive child matching?
        return another.cdir.is_dir() and self.cdir.names == another.cdir.names
