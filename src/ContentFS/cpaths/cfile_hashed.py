from ContentFS.cpaths import CPath, CFile
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

    def equals(self, another: 'CFileHashed') -> bool:
        """Equals without considering mtime"""
        # TODO: unittest
        return self.equals_wo_mtime_size(another)

    def equals_by_hash_only(self, another: 'CFileHashed') -> bool:
        # TODO: unittest
        if not isinstance(another, CFileHashed):
            return False
        return self.hash == another.hash

    def equals_wo_mtime_size(self, another: 'CFileHashed') -> bool:
        if not isinstance(another, CFileHashed):
            return False
        return self.get_type() == another.get_type() and \
               self.is_rel == another.is_rel and \
               self.names == another.names and \
               self.hash == another.hash

    def equals_wo_mtime(self, another: 'CFileHashed') -> bool:
        # TODO: unittest
        return self.equals_wo_mtime_size(another) and \
               self.size == another.size

    def to_dict(self):
        dct = super().to_dict()
        dct['hash'] = self.hash
        return dct

