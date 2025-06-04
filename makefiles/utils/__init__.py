import os.path
import pathlib


def exists(path: pathlib.Path) -> bool:
    """
    Checks whether the specified path exists, including broken symlinks.

    Args:
        path (pathlib.Path): The path to check.

    Returns:
        bool: True if the path exists or is a broken symlink, False otherwise.
    """
    return os.path.lexists(path)


def isfile(path: pathlib.Path) -> bool:
    """
    Checks whether the given path is a regular file and not a symbolic link.

    Args:
        path (pathlib.Path): The path to evaluate.

    Returns:
        bool: True if the path exists, is a regular file, and is not a symlink; False otherwise.
    """
    return path.is_file() and not path.is_symlink()


def isdir(path: pathlib.Path) -> bool:
    """
    Checks whether the given path is a directory and not a symbolic link.

    Args:
        path (pathlib.Path): The path to evaluate.

    Returns:
        bool: True if the path exists, is a directory, and is not a symlink; False otherwise.
    """
    return path.is_dir() and not path.is_symlink()


def isbrokenlink(path: pathlib.Path) -> bool:
    """
    Checks whether the given path is a broken symbolic link.

    Args:
        path (pathlib.Path): The path to evaluate.

    Returns:
        bool: True if the path is a symlink and its target does not exist; False otherwise.

    Note:
        This relies on the fact that `path.exists()` returns False for broken symlinks.
    """
    # if path is a broken link, pathlib.Path.exists will return False. We will use this feature
    return path.is_symlink() and not path.exists()


def islink(path: pathlib.Path) -> bool:
    """
    Checks whether the given path is a valid (non-broken) symbolic link.

    Args:
        path (pathlib.Path): The path to evaluate.

    Returns:
        bool: True if the path is a symlink and its target exists; False otherwise.
    """
    return path.is_symlink() and not isbrokenlink(path)


def islinkf(path: pathlib.Path) -> bool:
    """
    Checks whether the given path is a symbolic link that points to a regular file.

    Args:
        path (pathlib.Path): The path to evaluate.

    Returns:
        bool: True if the path is a symlink and its target is a regular file; False otherwise.
    """
    return path.is_symlink() and path.is_file()


def islinkd(path: pathlib.Path) -> bool:
    """
    Checks whether the given path is a symbolic link that points to a directory.

    Args:
        path (pathlib.Path): The path to evaluate.

    Returns:
        bool: True if the path is a symlink and its target is a directory; False otherwise.
    """
    return path.is_symlink() and path.is_dir()


def get_version() -> str:
    """
    Returns the current version of the tool using `setuptools_scm`.

    Attempts to import the version from the auto-generated `_version.py` module.
    Falls back to "unknown" if the version cannot be imported.

    Returns:
        str: The current version string, or "unknown" if unavailable.
    """
    try:
        import makefiles._version as v

        return v.version
    except ImportError:
        return "unknown"


def get_hinder(path: pathlib.Path) -> str | None:
    """
    Recursively identifies the nearest path component that would prevent file or directory creation.

    This function checks if any part of the given path is a broken symlink or a non-directory
    (excluding valid directory symlinks). It traverses up the path hierarchy until it either
    finds such a hindrance or reaches the root.

    Args:
        path (pathlib.Path): The path to evaluate.

    Returns:
        str | None: The problematic path component as a string, or None if no hindrance is found.
    """
    if isbrokenlink(path) or not (isdir(path) or islinkd(path)):
        return str(path)
    if str(path) == "/":
        return

    return get_hinder(path.parent)
