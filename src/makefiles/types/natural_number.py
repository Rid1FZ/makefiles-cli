from __future__ import annotations

from typing import Any


class NaturalNumber(int):
    """
    A strongly-typed representation of a natural number (positive integer > 0).

    Only accepts literal `int` values greater than 0 or digit-only `str` literals
    convertible to such integers. Rejects float, bool, Decimal, and other numeric types
    to ensure semantic and type safety.

    Arguments:
        x (int | str): A positive integer greater than 0, either as an int or
                       a digit-only string. Other types are rejected.

    Raises:
        TypeError: If the input is not an `int` or digit-only `str`.
        ValueError: If the integer is not strictly greater than 0.

    Examples:
        >>> NaturalNumber(1)
        1

        >>> NaturalNumber("17")
        17

        >>> NaturalNumber(0)
        ValueError: NaturalNumber must be greater than 0, got 0

        >>> NaturalNumber("abc")
        TypeError: Invalid literal for NaturalNumber: 'abc'

        >>> NaturalNumber(3.0)
        TypeError: NaturalNumber only accepts int or digit-only strings, got float

        >>> NaturalNumber(True)
        TypeError: NaturalNumber does not accept bool values: True
    """

    def __new__(cls, x: Any, /) -> NaturalNumber:
        value: int

        if isinstance(x, bool):  # Checking explicitly because `bool` is a subclass of `int`
            raise TypeError(f"NaturalNumber does not accept bool values: {x!r}")

        if isinstance(x, int):
            value = x
        elif isinstance(x, str):
            if not x.isdigit():
                raise TypeError(f"Invalid literal for NaturalNumber: {x!r}")
            value = int(x)
        else:
            raise TypeError(f"NaturalNumber only accepts int or digit-only strings, got {type(x).__name__}")

        if value <= 0:
            raise ValueError(f"NaturalNumber must be greater than 0, got {value}")

        return super().__new__(cls, value)
