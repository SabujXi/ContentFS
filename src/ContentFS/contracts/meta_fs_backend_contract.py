import abc
from typing import IO, List


class BaseMetaFsBackendContract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_base_path(self, base_path):
        """Base path for performing different operations"""

    @property
    @abc.abstractmethod
    def base_path(self):
        pass

    @abc.abstractmethod
    def exists(self, path) -> bool:
        """
        Checks existence of path

        * does not check the type of the path.
        """

    @abc.abstractmethod
    def is_file(self, path) -> bool:
        """Checks if it is a file"""

    @abc.abstractmethod
    def is_dir(self, path) -> bool:
        """Checks if it is a dir"""

    @abc.abstractmethod
    def listdir(self, path) -> List[str]:
        """Lists a directory"""

    @abc.abstractmethod
    def getsize(self, path) -> int:
        """"""

    @abc.abstractmethod
    def getmtime(self, path) -> int:
        # int or float?? TODO: check
        """Get modification? time"""

    @abc.abstractmethod
    def gethash(self, path) -> str:
        """Get hash of the file"""

    @abc.abstractmethod
    def is_real_fs(self) -> bool:
        """
        Real fs will allow you to read contents of cfile.
        """
        return False

    def open(self, path, *args, **kwargs) -> IO:
        if not self.is_real_fs():
            raise Exception("Cannot use read on non real fs")  # TODO: proper exception from contentfs
        else:
            raise NotImplemented
