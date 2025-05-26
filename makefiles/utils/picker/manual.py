import makefiles.types as custom_types
import makefiles.utils.cli_io as cli_io


def prompt(options: list[str]) -> str:
    """
    Create a simple prompt using `print` and `input` function to select
    from a bunch of options. The only way to exit out of this prompt is
    to trigger the `KeyboardInterrupt` exception using Ctrl-c.

    Parameters:
        options(list[str]): list of options to choose from. Must be a list of
            strings.
    """
    options = sorted(options)  # do not modify the parameter

    for index, option in enumerate(options, start=1):
        cli_io.print(f"[{index}]: {option}\n")

    while True:
        try:
            cli_io.print("Choose a template: ")
            choice: custom_types.NaturalNumber = custom_types.NaturalNumber(cli_io.input())
            assert choice <= len(options)
            break
        except (ValueError, TypeError, AssertionError):
            cli_io.eprint("Please insert a valid input\n")

    return options[choice - 1]
