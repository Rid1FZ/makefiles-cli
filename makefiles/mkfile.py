import argparse
import os
import pathlib
import typing

import makefiles.cli_parser as cli_parser
import makefiles.exceptions as exceptions
import makefiles.types as custom_types
import makefiles.utils as utils
import makefiles.utils.cli_io as cli_io
import makefiles.utils.dirwalker as dirwalker
import makefiles.utils.fileutils as fileutils
import makefiles.utils.picker as picker

TEMPLATES_DIR: str = os.environ.get("XDG_TEMPLATES_DIR", f"{os.environ["HOME"]}/Templates")


def _get_available_templates(templates_dir: pathlib.Path) -> list[str]:
    try:
        available_templates: list[str] = dirwalker.listf(templates_dir)
        if not available_templates:
            raise exceptions.NoTemplatesAvailableError("no templates found")
    except exceptions.InvalidPathError:
        raise exceptions.NoTemplatesAvailableError("could not find template directory") from None

    return available_templates


def _create_template(
    template: str,
    *destinations: pathlib.Path,
    templates_dir: pathlib.Path,
    overwrite: bool,
    parents: bool,
) -> custom_types.ExitCode:
    exitcode: custom_types.ExitCode = custom_types.ExitCode(0)

    template_path: pathlib.Path = templates_dir.joinpath(template)
    try:
        exitcode = fileutils.copy(template_path, *destinations, overwrite=overwrite, parents=parents) or exitcode
    except exceptions.SourceNotFoundError:
        raise exceptions.TemplateNotFoundError(f"template {template} not found") from None

    return exitcode


def _get_template_from_prompt(
    *,
    t_picker: typing.Literal["fzf"] | typing.Literal["manual"],
    fzf_height: custom_types.NaturalNumber = custom_types.NaturalNumber(10),
    templates_dir: pathlib.Path,
) -> str:
    """
    Prompt the user using the fzf or manual prompt to choose template.
    """
    available_templates: list[str] = _get_available_templates(templates_dir)

    if t_picker == "fzf":
        return picker.fzf(available_templates, height=fzf_height)
    elif t_picker == "manual":
        return picker.manual(available_templates)


def runner(cli_arguments: argparse.Namespace, templates_dir: pathlib.Path) -> custom_types.ExitCode:
    exitcode: custom_types.ExitCode = custom_types.ExitCode(0)

    files: list[str] = cli_arguments.files
    template: str | object | None = cli_arguments.template
    t_picker: typing.Literal["fzf"] | typing.Literal["manual"] = cli_arguments.picker[0]
    fzf_height: custom_types.NaturalNumber = cli_arguments.height[0]

    if cli_arguments.version:
        cli_io.print(f"{utils.get_version()}\n")
        exitcode = custom_types.ExitCode(1)
        return exitcode

    if cli_arguments.list:
        cli_io.print(f"{"\n".join(_get_available_templates(templates_dir))}\n")
        return exitcode

    files_paths: list[pathlib.Path] = list(map(pathlib.Path, files))

    if not template:
        exitcode = (
            fileutils.create_empty_files(*files_paths, overwrite=False, parents=cli_arguments.parents) or exitcode
        )
        return exitcode

    if not isinstance(template, str):
        template = _get_template_from_prompt(
            t_picker=t_picker,
            fzf_height=fzf_height,
            templates_dir=templates_dir,
        )

    # fmt:off
    exitcode = _create_template(
        template,
        *files_paths,
        templates_dir=templates_dir,
        overwrite=False,
        parents=cli_arguments.parents,
    ) or exitcode 
    # fmt:on

    return exitcode


def main() -> custom_types.ExitCode:
    templates_dir_path: pathlib.Path = pathlib.Path(TEMPLATES_DIR)
    exitcode: custom_types.ExitCode = custom_types.ExitCode(0)

    argument_parser: argparse.ArgumentParser = cli_parser.get_parser()
    cli_arguments: argparse.Namespace = cli_parser.get_cli_args(argument_parser)

    try:
        exitcode = runner(cli_arguments, templates_dir_path) or exitcode
    except exceptions.MKFileException as ex:
        cli_io.eprint(f"{argument_parser.prog}: {str(ex)}\n")
        exitcode = custom_types.ExitCode(1)
    except KeyboardInterrupt:
        exitcode = custom_types.ExitCode(130)

    return exitcode
