from typing import Union
from ContentFS.cpaths import CPath, CDir
from ContentFS.exceptions import CFSExceptionInvalidPathName


class CFile(CPath):
    def __init__(self, names, mtime, size):
        super().__init__(names, is_dir=False)
        self.__size = size
        self.__mtime = mtime

    # FUNDAMENTAL METHODS
    @property
    def size(self):
        return self.__size

    @property
    def mtime(self):
        return self.__mtime

    # HELPER METHODS for ancestor/descendant
    def get_parent(self) -> Union['CDir', None]:
        cpath_info = self.get_cpath_info()
        if not cpath_info.has_parent():
            return None
        return CDir(cpath_info.get_parent())

    # HELPER METHODS
    def equals(self, another):
        return super().equals(another) and\
               self.size == another.size and \
               self.mtime == another.mtime

    def equals_with_size(self, another):
        return self.equals_by_path_only(another) and self.size == another.size

    def equals_with_size_timestamp(self, another: 'CFile'):
        """Equality by timestamp and size"""
        return self.get_type() == another.get_type() and self.is_rel == another.is_rel and self.size == another.size and self.mtime == another.mtime

    def to_dict(self):
        dct = super().to_dict()
        dct['mtime'] = self.mtime
        dct['size'] = self.size
        return dct

    def __str__(self):
        return super().__str__()
