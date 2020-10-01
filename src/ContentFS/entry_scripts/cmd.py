import os
import sys
from ContentFS.ctrees.crootdirtree import CRootDirTree


def main():
    args = sys.argv[1:]
    print(f'ARGS: {args}')
    base_path = os.getcwd()
    print(f'base_path: {base_path}')
    root = CRootDirTree(base_path)
    if '--hash' in args:
        do_hash = True
    else:
        do_hash = False
    root.load(do_hash=do_hash)
    print(root.to_json())
