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


def _create_template(template: str, *destinations: pathlib.Path, templates_dir: pathlib.Path) -> None:
    template_path: pathlib.Path = templates_dir.joinpath(template)
    try:
        fileutils.copy(template_path, *destinations, overwrite=False)
    except exceptions.SourceNotFoundError:
        raise exceptions.TemplateNotFoundError(f"template {template} not found") from None


def _get_template_from_prompt(
    *,
    t_picker: typing.Literal["fzf"] | typing.Literal["manual"],
    fzf_height: custom_types.NaturalNumber = custom_types.NaturalNumber(10),
    templates_dir: pathlib.Path,
) -> str:
    """
    Prompt the user using the fzf or manual prompt to choose template.
    """
    try:
        available_templates: list[str] = dirwalker.listf(templates_dir)
        if not available_templates:
            raise exceptions.NoTemplatesAvailableError("no templates found")
    except exceptions.InvalidPathError:
        raise exceptions.NoTemplatesAvailableError("could not find template directory") from None

    if t_picker == "fzf":
        return picker.fzf(available_templates, height=fzf_height)
    elif t_picker == "manual":
        return picker.manual(available_templates)


def runner(cli_arguments: argparse.Namespace) -> None:
    templates_dir_path: pathlib.Path = pathlib.Path(TEMPLATES_DIR)

    files: list[str] = cli_arguments.files
    template: str | object | None = cli_arguments.template
    t_picker: typing.Literal["fzf"] | typing.Literal["manual"] = cli_arguments.picker[0]
    fzf_height: custom_types.NaturalNumber = cli_arguments.height[0]

    files_paths: list[pathlib.Path] = list(map(pathlib.Path, files))

    if not template:
        fileutils.create_empty_files(*files_paths)
        return

    if not isinstance(template, str):
        template = _get_template_from_prompt(
            t_picker=t_picker,
            fzf_height=fzf_height,
            templates_dir=templates_dir_path,
        )

    _create_template(template, *files_paths, templates_dir=templates_dir_path)


def main() -> int:
    argument_parser: argparse.ArgumentParser = cli_parser.get_parser()
    cli_arguments: argparse.Namespace = argument_parser.parse_args()
    try:
        runner(cli_arguments)
    except exceptions.MKFileException as ex:
        cli_io.eprint(f"{argument_parser.prog}: {str(ex)}\n")
        return 1
    except KeyboardInterrupt as ex:
        return 130
    else:
        return 0
