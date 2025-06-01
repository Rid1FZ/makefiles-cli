import os
import pathlib

import makefiles.exceptions as exceptions
import makefiles.utils as utils


def listf(path: pathlib.Path) -> list[str]:
    """
    List all the files recursively inside given directory and it's subdirectories.

    Parameters:
        path(pathlib.Path): path to directory.

    Raises:
        exceptions.InvalidPathError: if `path` is not a directory or link to directory.
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
