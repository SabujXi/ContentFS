from .fsmatchers import FsMatcherGitignore, UniMetaFsIncluder, UniMetaFsExcluder
from .contracts import AbcFsMatcher
from typing import Type, Mapping


class FsMatcherMapper:
    MATCHER_TYPE_EXCLUDER = 1
    MATCHER_TYPE_INCLUDER = 2

    FILENAME_CLASS: Mapping[str, Type[AbcFsMatcher]] = {
        '.gitignore': FsMatcherGitignore,
        '.unimetafs_exclude': UniMetaFsExcluder,
        '.unimetafs_include': UniMetaFsIncluder
    }

    @classmethod
    def exists(cls, filename: str) -> bool:
        return filename in cls.FILENAME_CLASS

    @classmethod
    def get(cls, filename, default=None) -> Type[AbcFsMatcher]:
        return cls.FILENAME_CLASS.get(filename, default)
