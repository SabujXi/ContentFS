from ContentFS.pathmatch.fsmatchers import FsMatcherGitignore


class DevFsMatcher(FsMatcherGitignore):
    def __init__(self, text=".git/\n"):
        _exclude_these = text
        super().__init__(_exclude_these)
