import argparse
import os
import pathlib
import typing
from logging import Logger
from typing import Literal

try:
    from typing import assert_never
except ImportError:
    from typing_extensions import assert_never  # for python3.10

import makefiles.cli_parser as cli_parser
import makefiles.exceptions as exceptions
import makefiles.types as custom_types
import makefiles.utils as utils
import makefiles.utils.cli_io as cli_io
import makefiles.utils.dirwalker as dirwalker
import makefiles.utils.fileutils as fileutils
import makefiles.utils.picker as picker
from makefiles.logger import get_logger, setup_logging

TEMPLATES_DIR: typing.Final[str] = os.environ.get("XDG_TEMPLATES_DIR", str(pathlib.Path.home().joinpath("Templates")))

_logger: Logger = get_logger(__name__)


def _get_available_templates(templates_dir: pathlib.Path) -> list[str]:
    """
    Returns relative paths of all non-hidden files under *templates_dir*.

    Args:
        templates_dir (pathlib.Path): Directory that holds template files.

    Returns:
        list[str]: Relative template file paths.

    Raises:
        makefiles.exceptions.NoTemplatesAvailableError: If the directory does
            not exist, is not a directory, or contains no files.
    """
    try:
        available_templates: list[str] = dirwalker.listf(templates_dir)
        if not available_templates:
            raise exceptions.NoTemplatesAvailableError("no templates found")
    except exceptions.InvalidPathError:
        raise exceptions.NoTemplatesAvailableError("could not find template directory") from None

    return available_templates


def _create_template(
    template: str,
    destinations: tuple[pathlib.Path, ...],
    templates_dir: pathlib.Path,
    overwrite: bool,
    parents: bool,
    verbose: bool,
    dry_run: bool,
) -> custom_types.ExitCode:
    """
    Copies a named template to each destination path.

    Args:
        template (str): Template filename relative to *templates_dir*.
        destinations (tuple[pathlib.Path, ...]): Target paths for the copy.
        templates_dir (pathlib.Path): Root directory of available templates.
        overwrite (bool): Replace existing destinations when *True*.
        parents (bool): Create missing parent directories when *True*.
        verbose (bool): Print a confirmation for each successful copy.
        dry_run (bool): Preview only; make no filesystem changes.

    Returns:
        custom_types.ExitCode: `0` on success / preview, `1` on any skip.

    Raises:
        makefiles.exceptions.TemplateNotFoundError: If *template* does not
            exist inside *templates_dir*.
    """
    exitcode: custom_types.ExitCode = custom_types.ExitCode(0)

    template_path: pathlib.Path = templates_dir.joinpath(template)
    _logger.debug("_create_template: template=%s destinations=%s dry_run=%s", template_path, destinations, dry_run)

    try:
        exitcode = (
            fileutils.copy_file(
                template_path,
                destinations,
                overwrite=overwrite,
                parents=parents,
                verbose=verbose,
                dry_run=dry_run,
            )
            or exitcode
        )
    except exceptions.SourceNotFoundError:
        raise exceptions.TemplateNotFoundError(f"template {template} not found") from None

    return exitcode


def _get_template_from_prompt(
    *,
    t_picker: Literal["fzf"] | Literal["manual"],
    fzf_height: custom_types.NaturalNumber = custom_types.NaturalNumber(10),
    templates_dir: pathlib.Path,
) -> str:
    """
    Interactively prompts the user to choose a template.

    Args:
        t_picker: `fzf` or `manual` – the selection UI to use.
        fzf_height (custom_types.NaturalNumber): Terminal height for the fzf
            window (only used when *t_picker* is `fzf`).
        templates_dir (pathlib.Path): Directory scanned for available templates.

    Returns:
        str: The template name chosen by the user.

    Raises:
        makefiles.exceptions.NoTemplatesAvailableError: If no templates exist.
        makefiles.exceptions.FZFNotFoundError: If `fzf` is selected but
            the binary is not in `PATH`.
    """
    available_templates: list[str] = _get_available_templates(templates_dir)

    if t_picker == "fzf":
        return picker.fzf(available_templates, height=fzf_height)
    elif t_picker == "manual":
        return picker.manual(available_templates)

    assert_never(t_picker)  # for linter


