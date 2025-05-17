import os.path
import pathlib


def exists(path: pathlib.Path) -> bool:
    """Checks if given path exists"""
    return os.path.lexists(path)


def isfile(path: pathlib.Path) -> bool:
    """Checks if given path is a regular file and not a symlink"""
    return path.is_file() and not path.is_symlink()


def isdir(path: pathlib.Path) -> bool:
    """Checks if given path is a directory and not a symlink"""
    return path.is_dir() and not path.is_symlink()


def islink(path: pathlib.Path) -> bool:
    """Checks if given path is a symlink"""
    return path.is_symlink() and not isbrokenlink(path)


def islinkf(path: pathlib.Path) -> bool:
    """Checks if given path is a link to a file"""
    return path.is_symlink() and path.is_file()


def islinkd(path: pathlib.Path) -> bool:
    """Checks if given path is a link to directory"""
    return path.is_symlink() and path.is_dir()


def isbrokenlink(path: pathlib.Path) -> bool:
    """Checks if given path is a broken symlink"""
    # if path is a broken link, pathlib.Path.exists will return False. We will use this feature
    return path.is_symlink() and not path.exists()
