import abc
from typing import IO


class BaseMetaFsBackendContract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_base_path(self, base_path):
        """Base path for performing different operations"""

    @property
    @abc.abstractmethod
    def base_path(self):
        pass

    @abc.abstractmethod
    def exists(self, path):
        """Checks existence of path"""

    @abc.abstractmethod
    def is_file(self, path):
        """Checks if it is a file"""

    @abc.abstractmethod
    def is_dir(self, path):
        """Checks if it is a dir"""

    @abc.abstractmethod
    def listdir(self, path):
        """Lists a directory"""

    @abc.abstractmethod
    def getsize(self, path):
        """"""

    @abc.abstractmethod
    def getmtime(self, path):
        """Get modification? time"""

    @abc.abstractmethod
    def gethash(self, path):
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
