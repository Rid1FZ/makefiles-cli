import pathlib
import shutil

import makefiles.exceptions as exceptions
import makefiles.types as custom_types
import makefiles.utils as utils
import makefiles.utils.cli_io as cli_io
import makefiles.utils.fileutils as fileutils


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

    if not dests:
        raise ValueError(f"at least 1 destination expected. Got {len(dests)}")

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

        fileutils.remove_path(dest)
        dest_parent.mkdir(parents=True, exist_ok=True)

        shutil.copyfile(src, dest, follow_symlinks=True)

    return exitcode
