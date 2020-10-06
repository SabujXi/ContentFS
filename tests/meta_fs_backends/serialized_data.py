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


fs_json_hashed = """
{
    "cpaths": [
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
                "adir"
            ],
            "type": "DIR",
            "path": "adir/",
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
                        "empty_nested_dir"
                    ],
                    "type": "DIR",
                    "path": "dir with children/empty_nested_dir/",
                    "children": []
                },
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
                                            "mtime": 1601984259.541,
                                            "size": 46,
                                            "hash": "f0a1d4dfdb9d4418dd351e0d78e7d6dac9294b5b"
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
                                    "mtime": 1601984295.07,
                                    "size": 40,
                                    "hash": "c08c1501c3f8e3922cf6568fddf057ab0399700e"
                                }
                            ]
                        }
                    ]
                },
                {
                    "names": [
                        "dir with children",
                        "x.txt"
                    ],
                    "type": "FILE",
                    "path": "dir with children/x.txt",
                    "mtime": 1601984203.996,
                    "size": 36,
                    "hash": "b05d8652adf9ec0459f6ee0f9b4088770bff2f34"
                }
            ]
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
                        "a.txt"
                    ],
                    "type": "FILE",
                    "path": "dir with files only/a.txt",
                    "mtime": 1601984143.549,
                    "size": 66,
                    "hash": "0cc1a0874d1bd2327fd3674b73f7582b1edc0997"
                },
                {
                    "names": [
                        "dir with files only",
                        "empty.file"
                    ],
                    "type": "FILE",
                    "path": "dir with files only/empty.file",
                    "mtime": 1601984153.064,
                    "size": 0,
                    "hash": "da39a3ee5e6b4b0d3255bfef95601890afd80709"
                }
            ]
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
                "a.txt"
            ],
            "type": "FILE",
            "path": "a.txt",
            "mtime": 1601984065.019,
            "size": 0,
            "hash": "da39a3ee5e6b4b0d3255bfef95601890afd80709"
        }
    ]
}
"""

fs_dict_hashed = {'cpaths': [{'names': ('a',), 'type': 'DIR', 'path': 'a/', 'children': ()},
                             {'names': ('adir',), 'type': 'DIR', 'path': 'adir/', 'children': ()},
                             {'names': ('dir with children',), 'type': 'DIR', 'path': 'dir with children/',
                              'children': ({'names': ('dir with children', 'empty_nested_dir'), 'type': 'DIR',
                                            'path': 'dir with children/empty_nested_dir/', 'children': ()},
                                           {'names': ('dir with children', 'nested dir with children'), 'type': 'DIR',
                                            'path': 'dir with children/nested dir with children/', 'children': (
                                               {'names': ('dir with children', 'nested dir with children', 'secrets'),
                                                'type': 'DIR',
                                                'path': 'dir with children/nested dir with children/secrets/', 'children': (
                                                   {'names': (
                                                       'dir with children', 'nested dir with children', 'secrets', 'no secret'),
                                                       'type': 'DIR',
                                                       'path': 'dir with children/nested dir with children/secrets/no secret/',
                                                       'children': ({'names': (
                                                           'dir with children', 'nested dir with children', 'secrets', 'no secret',
                                                           'plain file'), 'type': 'FILE',
                                                                        'path': 'dir with children/nested dir with children/secrets/no secret/plain file',
                                                                        'mtime': 1601984259.541, 'size': 46,
                                                                        'hash': 'f0a1d4dfdb9d4418dd351e0d78e7d6dac9294b5b'},)}, {
                                                       'names': ('dir with children', 'nested dir with children', 'secrets',
                                                                 'secret.txt'), 'type': 'FILE',
                                                       'path': 'dir with children/nested dir with children/secrets/secret.txt',
                                                       'mtime': 1601984295.07, 'size': 40,
                                                       'hash': 'c08c1501c3f8e3922cf6568fddf057ab0399700e'})},)},
                                           {'names': ('dir with children', 'x.txt'), 'type': 'FILE',
                                            'path': 'dir with children/x.txt', 'mtime': 1601984203.996, 'size': 36,
                                            'hash': 'b05d8652adf9ec0459f6ee0f9b4088770bff2f34'})},
                             {'names': ('dir with files only',), 'type': 'DIR', 'path': 'dir with files only/',
                              'children': ({'names': ('dir with files only', 'a.txt'), 'type': 'FILE',
                                            'path': 'dir with files only/a.txt', 'mtime': 1601984143.549, 'size': 66,
                                            'hash': '0cc1a0874d1bd2327fd3674b73f7582b1edc0997'},
                                           {'names': ('dir with files only', 'empty.file'), 'type': 'FILE',
                                            'path': 'dir with files only/empty.file', 'mtime': 1601984153.064,
                                            'size': 0, 'hash': 'da39a3ee5e6b4b0d3255bfef95601890afd80709'})},
                             {'names': ('empty_dir',), 'type': 'DIR', 'path': 'empty_dir/', 'children': ()},
                             {'names': ('a.txt',), 'type': 'FILE', 'path': 'a.txt', 'mtime': 1601984065.019, 'size': 0,
                              'hash': 'da39a3ee5e6b4b0d3255bfef95601890afd80709'}]}
