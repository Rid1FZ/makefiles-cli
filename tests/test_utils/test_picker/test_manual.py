from unittest import mock

import pytest

import makefiles.utils.cli_io as cli_io
from makefiles.utils.picker import manual


class TestSimplePrompt:
    def test_returns_correct_selection(self):
        """Should return the correct option based on valid user input."""
        options: list[str] = ["delta", "alpha", "charlie"]
        user_input: str = "2"  # sorted: ["alpha", "charlie", "delta"] => index 2 = "charlie"

        with (
            mock.patch.object(cli_io, "input", return_value=user_input),
            mock.patch.object(cli_io, "print") as mock_print,
        ):

            result: str = manual(options)
            assert result == "charlie"

            # Print should include numbered options
            printed_lines: list[str] = [call.args[0] for call in mock_print.call_args_list]
            assert "[1]: alpha" in printed_lines[0]
            assert "[2]: charlie" in printed_lines[1]
            assert "[3]: delta" in printed_lines[2]

    @pytest.mark.parametrize("bad_input", ["abc", "0", "-1", "99", "", "3.14"])
    def test_invalid_inputs_retry_until_valid(self, bad_input: str):
        """Should loop on invalid inputs until a valid selection is made."""
        options: list[str] = ["one", "two", "three"]
        valid_input: str = "1"

        with (
            mock.patch.object(cli_io, "input", side_effect=[bad_input, valid_input]),
            mock.patch.object(cli_io, "print") as mock_print,
            mock.patch.object(cli_io, "eprint") as mock_eprint,
        ):
            result: str = manual(options)
            assert result == "one"
            mock_eprint.assert_called_with("Please insert a valid input\n")

    def test_exact_bounds_selection(self):
        """Should accept lowest and highest valid index values."""
        options: list[str] = ["x", "a", "z"]  # sorted: ["a", "x", "z"]

        for index, expected in enumerate(sorted(options), start=1):
            with mock.patch.object(cli_io, "input", return_value=str(index)):
                assert manual(options) == expected
