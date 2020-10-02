from ContentFS.cpaths.cpath import CPath


class CDir(CPath):
    def __init__(self, names):
        super().__init__(names, True)

    def is_file(self):
        return False

    def is_dir(self):
        return not self.is_file()

    def is_root(self) -> bool:
        return self.names_count == 0

    def to_dict(self):
        dct = super().to_dict()
        return dct

    def equals(self, another):
        return self.equals_by_path(another)

    def __str__(self):
        return "CDir: " + self.path
