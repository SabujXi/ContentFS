import os
from ContentFS.cpaths.crootdirtree import CRootDirTree
from ContentFS.meta_fs_backends.real_fs_backend_meta import RealMetaFileSystemBackend
from ContentFS.pathmatch.fsignore import FsIgnorer


def main():
    base_path = os.getcwd()
    print(f'base_path: {base_path}')
    root = CRootDirTree(base_path)
    root.load()
    print(root.to_json())
