from ContentFS.cpaths.cpath import CPath


class CFile(CPath):
    def __init__(self, names, mtime, size):
        super().__init__(names)
        self.__size = size
        self.__mtime = mtime

    @property
    def size(self):
        return self.__size

    @property
    def mtime(self):
        return self.__mtime

    def is_file(self):
        return True

    def is_dir(self):
        return not self.is_file()

    def equals(self, another):
        return self.equals_by_size_timestamp(another)

    def equals_by_size(self, another):
        return self.equals_by_path(another) and self.size == another.size

    def equals_by_size_timestamp(self, another):
        """Equality by timestamp and size"""
        return self.equals_by_size(another) and self.mtime == another.mtime

    def to_dict(self):
        dct = super().to_dict()
        dct['mtime'] = self.mtime
        dct['size'] = self.size
        return dct

    def __str__(self):
        return super().__str__()
