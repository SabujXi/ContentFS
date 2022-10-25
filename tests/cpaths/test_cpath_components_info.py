import json
from unittest import TestCase
from ContentFS.cpaths.cpath_components_info import CPathComponentsInfo
from ContentFS.exceptions import CFSExceptionInvalidPathName


class TestCPathComponentsInfo(TestCase):
    def test_init(self):
        empty_path = ""
        with self.assertRaises(CFSExceptionInvalidPathName):
            cci = CPathComponentsInfo(empty_path)

        dot_path = "."
        with self.assertRaises(CFSExceptionInvalidPathName):
            cci = CPathComponentsInfo(dot_path)

        dot_space_path = " ."
        with self.assertRaises(CFSExceptionInvalidPathName):
            cci = CPathComponentsInfo(dot_space_path)

    def test_drive__relative(self):
        relative_path = "hey/"
        cci_rel = CPathComponentsInfo(relative_path)
        self.assertEqual("", cci_rel.drive)

    def test_drive__unix(self):
        unix_path = "/a path to hell/oh_file.ext"
        cci_unix = CPathComponentsInfo(unix_path)
        self.assertEqual("/", cci_unix.drive)

    def test_drive__windows(self):
        windows_path = r"C:\\dir/file.ext"
        cci_win = CPathComponentsInfo(windows_path)
        self.assertEqual("C:", cci_win.drive)

    def test_drive__file(self):
        file_path = "file://a file path"
        cci_file = CPathComponentsInfo(file_path)
        self.assertEqual(cci_file.drive, "file:")

    def test_names(self):
        relative_path = "hey/"
        cci_rel = CPathComponentsInfo(relative_path)
        self.assertEqual(("hey",), cci_rel.names)

        unix_path = "/a path to hell/oh_file.ext"
        cci_unix = CPathComponentsInfo(unix_path)
        self.assertEqual(("a path to hell", "oh_file.ext"), cci_unix.names)

        windows_path = r"C:\\dir/file.ext"
        cci_win = CPathComponentsInfo(windows_path)
        self.assertEqual(("dir", "file.ext"), cci_win.names)

        file_path = "file://a file path"
        cci_file = CPathComponentsInfo(file_path)
        self.assertEqual(("a file path",), cci_file.names)

    def test_last_char(self):
        relative_path = "hey/"
        cci_rel = CPathComponentsInfo(relative_path)
        self.assertEqual("/", cci_rel.last_char)

        unix_path = "/a path to hell/oh_file.ext"
        cci_unix = CPathComponentsInfo(unix_path)
        self.assertEqual("t", cci_unix.last_char)

        windows_path = r"C:\\dir/file.ext"
        cci_win = CPathComponentsInfo(windows_path)
        self.assertEqual("t", cci_win.last_char)

        file_path = "file://a file path"
        cci_file = CPathComponentsInfo(file_path)
        self.assertEqual("h", cci_file.last_char)

        # *** this part of the test is very important where you will check that even if the last char
        # *** is backward slash it will show as forward slash
        backward_slash_path = "a path\\"
        cci_backward_slash_path = CPathComponentsInfo(backward_slash_path)
        self.assertEqual("/", cci_backward_slash_path.last_char)

        drive_only_path_linux = "/"
        cci_drive_only_linux = CPathComponentsInfo(drive_only_path_linux)
        self.assertEqual("", cci_drive_only_linux.last_char)

        drive_only_path_windows = "C://"
        cci_drive_only_windows = CPathComponentsInfo(drive_only_path_windows)
        self.assertEqual("", cci_drive_only_windows.last_char)

        drive_only_path_file = "file://"
        cci_drive_only_file = CPathComponentsInfo(drive_only_path_file)
        self.assertEqual("", cci_drive_only_file.last_char)

    def test_has_drive(self):
        relative_path = "hey/"
        cci_rel = CPathComponentsInfo(relative_path)
        self.assertFalse(cci_rel.has_drive)

        unix_path = "/a path to hell/oh_file.ext"
        cci_unix = CPathComponentsInfo(unix_path)
        self.assertTrue(cci_unix.has_drive)

        windows_path = r"C:\\dir/file.ext"
        cci_win = CPathComponentsInfo(windows_path)
        self.assertTrue(cci_win.has_drive)

        file_path = "file://a file path"
        cci_file = CPathComponentsInfo(file_path)
        self.assertTrue(cci_file.has_drive)

    def test_has_non_unix_drive(self):
        relative_path = "hey/"
        cci_rel = CPathComponentsInfo(relative_path)
        self.assertFalse(cci_rel.has_non_unix_drive)

        unix_path = "/a path to hell/oh_file.ext"
        cci_unix = CPathComponentsInfo(unix_path)
        self.assertFalse(cci_unix.has_non_unix_drive)

        windows_path = r"C:\\dir/file.ext"
        cci_win = CPathComponentsInfo(windows_path)
        self.assertTrue(cci_win.has_non_unix_drive)

        file_path = "file://a file path"
        cci_file = CPathComponentsInfo(file_path)
        self.assertTrue(cci_file.has_non_unix_drive)

    def test_has_unix_root(self):
        relative_path = "hey/"
        cci_rel = CPathComponentsInfo(relative_path)
        self.assertFalse(cci_rel.has_unix_root)

        unix_path = "/a path to hell/oh_file.ext"
        cci_unix = CPathComponentsInfo(unix_path)
        self.assertTrue(cci_unix.has_unix_root)

        windows_path = r"C:\\dir/file.ext"
        cci_win = CPathComponentsInfo(windows_path)
        self.assertFalse(cci_win.has_unix_root)

        file_path = "file://a file path"
        cci_file = CPathComponentsInfo(file_path)
        self.assertFalse(cci_file.has_unix_root)

    def test_to_dict(self):
        """
        Not much to test here as all the other method tests will validate that this is working properly.
        So, one/two tests are enough.
        """
        # test empty path string.
        path_string = "abc"
        cci = CPathComponentsInfo(path_string)
        self.assertEqual(cci.to_dict(), {
            "drive": "",
            "names": ("abc", ),
            "last_char": "c"
        })

    def test_to_json(self):
        """
        From to_dict take the value, serialize and deserialize that and match that with deserialized .to_json
        """
        path_string = "/usr/bin/whatever.ext"
        cci = CPathComponentsInfo(path_string)
        self.assertDictEqual(json.loads(cci.to_json()), json.loads(json.dumps(cci.to_dict())))
