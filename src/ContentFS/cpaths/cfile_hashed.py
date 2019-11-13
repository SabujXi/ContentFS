from ContentFS.cpaths.cfile import CFile


class CFileHashed(CFile):
    def __init__(self, names, mtime, size, file_hash=None):
        super().__init__(names, mtime, size)
        self.__hash = file_hash

    @property
    def hash(self):
        return self.__hash

    def equals(self, another):
        return super().equals(another) and self.hash == another.hash

    def to_dict(self):
        dct = super().to_dict()
        dct['hash'] = self.hash
        return dct

