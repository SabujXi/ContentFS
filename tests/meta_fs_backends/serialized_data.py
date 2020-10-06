# these dict and json data represents the dir from test: tests/test_data/metafs_json_n_dict_test_dir

fs_json = """
{
    "cpaths": [
        {
            "names": [
                "adir"
            ],
            "type": "DIR",
            "path": "adir/",
            "children": []
        },
        {
            "names": [
                "empty_dir"
            ],
            "type": "DIR",
            "path": "empty_dir/",
            "children": []
        },
        {
            "names": [
                "dir with files only"
            ],
            "type": "DIR",
            "path": "dir with files only/",
            "children": [
                {
                    "names": [
                        "dir with files only",
                        "empty.file"
                    ],
                    "type": "FILE",
                    "path": "dir with files only/empty.file",
                    "mtime": 1601984153.0640109,
                    "size": 0
                },
                {
                    "names": [
                        "dir with files only",
                        "a.txt"
                    ],
                    "type": "FILE",
                    "path": "dir with files only/a.txt",
                    "mtime": 1601984143.5499153,
                    "size": 66
                }
            ]
        },
        {
            "names": [
                "a"
            ],
            "type": "DIR",
            "path": "a/",
            "children": []
        },
        {
            "names": [
                "dir with children"
            ],
            "type": "DIR",
            "path": "dir with children/",
            "children": [
                {
                    "names": [
                        "dir with children",
                        "nested dir with children"
                    ],
                    "type": "DIR",
                    "path": "dir with children/nested dir with children/",
                    "children": [
                        {
                            "names": [
                                "dir with children",
                                "nested dir with children",
                                "secrets"
                            ],
                            "type": "DIR",
                            "path": "dir with children/nested dir with children/secrets/",
                            "children": [
                                {
                                    "names": [
                                        "dir with children",
                                        "nested dir with children",
                                        "secrets",
                                        "no secret"
                                    ],
                                    "type": "DIR",
                                    "path": "dir with children/nested dir with children/secrets/no secret/",
                                    "children": [
                                        {
                                            "names": [
                                                "dir with children",
                                                "nested dir with children",
                                                "secrets",
                                                "no secret",
                                                "plain file"
                                            ],
                                            "type": "FILE",
                                            "path": "dir with children/nested dir with children/secrets/no secret/plain file",
                                            "mtime": 1601984259.5411055,
                                            "size": 46
                                        }
                                    ]
                                },
                                {
                                    "names": [
                                        "dir with children",
                                        "nested dir with children",
                                        "secrets",
                                        "secret.txt"
                                    ],
                                    "type": "FILE",
                                    "path": "dir with children/nested dir with children/secrets/secret.txt",
                                    "mtime": 1601984295.0706043,
                                    "size": 40
                                }
                            ]
                        }
                    ]
                },
                {
                    "names": [
                        "dir with children",
                        "empty_nested_dir"
                    ],
                    "type": "DIR",
                    "path": "dir with children/empty_nested_dir/",
                    "children": []
                },
                {
                    "names": [
                        "dir with children",
                        "x.txt"
                    ],
                    "type": "FILE",
                    "path": "dir with children/x.txt",
                    "mtime": 1601984203.9962876,
                    "size": 36
                }
            ]
        },
        {
            "names": [
                "a.txt"
            ],
            "type": "FILE",
            "path": "a.txt",
            "mtime": 1601984065.019008,
            "size": 0
        }
    ]
}
"""

fs_dict = {'cpaths': [{'names': ('adir',), 'type': 'DIR', 'path': 'adir/', 'children': ()},
                      {'names': ('empty_dir',), 'type': 'DIR', 'path': 'empty_dir/', 'children': ()},
                      {'names': ('dir with files only',), 'type': 'DIR', 'path': 'dir with files only/', 'children': (
                          {'names': ('dir with files only', 'empty.file'), 'type': 'FILE',
                           'path': 'dir with files only/empty.file', 'mtime': 1601984153.0640109, 'size': 0},
                          {'names': ('dir with files only', 'a.txt'), 'type': 'FILE', 'path': 'dir with files only/a.txt',
                           'mtime': 1601984143.5499153, 'size': 66})},
                      {'names': ('a',), 'type': 'DIR', 'path': 'a/', 'children': ()},
                      {'names': ('dir with children',), 'type': 'DIR', 'path': 'dir with children/', 'children': (
                          {'names': ('dir with children', 'nested dir with children'), 'type': 'DIR',
                           'path': 'dir with children/nested dir with children/', 'children': (
                              {'names': ('dir with children', 'nested dir with children', 'secrets'), 'type': 'DIR',
                               'path': 'dir with children/nested dir with children/secrets/', 'children': (
                                  {'names': ('dir with children', 'nested dir with children', 'secrets', 'no secret'),
                                   'type': 'DIR', 'path': 'dir with children/nested dir with children/secrets/no secret/',
                                   'children': ({'names': (
                                       'dir with children', 'nested dir with children', 'secrets', 'no secret', 'plain file'),
                                                    'type': 'FILE',
                                                    'path': 'dir with children/nested dir with children/secrets/no secret/plain file',
                                                    'mtime': 1601984259.5411055, 'size': 46},)},
                                  {'names': ('dir with children', 'nested dir with children', 'secrets', 'secret.txt'),
                                   'type': 'FILE', 'path': 'dir with children/nested dir with children/secrets/secret.txt',
                                   'mtime': 1601984295.0706043, 'size': 40})},)},
                          {'names': ('dir with children', 'empty_nested_dir'), 'type': 'DIR',
                           'path': 'dir with children/empty_nested_dir/', 'children': ()},
                          {'names': ('dir with children', 'x.txt'), 'type': 'FILE', 'path': 'dir with children/x.txt',
                           'mtime': 1601984203.9962876, 'size': 36})},
                      {'names': ('a.txt',), 'type': 'FILE', 'path': 'a.txt', 'mtime': 1601984065.019008, 'size': 0}]}
