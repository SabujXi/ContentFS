import enum


class CPathType(enum.Enum):
    DIR = 'DIR'
    FILE = 'FILE'

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'CPathType.{self.name}'

    def is_dir(self) -> bool:
        return self == CPathType.DIR

    def is_file(self):
        return self == CPathType.FILE

    @classmethod
    def get_type(cls, is_dir: bool):
        if is_dir:
            return cls.DIR
        return cls.FILE
