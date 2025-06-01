import os
import pathlib

import makefiles.exceptions as exceptions
import makefiles.utils as utils


def listf(path: pathlib.Path) -> list[str]:
    """
    Recursively lists all non-hidden files within a directory, relative to the given path.

    Args:
        path (pathlib.Path): Path to a directory or a symbolic link to a directory.

    Returns:
        list[str]: A list of relative file paths (as strings) for all non-hidden files
                   within the directory tree rooted at `path`.

    Raises:
        makefiles.exceptions.InvalidPathError: If the provided path is not a directory or a symlink to a directory.
    """
    path = path.absolute()
    if not (utils.isdir(path) or utils.islinkd(path)):
        raise exceptions.InvalidPathError("given path is not a directory or link to directory")

    result: list[str] = []

    for root, dirs, files in os.walk(path, topdown=True):
        # Exclude hidden directories
        dirs[:] = filter(lambda d: not d.startswith("."), dirs)

        for file in files:
            if not file.startswith("."):
                relative_path: str = os.path.relpath(os.path.join(root, file), path)
                result.append(relative_path)

    return result
