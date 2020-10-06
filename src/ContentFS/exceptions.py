class CFSException(Exception):
    pass


class CFSPathDoesNotExistException(CFSException):
    pass


class CFSExceptionInvalidPathName(CFSException):
    pass


class CFSExceptionFileHashSizeMismatch(CFSException):
    pass
