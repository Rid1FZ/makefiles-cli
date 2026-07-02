import pathlib
from logging import Logger

import makefiles.exceptions as exceptions
import makefiles.utils as utils
import makefiles.utils.cli_io as cli_io
import makefiles.utils.fileutils as fileutils
from makefiles.logger import get_logger
from makefiles.types import ExitCode

_logger: Logger = get_logger(__name__)


def create(
    paths: tuple[pathlib.Path, ...] = (),
    *,
    overwrite: bool = False,
    parents: bool = False,
    verbose: bool = False,
    dry_run: bool = False,
) -> ExitCode:
    """
    Creates empty files at the specified paths.

    Args:
        paths (tuple[pathlib.Path, ...]): One or more target paths.
        overwrite (bool): When *True*, existing files/dirs/symlinks at those
            paths are removed and replaced.  When *False* (default), a
            warning is printed and the path is skipped.
        parents (bool): When *True*, missing parent directories are created
            automatically.  When *False* (default), a warning is printed and
            the path is skipped.
        verbose (bool): When *True*, print a confirmation line to *stdout*
            for every file that is created (or previewed with *dry_run*).
        dry_run (bool): When *True*, perform all pre-flight checks but make
            **no** changes to the filesystem.  Implies *verbose*.

    Returns:
        ExitCode: `0` on full success (or full preview), `1` if any path
        was skipped.

    Raises:
        ValueError: If *paths* is empty.
        makefiles.exceptions.InvalidPathError: If a parent directory cannot
            be created (e.g. a file sits in the path).
    """
    exitcode: ExitCode = ExitCode(0)

    if not paths:
        raise ValueError(f"at least one path expected. Got {len(paths)}")

    _logger.debug("create_empty_files: overwrite=%s parents=%s dry_run=%s paths=%s", overwrite, parents, dry_run, paths)

    for path in paths:
        if utils.exists(path) and not overwrite:
            cli_io.eprint(f"destination {path} already exists\n")
            exitcode = ExitCode(1)
            continue

        path_parent: pathlib.Path = path.parent
        if not (utils.isdir(path_parent) or utils.islinkd(path_parent)) and not parents:
            cli_io.eprint(f"parent dir {str(path_parent)} does not exists\n")
            exitcode = ExitCode(1)
            continue

        if dry_run:
            cli_io.print(f"[dry-run] would create '{path}'\n")
            _logger.debug("dry-run: would create %s", path)
            continue

        fileutils.remove_path(path)
        try:
            path_parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise exceptions.InvalidPathError(f"cannot create parent dir: {e}") from None

        path.touch(exist_ok=False)

        _logger.debug("created %s", path)
        if verbose:
            cli_io.print(f"created '{path}'\n")

    return exitcode
