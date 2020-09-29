import abc


class AbcMatcher(metaclass=abc.ABCMeta):
    """
    Abstract base class for matchers.
    """
    @abc.abstractmethod
    def matches(self, *params) -> bool:
        pass


class AbcSubCompMatcher(metaclass=abc.ABCMeta):
    """Sub comp of comp matcher"""
    @abc.abstractmethod
    def matches(self, *params) -> bool:
        pass

    @property
    @abc.abstractmethod
    def regex_pat(self) -> str:
        pass