def runner(cli_arguments: argparse.Namespace, templates_dir: pathlib.Path) -> custom_types.ExitCode:
    """
    Core program logic: dispatches to file-creation or template-copy
    operations based on the parsed CLI arguments.

    Args:
        cli_arguments (argparse.Namespace): Validated namespace from
            :func:`~makefiles.cli_parser.get_cli_args`.
        templates_dir (pathlib.Path): Directory that holds template files.

    Returns:
        custom_types.ExitCode: `0` on success, `1` when any destination
        was skipped.

    Raises:
        makefiles.exceptions.NoTemplatesAvailableError: If `--list` is used
            and no templates exist.
        makefiles.exceptions.TemplateNotFoundError: If the requested template
            does not exist.
        makefiles.exceptions.MKFileException: For other application errors.
    """
    exitcode: custom_types.ExitCode = custom_types.ExitCode(0)

    files: list[str] = cli_arguments.files
    template: str | object | None = cli_arguments.template
    t_picker: Literal["fzf"] | Literal["manual"] = cli_arguments.picker[0]
    fzf_height: custom_types.NaturalNumber = cli_arguments.height[0]
    verbose: bool = cli_arguments.verbose
    dry_run: bool = cli_arguments.dry_run

    if cli_arguments.version:
        cli_io.print(f"{utils.get_version()}\n")
        exitcode = custom_types.ExitCode(1)
        return exitcode

    if cli_arguments.list:
        cli_io.print("\n".join(_get_available_templates(templates_dir)) + "\n")
        return exitcode

    files_paths: tuple[pathlib.Path, ...] = tuple(map(pathlib.Path, files))

    _logger.info(
        "runner: files=%s template=%r verbose=%s dry_run=%s parents=%s",
        files,
        template if isinstance(template, str) or template is None else "<sentinel>",
        verbose,
        dry_run,
        cli_arguments.parents,
    )

    if not template:
        exitcode = (
            fileutils.create_empty_files(
                files_paths,
                overwrite=False,
                parents=cli_arguments.parents,
                verbose=verbose,
                dry_run=dry_run,
            )
            or exitcode
        )
        return exitcode

    if not isinstance(template, str):
        template = _get_template_from_prompt(
            t_picker=t_picker,
            fzf_height=fzf_height,
            templates_dir=templates_dir,
        )

    exitcode = (
        _create_template(
            template,
            files_paths,
            templates_dir=templates_dir,
            overwrite=False,
            parents=cli_arguments.parents,
            verbose=verbose,
            dry_run=dry_run,
        )
        or exitcode
    )

    return exitcode


def main() -> custom_types.ExitCode:
    """
    Entry point for the `mkfile` command-line tool.

    Sets up logging, parses CLI arguments, delegates to :func:`runner`, and
    handles top-level exceptions.  A log entry is written both when the
    program starts and when it terminates — regardless of whether it exits
    normally or via an exception.

    Returns:
        custom_types.ExitCode: Final process exit code.
    """
    setup_logging()
    _logger.info("makefiles-cli started")

    templates_dir_path: pathlib.Path = pathlib.Path(TEMPLATES_DIR)
    exitcode: custom_types.ExitCode = custom_types.ExitCode(0)

    argument_parser: argparse.ArgumentParser = cli_parser.get_parser()

    try:
        cli_arguments: argparse.Namespace = cli_parser.get_cli_args(argument_parser)
        exitcode = runner(cli_arguments, templates_dir_path) or exitcode

    except exceptions.MKFileException as ex:
        cli_io.eprint(f"{argument_parser.prog}: {str(ex)}\n")
        _logger.error("MKFileException: %s", ex)
        exitcode = custom_types.ExitCode(1)

    except KeyboardInterrupt:
        _logger.info("interrupted by user (SIGINT)")
        exitcode = custom_types.ExitCode(130)

    finally:
        _logger.info("makefiles-cli exiting with code %d", exitcode)

    return exitcode
