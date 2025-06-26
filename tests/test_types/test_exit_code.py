from typing import Any

import pytest

from makefiles.types import ExitCode


class TestExitCode:
    """Unit tests for the ExitCode type with strict validation."""

    @pytest.mark.parametrize(
        "valid_input, expected",
        [
            (0, 0),
            (1, 1),
            (42, 42),
            (255, 255),
            ("0", 0),
            ("255", 255),
            ("100", 100),
        ],
    )
    def test_valid_exit_codes(self, valid_input: str | int, expected: int) -> None:
        """Test valid exit codes as int or digit-only string."""
        code: ExitCode = ExitCode(valid_input)
        assert isinstance(code, ExitCode)
        assert isinstance(code, int)
        assert code == expected

    @pytest.mark.parametrize(
        "invalid_type",
        [
            3.0,
            42.5,
            complex(1, 2),
            True,  # explicitly disallowed
            None,
            [],
            {},
            set(),
            object(),
            b"10",
            bytearray(b"20"),
            memoryview(b"30"),
        ],
    )
    def test_invalid_exitcode_type_raises_typeerror(self, invalid_type: Any) -> None:
        """Test that disallowed types raise TypeError."""
        with pytest.raises(TypeError, match="ExitCode"):
            ExitCode(invalid_type)

    @pytest.mark.parametrize(
        "bad_str",
        [
            "3.14",  # decimal string
            "-1",  # negative string
            "abc",  # non-numeric
            "",  # empty
            "+42",  # sign disallowed
            " 1",  # leading space
        ],
    )
    def test_invalid_exitcode_string_raises_typeerror(self, bad_str: str):
        """Test that invalid strings raise TypeError."""
        with pytest.raises(TypeError, match=r"Invalid literal for ExitCode"):
            ExitCode(bad_str)

    @pytest.mark.parametrize(
        "out_of_range",
        [
            -1,
            256,
            999,
            "300",
        ],
    )
    def test_exitcode_out_of_range_raises_valueerror(self, out_of_range: str | int):
        """Test that out-of-range values raise ValueError."""
        with pytest.raises(ValueError, match=r"ExitCode must be in range of \[0,255\]"):
            ExitCode(out_of_range)
