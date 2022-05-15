import json
import os
import os.path
from ContentFS.cpaths.cpath import CPath
from ContentFS.cpaths.cdir import CDir
from ContentFS.cpaths.cfile import CFile
from ContentFS.cpaths.cfile_hashed import CFileHashed
from ContentFS.ctrees.cdirtree import CDirTree
from ContentFS.contracts.meta_fs_backend_contract import BaseMetaFsBackendContract
from ContentFS.exceptions import CFSException, CFSPathDoesNotExistException
from typing import Callable
from typing import List


def visit_fs_dictz(dict_list: List[dict], visitor_callable: Callable[[dict], None]):
    """
    Depth first visitor
    :param dict_list: list of dicts where the dicts are cpath serialized dict with addition that when it is dir, it can contain children
    :param visitor_callable: callback for what?
    """
    for path_dict in dict_list:
        visitor_callable(path_dict)
        if path_dict['type'] == 'DIR':
            if path_dict['children']:
                # recurse
                visit_fs_dictz(path_dict['children'], visitor_callable)


class DictMetaFileSystemBackend(BaseMetaFsBackendContract):
    def __init__(self, cpath_tree_dict: dict):
        self.__cpath_tree_dict = cpath_tree_dict
        self.__dict_list = self.__cpath_tree_dict['cpaths']

        self.__cdir_tree = CDirTree()

        self.__base_path = None

        # build the cdir tree
        def json_visitor_callable(path_dict):
            if path_dict['type'] == 'DIR':
                cpath = CDir(path_dict['names'])
            else:
                assert path_dict['type'] == 'FILE'
                if path_dict.get('hash', None) is None:
                    cpath = CFile(path_dict['names'], path_dict['mtime'], path_dict['size'])
                else:
                    cpath = CFileHashed(path_dict['names'], path_dict['mtime'], path_dict['size'], path_dict['hash'])

            self.__cdir_tree.add(cpath)

        visit_fs_dictz(self.__dict_list, json_visitor_callable)

    def _get_dict_list(self):
        """
        Currently used for testing purpose only.
        """
        return tuple(self.__dict_list)

    def set_base_path(self, base_path: str):
        # Should I restrict to setting only once???
        self.__base_path = base_path
        return self

    @property
    def base_path(self):
        bp = self.__base_path
        assert bp is not None
        return bp

    def _full_path(self, cpath: CPath):
        return os.path.join(self.base_path, cpath.path)

    def exists(self, cpath: CPath):
        """Does not care what you pass, cdir or cfile - it does not check the type of the path"""
        inside_cpath = self.__cdir_tree.get(cpath, path_type_aware=False)
        return inside_cpath is not None

    def is_file(self, cpath: CPath):
        inside_cpath = self.__cdir_tree.get(cpath)
        if inside_cpath is None:
            raise CFSPathDoesNotExistException(
                f'Meta File System Error (occurred during checking if the cpath is a file cpath {cpath}):\n'
                f'X path does not exist'
            )
        else:
            if inside_cpath.is_file():
                return True
            else:
                return False

    def is_dir(self, cpath: CPath):
        return not self.is_file(cpath)

    def listdir(self, cpath: CPath) -> List[str]:
        if cpath.names_count > 0:
            sub_tree = self.__cdir_tree.get_sub_tree(cpath)
        else:
            sub_tree = self.__cdir_tree

        if sub_tree is None:
            return []
        else:
            children_cpaths = sub_tree.get_children_cpaths()
            return list(cpath.name for cpath in children_cpaths)

        # TODO: throw exceptions accordingly
        # if inside_cpath is None:
        #     raise CFSException(
        #         f'File System Error (occurred during listing cpath: {cpath}):\n'
        #         f'X Path does not exist'
        #     )
        # if inside_cpath.is_file():
        #     raise CFSException(
        #         f'File System Error (occurred during listing cpath: {cpath}):\n'
        #         f'X Cannot list on file'
        #     )

    def getmtime(self, cpath: CPath):
        inside_cpath = self.__cdir_tree.get(cpath)
        if inside_cpath is None:
            raise CFSException(
                f'File System Error (occurred during getmtime on cpath: {cpath}):\n'
                f'X Path does not exist'
            )

        if inside_cpath.is_dir() or cpath.is_dir():
            raise CFSException(
                f'File System Error (occurred during getmtime on cpath: {cpath}):\n'
                f'X gmtime on dir'
            )

        return inside_cpath.mtime

    def getsize(self, cpath: CPath):
        inside_cpath = self.__cdir_tree.get(cpath)

        if inside_cpath is None:
            raise CFSException(
                f'File System Error (occurred during gethash on cpath: {cpath}):\n'
                f'X Path not found'
            )

        if cpath.is_dir() or inside_cpath.is_dir():
            raise CFSException(
                f'File System Error (occurred during getsize on cpath: {cpath}):\n'
            )

        return inside_cpath.size

    def gethash(self, cpath: CPath):
        inside_cpath: CFileHashed = self.__cdir_tree.get(cpath)

        if inside_cpath is None:
            raise CFSException(
                f'File System Error (occurred during gethash on cpath: {cpath}):\n'
                f'X Path not found'
            )

        if not cpath.is_file() or not inside_cpath.is_file():
            raise CFSException(
                f'File System Error (occurred during gethash on cpath: {cpath}):\n'
                f'get hash can only be used on Files'
            )

        if not isinstance(inside_cpath, CFileHashed):
            raise CFSException(
                f'File System Error (occurred during gethash on cpath: {cpath}):\n'
                f'X file was not hashed'
            )

        return cpath.hash

    def is_real_fs(self):
        # this is not a real fs
        return False
