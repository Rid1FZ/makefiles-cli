from typing import Any

import pytest

from makefiles.types import NaturalNumber


class TestNaturalNumber:
    """Unit tests for the NaturalNumber type with strict validation."""

    @pytest.mark.parametrize(
        "valid_input, expected",
        [
            (1, 1),
            (42, 42),
            (999999, 999999),
            ("1", 1),
            ("500", 500),
        ],
    )
    def test_valid_natural_numbers(self, valid_input: Any, expected: Any) -> None:
        """Test valid natural numbers from int and digit-only str."""
        n = NaturalNumber(valid_input)
        assert isinstance(n, NaturalNumber)
        assert isinstance(n, int)
        assert n == expected

    @pytest.mark.parametrize(
        "invalid_type",
        [
            0,
            -1,
            -100,
            3.0,
            5.5,
            complex(1, 1),
            True,  # explicitly rejected
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
    def test_invalid_naturalnumber_type_raises_typeerror_or_valueerror(self, invalid_type: Any) -> None:
        """Test that invalid types raise appropriate errors."""
        with pytest.raises((TypeError, ValueError), match="NaturalNumber"):
            NaturalNumber(invalid_type)

    @pytest.mark.parametrize(
        "bad_str",
        [
            "0",  # valid string but fails value check
            "-1",
            "abc",
            "4.5",
            "",
            "+5",
            " 1",
        ],
    )
    def test_invalid_naturalnumber_string_raises_typeerror_or_valueerror(self, bad_str: Any) -> None:
        """Test that invalid string inputs raise appropriate errors."""
        with pytest.raises((TypeError, ValueError), match="NaturalNumber"):
            NaturalNumber(bad_str)
