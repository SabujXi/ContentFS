class Ignorer:
    def __init__(self):
        pass

    def ignore(self, cpath):
        if cpath.name == '.git' and cpath.is_dir():
            return True
        return False
