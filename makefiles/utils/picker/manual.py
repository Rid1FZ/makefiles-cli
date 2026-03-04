import makefiles.types as custom_types
import makefiles.utils.cli_io as cli_io


def prompt(options: list[str]) -> str:
    """
    Displays a numbered list of options and prompts the user to select one via keyboard input.

    Args:
        options (list[str]): A list of string options to present to the user for selection.
            NOTE: the given strings will be sorted when prompting for input.

    Returns:
        str: The selected option from the list, based on user input.
    """
    sorted_options = sorted(options)

    for index, option in enumerate(sorted_options, start=1):
        cli_io.eprint(f"[{index}]: {option}\n")

    while True:
        try:
            cli_io.eprint("Choose a template: ")
            choice: custom_types.NaturalNumber = custom_types.NaturalNumber(cli_io.input())
            assert choice <= len(sorted_options)
            break
        except (ValueError, TypeError, AssertionError):
            cli_io.eprint("Please insert a valid input\n")

    return sorted_options[choice - 1]
