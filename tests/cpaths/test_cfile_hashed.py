from unittest import TestCase
from ContentFS.cpaths.cfile_hashed import CFileHashed
from ContentFS.exceptions import CFSExceptionFileHashSizeMismatch


class TestCFileHashed(TestCase):
    def test_hash(self):
        self.assertRaises(CFSExceptionFileHashSizeMismatch, lambda: CFileHashed("a", 1, 2, "abc"))

        hcfile = CFileHashed("a", 1, 2, "a"*40)
        self.assertEqual("a"*40, hcfile.hash)

    def test_equals(self):
        """
        Caution: this is by hash matching only
        """
        hcfile1 = CFileHashed("a", 1, 2, "a" * 40)
        hcfile2 = CFileHashed("a", 1111, 2, "a" * 40)

        self.assertTrue(hcfile1.equals(hcfile2))

    def test_equals_by_hash(self):
        hcfile1 = CFileHashed("a", 1, 2, "a"*40)
        hcfile2 = CFileHashed("a", 1111, 2, "a"*40)

        self.assertTrue(hcfile1.equals_by_hash(hcfile2))

    def test_to_dict(self):
        hcfile = CFileHashed("a", 1111, 2, "a"*40)
        self.assertEqual(
            {
                'type': 'FILE',
                'path': 'a',
                'names': ('a',),
                'mtime': 1111,
                'size': 2,
                'hash': 'a'*40
            },
            hcfile.to_dict()
        )
