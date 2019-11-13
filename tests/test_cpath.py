from unittest import TestCase
from json import dumps, loads
from ContentFS.cpaths.croot import CRoot
from ContentFS.ignorer import Ignorer


class TestCRoot(TestCase):
    base_dir = r'D:\tmp'

    def test_load_from_path_dicts(self):
        root1 = CRoot(self.base_dir, Ignorer())
        root1.load()

        root1_path_json = dumps(root1.to_list())

        root2 = CRoot(self.base_dir, Ignorer())
        root2.load_from_path_dicts(loads(root1_path_json))

        diff = root1.diff(root2)

        self.assertTrue(not diff.changed(), "Reload from string doesn't work, so it is not ok")
