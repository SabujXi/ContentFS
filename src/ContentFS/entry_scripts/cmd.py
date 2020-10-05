import os
import sys
from ContentFS.ctrees.crootdirtree import CRootDirTree
from ContentFS.cpaths.cfile_hashed import CFileHashed


def main():
    args = sys.argv[1:]
    print(f'ARGS: {args}')
    base_path = os.getcwd()
    print(f'base_path: {base_path}')
    root = CRootDirTree(base_path)#.with_dev_matcher()
    if '--hash' in args:
        do_hash = True
    else:
        do_hash = False
    root.load(do_hash=do_hash)
    path_infos = []
    for cpath in root.get_descendant_cpaths():
        path_infos.append(f"-{'D' if cpath.is_dir() else 'F'}> {cpath.path}{'    [size(' + str(cpath.size) + ') mtime(' + str(cpath.mtime) + ')]' if cpath.is_file() else ''}{' - hash(' + cpath.hash + ')' if isinstance(cpath, CFileHashed) else ''}")
    for path_info in path_infos:
        print(path_info)


if __name__ == '__main__':
    main()

