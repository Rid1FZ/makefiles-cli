import makefiles.types as custom_types


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
        print(f"[{index}]: {option}")

    while True:
        try:
            choice: custom_types.NaturalNumber = custom_types.NaturalNumber(input("Choose a template: "))
            assert choice <= len(options)
            break
        except (ValueError, TypeError, AssertionError):
            print("Please insert a valid input")

    return options[choice - 1]
