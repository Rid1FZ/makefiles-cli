import pathlib
import shutil

import makefiles.exceptions as exceptions
import makefiles.types as custom_types
import makefiles.utils as utils
import makefiles.utils.cli_io as cli_io


def _clear_hinder(path: pathlib.Path) -> None:
    """
    Remove/unlink any hinder which may cause creation of `path` to be failed.
    """
    hinder: str | None = utils.get_hinder(path)
    if not hinder:
        return

    hinder_path: pathlib.Path = pathlib.Path(hinder)
    try:
        if utils.isfile(hinder_path) or utils.islink(hinder_path) or utils.isbrokenlink(hinder_path):
            hinder_path.unlink(missing_ok=True)
        elif utils.isdir(hinder_path):
            shutil.rmtree(hinder_path)
    except FileNotFoundError:
        pass


def copy(
    src: pathlib.Path,
    *dests: pathlib.Path,
    overwrite: bool = False,
    parents: bool = False,
) -> custom_types.ExitCode:
    """
    Copies a source file or symbolic link to one or more destination paths.

    Args:
        src (pathlib.Path): Path to the source file. Must be a regular file or a symlink to a file.
        *dests (pathlib.Path): One or more destination paths to copy the source to.
        overwrite (bool, optional): If True, existing destination files will be overwritten.
                                    If False (default), print an error message and be skip.
        parents (bool, optional): If True, create parent(s) if not already exists.
                                  If False (default), print an error message and skip.

    Returns:
        custom_types.ExitCode: Exit code 0 if all copies succeed.
                               Returns 1 if any destination exists and overwrite is False.

    Raises:
        makefiles.exceptions.SourceNotFoundError: If the source path does not exist.
        makefiles.exceptions.InvalidSourceError: If the source is not a file or a symbolic link to a file.
    """
    exitcode: custom_types.ExitCode = custom_types.ExitCode(0)

    if not utils.exists(src):
        raise exceptions.SourceNotFoundError(f"source {str(src)} does not exists")
    elif not (utils.isfile(src) or utils.islinkf(src)):
        raise exceptions.InvalidSourceError(f"source {str(src)} is not a file or a link to file")

    for dest in dests:
        if utils.exists(dest) and not overwrite:
            cli_io.eprint(f"destination {str(dest)} already exists\n")
            exitcode = custom_types.ExitCode(1) or exitcode
            continue

        dest_parent: pathlib.Path = dest.parent
        if not (utils.isdir(dest_parent) or utils.islinkd(dest_parent)) and not parents:
            cli_io.eprint(f"parent dir {str(dest_parent)} does not exists\n")
            exitcode = custom_types.ExitCode(1) or exitcode
            continue

        _clear_hinder(dest)
        dest_parent.mkdir(parents=True, exist_ok=True)

        shutil.copyfile(src, dest, follow_symlinks=True)

    return exitcode


def create_empty_files(
    *paths: pathlib.Path,
    overwrite: bool = False,
    parents: bool = False,
) -> custom_types.ExitCode:
    """
    Creates empty files at the specified paths, optionally overwriting existing files or directories.

    Args:
        *paths (pathlib.Path): One or more paths where empty files should be created.
        overwrite (bool, optional): If True, existing destination files will be overwritten.
                                    If False (default), print an error message and be skip.
        parents (bool, optional): If True, create parent(s) if not already exists.
                                  If False (default), print an error message and skip.

    Returns:
        makefiles.types.ExitCode: Exit code 0 on full success.
                                  Exit code 1 if any file already exists and overwrite is False.
    """
    exitcode: custom_types.ExitCode = custom_types.ExitCode(0)

    for path in paths:
        if utils.exists(path) and not overwrite:
            cli_io.eprint(f"destination {path} already exists\n")
            exitcode = custom_types.ExitCode(1) or exitcode
            continue

        path_parent: pathlib.Path = path.parent
        if not (utils.isdir(path_parent) or utils.islinkd(path_parent)) and not parents:
            cli_io.eprint(f"parent dir {str(path_parent)} does not exists\n")
            exitcode = custom_types.ExitCode(1) or exitcode
            continue

        _clear_hinder(path)
        path_parent.mkdir(parents=True, exist_ok=False)

        path.touch(exist_ok=False)

    return exitcode
