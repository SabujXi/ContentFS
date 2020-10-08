# Rules

## This module only work with files and dirs, no symlink
Symlinks refer to file or dir, there is no place for symlink in this library, because that is in itself not serializable.

## CFile cannot be passed path with / at the end.
Here I am explicit, passing CFile("abc/") should not be accepted. It should throw an error.
