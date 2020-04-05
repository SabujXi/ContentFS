import re
from .matchers import DoubleAsteriskMatcher, CompMatcher, PathMatcher


def gitignore_parser(text):
    _lines = re.split(r'\n\r|\n|\r', text)
    path_matchers = []
    # Put a backslash ("\") in front of the first hash for patterns that begin with a hash.
    for line in _lines:
        line_original = line
        is_negative = False
        only_directories = False
        is_root_relative = True
        path_comps = ()
        # A blank line matches no files, so it can serve as a separator for readability.
        line = line.strip()
        if not line:
            continue
        # A line starting with # serves as a comment.
        if line.startswith('#'):
            continue
        # Put a backslash ("\") in front of the first hash for patterns that begin with a hash.
        if line.startswith(r'\#'):
            line = line[1:]
        # An optional prefix "!" which negates the pattern; any matching file excluded by a previous pattern will become
        # included again.
        if line.startswith('!'):
            is_negative = True
            line = line[1:]

        # now replace the consecutive seps |: not in the rule though
        line = re.sub(r'/+', r'/', line)
        # If there is a separator at the end of the pattern then the pattern will only match directories, otherwise
        # the pattern can match both files and directories.
        if line.endswith('/'):
            only_directories = True
            line = line[:-1]
        # If there is a separator at the beginning or middle (or both) of the pattern, then the pattern is relative to
        # the directory level of the particular .gitignore file itself. Otherwise the pattern may also match at
        # any level below the .gitignore level.
        path_comps = line.split('/')
        if path_comps[0] == '':
            del path_comps[0]  # "/" will return empty path comps? TODO: have a closer look and test.
        if len(path_comps) == 1:
            is_root_relative = False

        _path_comps = []
        # reduce consecutive double asterisks
        prev_d_asterisks = False
        for comp in path_comps:
            if comp == '**':
                if prev_d_asterisks:
                    # drop this one
                    continue
                else:
                    _path_comps.append(comp)
                prev_d_asterisks = True
            else:
                _path_comps.append(comp)
                prev_d_asterisks = False
        path_comps = _path_comps

        # build the match objects
        matcher_objects = []
        for comp in path_comps:
            if comp == '**':
                matcher = DoubleAsteriskMatcher(comp)
            else:
                matcher = CompMatcher(comp)
            matcher_objects.append(matcher)
        path_matchers.append(
            PathMatcher(matcher_objects, line_original, is_negative, only_directories, is_root_relative)
        )

    return path_matchers
