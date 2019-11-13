from ContentFS.cpaths.cpath import CPath


class CFile(CPath):
    def __init__(self, names, mtime, size, file_hash=None):
        super().__init__(names)
        self.__size = size
        self.__mtime = mtime
        self.__hash = file_hash

    @property
    def size(self):
        return self.__size

    @property
    def mtime(self):
        return self.__mtime

    @property
    def hash(self):
        return self.__hash

    def is_file(self):
        return True

    def is_dir(self):
        return not self.is_file()

    def equals(self, another):
        return another.is_file() and super().equals(another) and self.mtime == another.mtime and self.size == another.size

    def to_dict(self):
        dct = super().to_dict()
        dct['type'] = 'FILE'
        dct['mtime'] = self.mtime
        dct['size'] = self.size
        return dct

    def to_path_dict(self):
        pdct = super().to_path_dict()
        pdct['type'] = 'FILE'
        pdct['mtime'] = self.mtime
        pdct['size'] = self.size
        return pdct

    def __str__(self):
        return super().__str__()