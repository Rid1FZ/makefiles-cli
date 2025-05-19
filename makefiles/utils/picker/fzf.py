import shutil
import subprocess

import makefiles.exceptions as exceptions

FZF_DEFAULT_FLAGS: list[str] = [
    "--style=minimal",
    "--info=hidden",
    "--keep-right",
]


def prompt(options: list[str], *, height: int = 10) -> str:
    """
    Create a prompt using `fzf` commandline tool to choose from bunch of options.
    This function needs the `fzf` to be installed in the system and binary
    to be available in the `PATH`.

    Parameters:
        options(list[str]): list of options to prompt user to choose from.
            Must be a list of strings.
        height(int): height of `fzf` prompt. Default is 10. Can be negative integer.

    Raises:
        makefiles.exceptions.FZFNotFoundError: if `fzf` not found in `PATH`.
        makefiles.exceptions.FZFError: if `fzf` command returns non-zero returncode.
    """
    if not shutil.which("fzf"):
        raise exceptions.FZFNotFoundError("`fzf` is not found in path")

    options_str: str = "\n".join(options)

    process: subprocess.CompletedProcess = subprocess.run(
        ["fzf", *FZF_DEFAULT_FLAGS, f"--height=~{int(height)}"],
        input=options_str,
        text=True,
        capture_output=True,
    )

    if process.returncode != 0:
        raise exceptions.FZFError("`fzf` command returned non zero exit code")

    return process.stdout.strip("\n")
