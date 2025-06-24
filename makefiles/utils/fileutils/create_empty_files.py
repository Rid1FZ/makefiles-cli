import pathlib

import makefiles.utils as utils
import makefiles.utils.cli_io as cli_io
import makefiles.utils.fileutils as fileutils
from makefiles.types import ExitCode


def create(
    paths: tuple[pathlib.Path, ...] = (),
    *,
    overwrite: bool = False,
    parents: bool = False,
) -> ExitCode:
    """
    Creates empty files at the specified paths, optionally overwriting existing files or directories.

    Args:
        paths (tuple[pathlib.Path]): One or more paths where empty files should be created.
        overwrite (bool, optional): If True, existing destination files will be overwritten.
                                    If False (default), print an error message and be skip.
        parents (bool, optional): If True, create parent(s) if not already exists.
                                  If False (default), print an error message and skip.

    Returns:
        makefiles.types.ExitCode: Exit code 0 on full success.
                                  Exit code 1 if any file already exists and overwrite is False.
    """
    exitcode: ExitCode = ExitCode(0)

    if not paths:
        raise ValueError(f"at least on path expected. Got {len(paths)}")

    for path in paths:
        if utils.exists(path) and not overwrite:
            cli_io.eprint(f"destination {path} already exists\n")
            exitcode = ExitCode(1) or exitcode
            continue

        path_parent: pathlib.Path = path.parent
        if not (utils.isdir(path_parent) or utils.islinkd(path_parent)) and not parents:
            cli_io.eprint(f"parent dir {str(path_parent)} does not exists\n")
            exitcode = ExitCode(1) or exitcode
            continue

        fileutils.remove_path(path)
        path_parent.mkdir(parents=True, exist_ok=True)

        path.touch(exist_ok=False)

    return exitcode
