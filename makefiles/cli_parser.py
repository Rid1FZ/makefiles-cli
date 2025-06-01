import argparse

import makefiles.types as custom_types


def get_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="mkfile",
        description="A lightweight Python utility for file creation and template generation from XDG_TEMPLATES_DIR",
    )

    parser.add_argument(
        "files",
        nargs="+",
        action="store",
        help="paths to files to create",
    )

    parser.add_argument(
        "-t",
        "--template",
        nargs="?",
        action="store",
        type=str,
        const=object(),
        default=None,
        help="template to generate. If no template is provided, it will prompt for template.",
    )

    parser.add_argument(
        "-p",
        "--picker",
        nargs=1,
        action="store",
        type=str,
        choices=["fzf", "manual"],
        default=["manual"],
        help="which template picker to use. If picker is `fzf`, fzf must be present in PATH. Default is `manual`.",
    )

    parser.add_argument(
        "-H",
        "--height",
        nargs=1,
        action="store",
        type=custom_types.NaturalNumber,
        default=[custom_types.NaturalNumber(10)],
        help="height of fzf window if fzf is used as template picker.",
    )

    return parser
