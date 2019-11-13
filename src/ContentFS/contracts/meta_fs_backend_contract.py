import abc


class BaseMetaFsBackendContract(metaclass=abc.ABCMeta):
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