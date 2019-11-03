class Diff:
    def __init__(self):
        self.__deleted = []
        self.__modified = []
        self.__new = []

    @property
    def deleted(self):
        return tuple(self.__deleted)

    @property
    def modified(self):
        return tuple(self.__modified)

    @property
    def new(self):
        return tuple(self.__new)

    def add_deleted(self, cpath):
        self.__deleted.append(cpath)

    def add_modified(self, cpath):
        self.__modified.append(cpath)

    def add_new(self, cpath):
        self.__new.append(cpath)

    def changed(self):
        return self.__modified or self.__deleted or self.__new
