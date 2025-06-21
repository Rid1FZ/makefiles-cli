from __future__ import annotations


class ExitCode(int):
    """
    A strongly-typed representation of a POSIX-compliant process exit code.

    This class ensures that only valid exit codes (unsigned 8-bit integers, 0–255)
    can be instantiated. It inherits from `int`, so it can be used anywhere a regular
    integer is accepted, such as in `sys.exit()` or `subprocess` interfaces.

    Parameters:
        x (int | str): The value to be validated and converted into a valid exit code.
                       Non-integer inputs are attempted to be cast to `int`.

    Raises:
        TypeError: If the input is not convertible to an integer.
        ValueError: If the resulting integer is outside the range [0, 255].

    Example:
        >>> code = ExitCode(0)
        >>> sys.exit(code)

        >>> code = ExitCode("42")
        >>> print(code)  # 42

        >>> ExitCode(999)
        ValueError: ExitCode must be in range of [0,255], got 999
    """

    def __new__(cls, x, /) -> ExitCode:
        if not isinstance(x, int):
            try:
                x = int(x)
            except (TypeError, ValueError):
                raise TypeError(f"Invalid literal for ExitCode: {x!r}") from None

        if not (0 <= x <= 255):
            raise ValueError(f"ExitCode must be in range of [0,255], got {x}")

        return super().__new__(cls, x)
