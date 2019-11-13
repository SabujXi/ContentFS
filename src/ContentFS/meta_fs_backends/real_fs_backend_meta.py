import os
import os.path
import hashlib
from ContentFS.cpaths.cpath import CPath
from ContentFS.contracts.meta_fs_backend_contract import BaseMetaFsBackendContract
from ContentFS.exceptions import CFSException


class MetaFileSystemBackend(BaseMetaFsBackendContract):
    def exists(self, cpath: CPath):
        try:
            res = os.path.exists(cpath.path)
        except (OSError, IOError) as e:
            raise CFSException(
                f'Meta File System Error (occurred during exists() on cpath {cpath}):\n'
                f'{str(e)}'
            )
        return res

    def is_file(self, cpath: CPath):
        try:
            res = os.path.isfile(cpath.path)
        except (OSError, IOError) as e:
            raise CFSException(
                f'Meta File System Error (occurred during checking if the cpath is a file cpath {cpath}):\n'
                f'{str(e)}'
            )
        return res

    def is_dir(self, cpath: CPath):
        try:
            res = os.path.isdir(cpath.path)
        except (OSError, IOError) as e:
            raise CFSException(
                f'File System Error (occurred during checking if the cpath is a directory cpath {cpath}):\n'
                f'{str(e)}'
            )
        return res

    def listdir(self, cpath: CPath):
        try:
            res = os.listdir(cpath.path)
        except (OSError, IOError) as e:
            raise CFSException(
                f'File System Error (occurred during listing cpath: {cpath}):\n'
                f'{str(e)}'
            )
        return res

    def getmtime(self, cpath: CPath):
        try:
            res = os.path.getmtime(cpath.path)
        except (OSError, IOError) as e:
            raise CFSException(
                f'File System Error (occurred during getmtime on cpath: {cpath}):\n'
                f'{str(e)}'
            )
        return res

    def gethash(self, cpath: CPath):
        if not cpath.is_file():
            raise CFSException(
                f'File System Error (occurred during gethash on cpath: {cpath}):\n'
                f'get hash can only be used on Files'
            )
        try:
            BLOCKSIZE = 65536
            hasher = hashlib.sha1()
            with open(cpath.path, 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            res = hasher.hexdigest()
        except (OSError, IOError) as e:
            raise CFSException(
                f'File System Error (occurred during gethash on cpath: {cpath}):\n'
                f'{str(e)}'
            )
        return res
