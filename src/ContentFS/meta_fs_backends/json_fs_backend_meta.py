import json
import os
import os.path
from ContentFS.cpaths.cpath import CPath
from ContentFS.cpaths.cdir import CDir
from ContentFS.cpaths.cfile import CFile
from ContentFS.cpaths.cfile_hashed import CFileHashed
from ContentFS.ctrees.cdirtree import CDirTree
from ContentFS.contracts.meta_fs_backend_contract import BaseMetaFsBackendContract
from ContentFS.exceptions import CFSException
from typing import Callable


def visit_json_fs(json_list: list, visitor_callable: Callable[[dict, bool], None]):
    """
    Depth first visitor
    """
    for json_dict in json_list:
        if json_dict['type'] == 'DIR':
            if json_dict['children']:
                # recurse
                visit_json_fs(json_dict['children'], visitor_callable)
                visitor_callable(json_dict, False)
            else:
                visitor_callable(json_dict, True)
        else:
            visitor_callable(json_dict, True)


class JsonMetaFileSystemBackend(BaseMetaFsBackendContract):
    def __init__(self, json_text):
        self.__json_text = json_text
        self.__json_list = json.loads(json_text)

        self.__cdir_tree = CDirTree()

        self.__base_path = None

        # build the cdir tree
        def json_visitor_callable(path_dict, is_leaf: bool):
            if path_dict['type'] == 'DIR':
                cpath = CDir(path_dict['names'])
            else:
                assert path_dict['type'] == 'FILE'
                if path_dict.get('hash', None):
                    cpath = CFile(path_dict['names'], path_dict['mtime'], path_dict['msize'])
                else:
                    cpath = CFileHashed(path_dict['names'], path_dict['mtime'], path_dict['msize'], path_dict['hash'])

            self.__cdir_tree.add(cpath)

        visit_json_fs(self.__json_list, json_visitor_callable)

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
        inside_cpath = self.__cdir_tree.get(cpath)
        return inside_cpath is not None

    def is_file(self, cpath: CPath):
        inside_cpath = self.__cdir_tree.get(cpath)
        if inside_cpath is None:
            raise CFSException(
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

    def listdir(self, cpath: CPath):
        inside_cpath = self.__cdir_tree.get(cpath)
        if inside_cpath is None:
            raise CFSException(
                f'File System Error (occurred during listing cpath: {cpath}):\n'
                f'X Path does not exist'
            )
        if inside_cpath.is_file():
            raise CFSException(
                f'File System Error (occurred during listing cpath: {cpath}):\n'
                f'X Cannot list on file'
            )
        return self.__cdir_tree.get_children_cpaths()

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
