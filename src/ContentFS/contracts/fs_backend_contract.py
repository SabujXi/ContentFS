import abc
from .meta_fs_backend_contract import BaseMetaFsBackendContract


class BaseFsBackendContract(BaseMetaFsBackendContract):
    @abc.abstractmethod
    def open(self, path, *args, **kwargs):
        """Return a file object"""

    @abc.abstractmethod
    def makedirs(self, path):
        """Makes directories recursively"""

    @abc.abstractmethod
    def remove(self, path):
        """Removes the path"""
