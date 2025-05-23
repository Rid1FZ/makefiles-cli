import pytest

from makefiles.types import NaturalNumber


class TestNaturalNumber:
    def test_natural_numbers(self) -> None:
        numbers: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        assert all(isinstance(NaturalNumber(n), NaturalNumber) for n in numbers)

    def test_booleans(self) -> None:
        assert NaturalNumber(True) == 1

        with pytest.raises(ValueError):
            _ = NaturalNumber(False)

    def test_complex_numbers(self) -> None:
        with pytest.raises(TypeError):
            _ = NaturalNumber(1 + 2j)

    def test_infinity(self) -> None:
        with pytest.raises(OverflowError):
            _ = NaturalNumber(float("infinity"))
            _ = NaturalNumber(float("-infinity"))

    def test_None(self) -> None:
        with pytest.raises(TypeError):
            _ = NaturalNumber(None)

    def test_non_number(self) -> None:
        with pytest.raises(TypeError):
            _ = NaturalNumber(object())
