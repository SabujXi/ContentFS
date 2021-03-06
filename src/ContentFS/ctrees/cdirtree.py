from typing import List, Tuple, Union, OrderedDict as OrderedDictType, Callable, Iterable
from collections import OrderedDict, deque

from ContentFS.cpaths.cdir import CDir
from ContentFS.cpaths.cfile import CFile
from ContentFS.cpaths.cpath import CPath
from ContentFS.exceptions import CFSException


class CDirTree(CDir):
    def __init__(self, names: Union[CDir, str, bytes, List[str], Tuple[str, ...], List[bytes], Tuple[bytes, ...]] = ""):
        super().__init__(names)
        self.__child_cfiles_map: OrderedDictType[str, CFile] = OrderedDict()
        self.__child_cdirs_tree_map: OrderedDictType[str, CDirTree] = OrderedDict()

    def is_sub(self) -> bool:
        "Is sub tree"
        return not self.is_root()

    @property
    def as_cdir(self) -> Union[CDir, None]:
        return CDir(self.names)

    @property
    def is_empty(self) -> bool:
        return len(self.__child_cfiles_map) == 0 and len(self.__child_cdirs_tree_map) == 0

    def _get_child_cfiles(self) -> Iterable[CFile]:
        return self.__child_cfiles_map.values()

    def _get_child_cdirs(self) -> Iterable[CDir]:
        return (tree.as_cdir for tree in self.__child_cdirs_tree_map.values())

    def _get_child_cdir_trees(self) -> Iterable['CDirTree']:
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
        # if cpath.name in self.__child_cdirs_tree_map or cpath.name in self.__child_cfiles_map:
        #     raise CFSException("Cannot add path twice - it's not a replace operation")
        tree = self
        if isinstance(cpath, CFile):
            if cpath.name in self.__child_cfiles_map:
                raise CFSException(f"Cannot add child twice: {cpath.path}")  # TODO: appropriate new exception

            self.__child_cfiles_map[cpath.name] = cpath
        else:
            assert isinstance(cpath, CDir), f"Programmer's Error, passed type: {type(cpath)}"
            if cpath.name in self.__child_cdirs_tree_map:
                raise CFSException(f"Cannot add child twice: {cpath.path}")  # TODO: appropriate new exception

            tree = CDirTree(cpath)
            self.__child_cdirs_tree_map[cpath.name] = tree
        return tree

    def add(self, cpath: CPath) -> 'CDirTree':
        """
        Add any level of descendents
        :returns: last sub tree
        """
        assert isinstance(cpath, CPath)
        assert not isinstance(cpath, CDirTree)
        assert cpath.is_rel, "Cannot add absolute path to a tree"
        if cpath.is_dir():
            cdir: CDir = cpath
            assert not cdir.is_root(), f"Programmer's Error - cannot add root dir to a tree or sub tree: {cdir.to_dict()}"
        assert cpath.names_count > self.names_count
        if not self.is_root():
            assert cpath.names[:self.names_count] == self.names, f"cpath.names {cpath.names} cpath.names[:self.names_count] {cpath.names[:self.names_count]}, self.names {self.names}"
        # assert cpath.name not in self._child_map, "Cannot add a child twice" TODO: think later whether this old check will be added in the new add check

        comp_left_names = tuple(cpath.names[:self.names_count])
        comp_right_names = tuple(cpath.names[self.names_count:])
        assert comp_left_names == self.names, f"Root didn't match: {comp_left_names} <-> {self.names}"
        self_own_names = comp_left_names

        target_tree = self  # target tree is the tree where the cpath will be added as child
        _inc_right_names = []  # adding right names one by one for testing existence and adding to the tree.
        for dir_comp_name in comp_right_names[:-1]:
            _inc_right_names.append(dir_comp_name)
            new_target = target_tree._get_child_tree(dir_comp_name)

            if new_target is None:
                new_target = target_tree._add_child(CDir([*self_own_names, *_inc_right_names]))
            target_tree = new_target  # After the first time of writing this line I indented this one level forward and
            # there was bugs of duplicate dir in visit, I remember when I indented this one. First time ok,
            # second time wrong, now okay
        last_tree = target_tree._add_child(cpath)

        return last_tree

    def _get(self, path: Union[CPath, str, List[str], Tuple[str, ...]]) -> Union[CFile, 'CDirTree', None]:
        """
        It will return tree (not cdir), cfile or None
        """
        _orig_path = path
        if isinstance(path, CPath):
            cpath: CPath = path
            if self.is_root():
                names = cpath.names
            else:
                l = self.names
                r = cpath.names[:self.names_count]
                if cpath.names_count > self.names_count and l == r:
                    names = cpath.names[self.names_count:]
                else:
                    return None
                    # raise CFSException(f"Not a match bro!!! l {l} r {r}")
        else:
            assert isinstance(path, (list, tuple))
            names = CPath.to_cpath_info(path).names

        assert len(names) > 0, "Programmer's Error"

        target_tree = self
        for name in names[:-1]:
            new_target = target_tree._get_child_tree(name)
            if new_target is None:
                return None
            target_tree = new_target

        if target_tree._get_child_file(names[-1]) is not None:
            ret_cpath = target_tree._get_child_file(names[-1])
        elif target_tree._get_child_tree(names[-1]) is not None:
            ret_cpath = target_tree._get_child_tree(names[-1])  # returning the tree
        else:
            ret_cpath = None
        return ret_cpath

    def get(self, path: Union[CPath, str, List[str], Tuple[str, ...]], path_type_aware: bool = True) -> Union[CFile, CDir, None]:
        """
        # TODO: add support for CPathInfo as path.
        Pass a list of path comps/str path to act relatively to this tree/subtree
        Pass CPath to start from the root, yeah...

        When it is path type aware then it will check for the type of the path
        If the type is pure CPath then it will not check the type, if it is instance of cfile or cdir then it is sensitive when path_type_aware is set to true
        """
        _orig_path = path
        ret_cpath = self._get(path)
        # when this query is path type aware and not string (or string array or etc) neither concrete CPath is passed
        if ret_cpath is not None:
            if path_type_aware and isinstance(_orig_path, (CFile, CDir)):
                if _orig_path.get_type() != ret_cpath.get_type():
                    ret_cpath = None  # baat laga diya - stored cpath and passed cpath are not of the same type
        if type(ret_cpath) is CDirTree:
            ret_cpath = ret_cpath.as_cdir
        return ret_cpath

    def get_sub_tree(self, names: Union[CPath, List[str]]) -> Union['CDirTree', None]:
        ret_tree = self._get(names)
        if type(ret_tree) is CDirTree:
            ret_tree = None
        return ret_tree

    def exists(self, names: Union[CPath, List[str], Tuple[str, ...]]) -> bool:
        return True if self.get(names) is not None else False

    def visit(self, visitor_callable: Callable[[Union[CFile, CDir], bool, 'CDirTree'], None], depth_first=True):
        if depth_first:
            # for cfiles for condition 1
            for cfile in self._get_child_cfiles():
                visitor_callable(cfile, True, self)  # cdir, is_leaf, cdir_tree

        for tree in self._get_child_cdir_trees():
            # for cdir & cdirs
            # if tree.is_empty:
            #     visitor_callable(tree.as_cdir, True, tree) #cdir, is_leaf, cdir_tree
            # else:
            is_leaf = True if tree.is_empty else False

            if depth_first:
                tree.visit(visitor_callable, depth_first=depth_first)
                # in depth first current dir will be visited after all the depts are complete
                visitor_callable(tree.as_cdir, is_leaf, tree)  # cdir, is_leaf, cdir_tree
            else:
                # in non depth first it will be visited before descendants
                visitor_callable(tree.as_cdir, is_leaf, tree)  # cdir, is_leaf, cdir_tree
                tree.visit(visitor_callable, depth_first=depth_first)

        if not depth_first:
            # for cfiles for condition 2
            for cfile in self._get_child_cfiles():
                visitor_callable(cfile, True, self)  # cdir, is_leaf, cdir_tree

    def get_children(self) -> List[Union['CDirTree', CFile]]:
        """
        CDirTree (not CDir - because that will not return inner children) & CFile
        """
        return list(self._get_child_cdir_trees()) + list(self._get_child_cfiles())

    def get_children_cpaths(self) -> List[Union[CDir, CFile]]:
        return list(self._get_child_cdirs()) + list(self._get_child_cfiles())

    def get_descendant_cpaths(self) -> Tuple[CPath, ...]:
        descendants: List[CPath] = []

        def descendant_visitor(cpath: Union[CFile, CDir], is_leaf: bool, cdir_tree: 'CDirTree') -> None:
            descendants.append(cpath)

        self.visit(descendant_visitor, depth_first=False)
        return tuple(descendants)

    def get_leaves(self) -> Tuple[CPath, ...]:
        # TODO: write test
        descendant_leaves: List[CPath] = []

        def leaves_descendant_visitor(cpath: Union[CFile, CDir], is_leaf: bool, cdir_tree: 'CDirTree') -> None:
            if is_leaf:
                descendant_leaves.append(cpath)
        self.visit(leaves_descendant_visitor, depth_first=False)
        return tuple(descendant_leaves)

    def diff(self, another: 'CDirTree'):
        root1 = self
        root2 = another
        descendant_map1 = {}
        descendant_map2 = {}

        for cpath in root1.get_descendant_cpaths():
            descendant_map1[cpath.path] = cpath

        for cpath in root2.get_descendant_cpaths():
            descendant_map2[cpath.path] = cpath

        diff_obj = CDirTreeDiff()

        for cpath1 in descendant_map1.values():
            path1 = cpath1.path
            if path1 not in descendant_map2:
                diff_obj.deleted.add(cpath1)
            else:
                cpath2 = descendant_map2[path1]
                if not cpath1.equals(cpath2):
                    diff_obj.modified.add(cpath1)

        for cpath2 in descendant_map2.values():
            path2 = cpath2.path
            if path2 not in descendant_map1:
                diff_obj.new.add(cpath2)

        return diff_obj

    def __bool__(self):
        return self.__len__() > 0

    def __len__(self):
        return len(self.__child_cfiles_map) + len(self.__child_cdirs_tree_map)

    def __str__(self):
        return super().__str__() + '\n' + str(self.get_children())

    def to_dict(self):
        # TODO: unittest
        dct = self.as_cdir.to_dict()
        dct['children'] = tuple([child.to_dict() for child in self.get_children()])  # json has list not tuple, that makes unittesting equality of to json and to dict problematic
        return dct

    def equals(self, another: 'CDirTree'):
        # TODO: should implement recursive child matching?
        # TODO: unittest
        raise NotImplemented("Equality checking of tree should be recursive. Do later.")
        # return another.is_dir() and self.names == another.names


class CDirTreeDiff:
    def __init__(self):
        self.__deleted: CDirTree = CDirTree()
        self.__modified: CDirTree = CDirTree()
        self.__new: CDirTree = CDirTree()

    @property
    def deleted(self) -> CDirTree:
        return self.__deleted

    @property
    def modified(self) -> CDirTree:
        return self.__modified

    @property
    def new(self) -> CDirTree:
        return self.__new

    def changed(self) -> bool:
        return any([self.__modified, self.__deleted, self.__new])

    def __bool__(self):
        return self.changed()

    def to_dict(self) -> dict:
        return {
            'deleted': self.__deleted.to_dict(),
            'modified': self.__modified.to_dict(),
            'new': self.__new.to_dict()
        }
