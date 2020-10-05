import abc

from ContentFS.cpaths import CPath


class AbcFsMatcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def matches(self, cpath: CPath) -> bool:
        """
        Primary intention of matcher is including if not specified otherwise. For example, Gitignore will try to exclude.
        """

    # @abc.abstractmethod
    # def exclude(self, cpath: CPath) -> bool:
    #     pass

    def is_includer(self) -> bool:
        """
        Matcher group will take care of what to include and to exclude after matching.
        ---------------------
        is excluder or is includer.

        Ignorer does not care about whether you include or not.

        Gitignore is a excluder - it does not care about what you include. It only tells you what to exclude.
        There will be excluder first or both excluder and includer matchers in future.
        """
        pass
