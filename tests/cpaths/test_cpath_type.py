from unittest import TestCase
from ContentFS.cpaths import CPathType


class TestCPathType(TestCase):
    def test_init(self):
        # FILE
        self.assertEqual(CPathType.FILE.value, 'FILE')
        self.assertEqual(CPathType.FILE.name, 'FILE')
        self.assertEqual(str(CPathType.FILE), 'FILE')

        # DIR
        self.assertEqual(CPathType.DIR.value, 'DIR')
        self.assertEqual(CPathType.DIR.name, 'DIR')
        self.assertEqual(str(CPathType.DIR), 'DIR')

    def test_all_types(self):
        all_types = set(CPathType)
        self.assertEqual(all_types, {CPathType.DIR, CPathType.FILE})
