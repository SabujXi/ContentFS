from ContentFS.pathmatch.matchers.basic_matchers.abstract_base_matchers import AbcMatcher
from ContentFS.pathmatch.matchers.basic_matchers.component_matcher import CompMatcher


class DoubleAsteriskMatcher(AbcMatcher):
    def __init__(self, comp):
        assert comp == '**'
        self.__comp = comp

    def matches(self, path_components, matchers):
        raise Exception("This method must not be used - path matcher handles double asterisk stuffs")
        # hard part
        if len(matchers) == 0:
            # zero or more paths eaten by current double asterisks
            path_components.clear()
            # this last double asterisks matches the rest of the path components.
            return True
        else:
            next_matcher: CompMatcher = matchers.popleft()
            # double asterisk can match zero path comp, that's why the current path
            # comp is taken into consideration.
            next_matched = False
            while len(path_components) > 0:  # the target is to engulf the path components by next matcher.
                next_path_comp = path_components.popleft()
                if next_matcher.matches(next_path_comp):
                    # the work of double asterisk ends here. next patterns in the path matcher please.
                    next_matched = True
                    break
                else:
                    # let's match the next path component. with the matcher.
                    pass
            if next_matched:
                return True
            else:
                return False