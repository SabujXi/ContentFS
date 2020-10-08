import enum


class CPathType(enum.Enum):
    DIR = 'DIR'
    FILE = 'FILE'

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'CPathType.{self.name}'
