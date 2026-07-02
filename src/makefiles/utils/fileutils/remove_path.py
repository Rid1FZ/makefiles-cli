import pathlib
import shutil

import makefiles.utils as utils


def remove(path: pathlib.Path) -> None:
    """
    Recursively removes a file, directory, or (broken) symbolic link at the specified path.

    This function safely deletes the given path. It handles:
      - regular files
      - symbolic links (including broken links)
      - directories (recursively)

    If the path does not exist, it silently ignores the error.

    Args:
        path (pathlib.Path): The path to a file, directory, or symbolic link to remove.
    """
    try:
        if utils.isfile(path) or utils.islink(path) or utils.isbrokenlink(path):
            path.unlink(missing_ok=True)
        elif utils.isdir(path):
            shutil.rmtree(path)
    except FileNotFoundError:
        pass
