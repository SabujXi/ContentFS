class CFSException(Exception):
    pass


class CFSExceptionInvalidPathName(CFSException):
    pass


class CFSExceptionFileHashSizeMismatch(CFSException):
    pass
