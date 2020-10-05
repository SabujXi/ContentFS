from ContentFS.pathmatch.fsmatchers import FsMatcherGitignore


class DevFsMatcher(FsMatcherGitignore):
    def __init__(self):
        _exclude_these = ".git/\n"
        super().__init__(_exclude_these)
