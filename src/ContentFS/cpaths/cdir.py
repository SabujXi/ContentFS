from ContentFS.cpaths.cpath import CPath


class CDir(CPath):
    def __init__(self, names):
        super().__init__(names)

    def is_file(self):
        return False

    def is_dir(self):
        return not self.is_file()

    def to_dict(self):
        dct = super().to_dict()
        return dct

    def equals(self, another):
        return another.is_dir() and self.names == another.names

    def __str__(self):
        return "CDir: " + self.path
