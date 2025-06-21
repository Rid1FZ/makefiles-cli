import pytest

from makefiles.types import ExitCode


class TestExitCode:
    def test_out_of_bound(self) -> None:
        with pytest.raises(ValueError):
            _ = ExitCode(-1)
            _ = ExitCode(256)

    def test_booleans(self) -> None:
        assert ExitCode(True) == 1
        assert ExitCode(False) == 0

    def test_complex_numbers(self) -> None:
        with pytest.raises(TypeError):
            _ = ExitCode(1 + 2j)

    def test_infinity(self) -> None:
        with pytest.raises(OverflowError):
            _ = ExitCode(float("infinity"))
            _ = ExitCode(float("-infinity"))

    def test_None(self) -> None:
        with pytest.raises(TypeError):
            _ = ExitCode(None)

    def test_non_number(self) -> None:
        with pytest.raises(TypeError):
            _ = ExitCode(object())
