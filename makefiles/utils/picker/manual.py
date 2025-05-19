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

    choice: int = -1
    while True:
        try:
            choice = int(input("Choose a template: "))
            assert 0 < choice <= len(options)
            break
        except (ValueError, AssertionError):
            print("Please insert a valid input")

    return options[choice - 1]
