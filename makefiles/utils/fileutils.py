import pathlib
import shutil

import makefiles.exceptions as exceptions
import makefiles.utils as utils


def copy(src: pathlib.Path, *dests: pathlib.Path, overwrite: bool = False) -> None:
    """
    Makes one or multiple copies of `src`.

    Parameters:
        src(pathlib.Path): path to any file/symlink to file
        *dests(pathlib.Path): path to one or more non existing files
            which will be created using the `src`
        overwrite(bool): if `True` overwrite if any of the `dest` already exists

    Raises:
        makefiles.exceptions.SourceNotFoundError: if `src` does not exists
        makefiles.exceptions.InvalidSourceError: if `src` is not a regular file
            or a link to file
        makefiles.exceptions.DestinationExistsError: if any of the `dests` already
            exists and `overwrite` is `False`
    """
    if not utils.exists(src):
        raise exceptions.SourceNotFoundError(f"source {str(src)} does not exists")
    elif not (utils.isfile(src) or utils.islinkf(src)):
        raise exceptions.InvalidSourceError(f"source {str(src)} is not a file or a link to file")

    for dest in dests:
        if utils.exists(dest) and not overwrite:
            raise exceptions.DestinationExistsError(f"destination {str(dest)} already exists")

        # shutil.copyfile is unable to overwrite any broken symlink. So we will do it manually
        if utils.isbrokenlink(dest):
            dest.unlink(missing_ok=False)

        shutil.copyfile(src, dest, follow_symlinks=True)


def create_empty_files(*paths: pathlib.Path, overwrite: bool = False) -> None:
    """
    Create empty files in the given paths.

    Parameters:
        *paths(pathlib.Path): paths to files.
        overwrite(bool): if `True`, overwrite file if already exists

    Raises:
        makefiles.exceptions.DestinationExistsError: if given path already exists.
    """

    for path in paths:
        if utils.exists(path) and not overwrite:
            raise exceptions.DestinationExistsError(f"file {path} already exists")

        try:
            if utils.isfile(path) or utils.islink(path) or utils.isbrokenlink(path):
                path.unlink(missing_ok=True)
            elif utils.isdir(path):
                shutil.rmtree(path)
        except FileNotFoundError:
            pass

        path.touch(exist_ok=False)
