import pathlib
import shutil
from logging import Logger

import makefiles.exceptions as exceptions
import makefiles.utils as utils
import makefiles.utils.cli_io as cli_io
import makefiles.utils.fileutils as fileutils
from makefiles.logger import get_logger
from makefiles.types import ExitCode, NaturalNumber

_logger: Logger = get_logger(__name__)


def copy(
    src: pathlib.Path,
    dests: tuple[pathlib.Path, ...] = (),
    *,
    overwrite: bool = False,
    parents: bool = False,
    verbose: bool = False,
    dry_run: bool = False,
) -> ExitCode:
    """
    Copies a source file or symbolic link to one or more destination paths.

    Args:
        src (pathlib.Path): Source file.  Must be a regular file or a symlink
            to a regular file.
        dests (tuple[pathlib.Path, ...]): One or more destination paths.
        overwrite (bool): When *True*, an existing destination is replaced.
            When *False* (default), a warning is printed and that destination
            is skipped.
        parents (bool): When *True*, missing parent directories are created
            automatically.  When *False* (default), a warning is printed and
            that destination is skipped.
        verbose (bool): When *True*, print a confirmation line to *stdout*
            for every successful copy (or every would-be copy when
            *dry_run* is also *True*).
        dry_run (bool): When *True*, perform all pre-flight checks but make
            **no** changes to the filesystem.  Implies *verbose*.

    Returns:
        ExitCode: `0` when all copies succeed (or are previewed), `1`
        when any destination is skipped.

    Raises:
        ValueError: If *dests* is empty.
        makefiles.exceptions.SourceNotFoundError: If *src* does not exist.
        makefiles.exceptions.InvalidSourceError: If *src* is not a file or
            a symlink to a file.
        makefiles.exceptions.InvalidPathError: If a parent directory cannot
            be created (e.g. a file sits in the path).
    """
    exitcode: ExitCode = ExitCode(0)

    if not dests:
        raise ValueError(f"at least 1 destination expected. Got {len(dests)}")

    if not utils.exists(src):
        raise exceptions.SourceNotFoundError(f"source {str(src)} does not exists")
    elif not (utils.isfile(src) or utils.islinkf(src)):
        raise exceptions.InvalidSourceError(f"source {str(src)} is not a file or a link to file")

    for dest in dests:
        if utils.exists(dest) and not overwrite:
            cli_io.eprint(f"destination {str(dest)} already exists\n")
            exitcode = ExitCode(1)
            continue

        dest_parent: pathlib.Path = dest.parent
        if not (utils.isdir(dest_parent) or utils.islinkd(dest_parent)) and not parents:
            cli_io.eprint(f"parent dir {str(dest_parent)} does not exists\n")
            exitcode = ExitCode(1)
            continue

        if dry_run:
            cli_io.print(f"[dry-run] would copy '{src}' -> '{dest}'\n")
            _logger.debug("dry-run: would copy %s -> %s", src, dest)
            continue

        fileutils.remove_path(dest)
        try:
            dest_parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise exceptions.InvalidPathError(f"cannot create parent dir: {e}") from None

        shutil.copyfile(src, dest, follow_symlinks=True)
        _logger.debug("copied %s -> %s", src, dest)

        if verbose:
            cli_io.print(f"copied '{src}' -> '{dest}'\n")

    return exitcode
