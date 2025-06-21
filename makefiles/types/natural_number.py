from __future__ import annotations


class NaturalNumber(int):
    """
    A strict subclass of `int` that represents natural numbers (positive integers > 0).

    This class enforces validation at instantiation time. Any attempt to create a
    `NaturalNumber` with a non-integer, zero, or negative value will raise an error.

    Parameters:
        x (Any): A value that can be converted to an integer. Must represent a positive
            integer greater than zero. Accepts integers, numeric strings, or any type
            that supports conversion via `int(x)`.

    Examples:
        >>> NaturalNumber(5)
        5
        >>> NaturalNumber("3")
        3
        >>> NaturalNumber(-1)
        ValueError: NaturalNumber must be greater than 0, got -1
        >>> NaturalNumber("abc")
        TypeError: Invalid literal for NaturalNumber: 'abc'

    Raises:
        TypeError: If the input cannot be converted to an integer.
        ValueError: If the integer is not greater than 0.
    """

    def __new__(cls, x, /) -> NaturalNumber:
        if not isinstance(x, int):
            try:
                x = int(x)
            except (TypeError, ValueError):
                raise TypeError(f"Invalid literal for NaturalNumber: {x!r}") from None

        if x <= 0:
            raise ValueError(f"NaturalNumber must be greater than 0, got {x}")

        return super().__new__(cls, x)
