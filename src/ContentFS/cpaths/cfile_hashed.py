from ContentFS.cpaths.cfile import CFile
from ContentFS.exceptions import CFSException, CFSExceptionFileHashSizeMismatch


class CFileHashed(CFile):
    def __init__(self, names, mtime, size, file_hash):
        if len(file_hash) != 40:
            raise CFSExceptionFileHashSizeMismatch(
                f'file hash hex string must be of size 40 (sha1), length {len(file_hash)} found with the value of {file_hash}'
            )
        super().__init__(names, mtime, size)
        self.__hash = file_hash

    @property
    def hash(self):
        return self.__hash

    def equals(self, another):
        return self.equals_by_hash(another)

    def equals_by_hash(self, another):
        return self.equals_by_path(another) and self.hash == another.hash

    def to_dict(self):
        dct = super().to_dict()
        dct['hash'] = self.hash
        return dct

