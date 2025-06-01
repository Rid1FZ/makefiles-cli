import shutil
import subprocess

import makefiles.exceptions as exceptions
import makefiles.types as custom_types

FZF_DEFAULT_FLAGS: list[str] = [
    "--style=minimal",
    "--info=hidden",
    "--keep-right",
]


def prompt(options: list[str], *, height: custom_types.NaturalNumber = custom_types.NaturalNumber(10)) -> str:
    """
    Displays an interactive fuzzy-selection prompt using `fzf` and returns the user's selection.

    Args:
        options (list[str]): A list of string options to display in the selection interface.
        height (custom_types.NaturalNumber, optional): Approximate terminal height percentage for the `fzf` UI.
            Defaults to 10. The value is interpreted as `--height=~<value>` by `fzf`.

    Returns:
        str: The selected option as returned by `fzf`, with trailing newline removed.

    Raises:
        exceptions.FZFNotFoundError: If the `fzf` binary is not found in the system PATH.
        KeyboardInterrupt: If the user interrupts the prompt using Ctrl+C (fzf returns exit code 130).
        exceptions.FZFError: If `fzf` exits with a non-zero return code other than 130.
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
        if process.returncode == 130:
            raise KeyboardInterrupt
        raise exceptions.FZFError("`fzf` command returned non zero exit code")

    return process.stdout.strip("\n")
