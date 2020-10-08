from typing import Union
from ContentFS.cpaths.cpath import CPath


class CDir(CPath):
    def __init__(self, names):
        super().__init__(names, True)

    # HELPER METHODS for ancestor/descendant
    def get_parent(self) -> Union['CDir', None]:
        cpath_info = self.get_cpath_info()
        if not cpath_info.has_parent():
            return None
        return CDir(cpath_info.get_parent())

    # HELPER METHODS
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
