from __future__ import annotations

from typing import Any


class ExitCode(int):
    """
    A strongly-typed representation of a POSIX-compliant process exit code (0–255).

    Only accepts `int` values or string literals composed strictly of digits,
    and ensures the value is within the range [0, 255]. Rejects all other types
    including float, bool, Decimal, and other number-like objects.

    Arguments:
        x (int | str): The exit code. Must be an integer or digit-only string
                       representing a value between 0 and 255 (inclusive).

    Raises:
        TypeError: If the input is not an `int` or a digit-only `str`.
        ValueError: If the integer is not within the valid range [0, 255].

    Examples:
        >>> ExitCode(0)
        0

        >>> ExitCode("42")
        42

        >>> ExitCode(256)
        ValueError: ExitCode must be in range of [0,255], got 256

        >>> ExitCode(3.0)
        TypeError: ExitCode only accepts int or numeric strings, got float

        >>> ExitCode(True)
        TypeError: ExitCode does not accept bool values: True
    """

    def __new__(cls, x: Any, /) -> ExitCode:
        value: int

        if isinstance(x, bool):  # Checking explicitly because `bool` is a subclass of `int`
            raise TypeError(f"ExitCode does not accept bool values: {x!r}")

        if isinstance(x, int):
            value = x
        elif isinstance(x, str):
            if not x.isdigit():
                raise TypeError(f"Invalid literal for ExitCode: {x!r}")
            value = int(x)
        else:
            raise TypeError(f"ExitCode only accepts int or numeric strings, got {type(x).__name__}")

        if not (0 <= value <= 255):
            raise ValueError(f"ExitCode must be in range of [0,255], got {value}")

        return super().__new__(cls, value)
