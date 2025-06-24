import subprocess
from unittest import mock

import pytest

import makefiles.exceptions as exceptions
from makefiles.types import NaturalNumber
from makefiles.utils.picker import fzf
from makefiles.utils.picker.fzf import FZF_DEFAULT_FLAGS


@mock.patch("shutil.which", return_value="/usr/bin/fzf")
@mock.patch("subprocess.run")
class TestFzf:
    def test_returns_selected_option(self, mock_run, _):
        """Should return the user's selected value."""
        options = ["apple", "banana", "cherry"]
        expected = "banana"

        mock_run.return_value = subprocess.CompletedProcess(
            args=["fzf"],
            returncode=0,
            stdout=expected + "\n",
            stderr="",
        )

        result = fzf(options)
        assert result == expected

        mock_run.assert_called_once_with(
            ["fzf", *FZF_DEFAULT_FLAGS, "--height=~10"],
            input="\n".join(options),
            text=True,
            capture_output=True,
        )

    def test_returns_stripped_output(self, mock_run, _):
        """Should strip trailing newlines from fzf output."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=["fzf"],
            returncode=0,
            stdout="grape\n\n\n",
            stderr="",
        )

        assert fzf(["grape"]) == "grape"

    def test_uses_custom_height(self, mock_run, _):
        """Should pass custom height to fzf."""
        height = NaturalNumber(25)

        mock_run.return_value = subprocess.CompletedProcess(
            args=["fzf"],
            returncode=0,
            stdout="apple\n",
            stderr="",
        )

        fzf(["apple", "banana"], height=height)

        assert f"--height=~{height}" in mock_run.call_args[0][0]

    def test_fzf_not_found(self, *_):
        """Raises FZFNotFoundError when fzf is not found in PATH."""
        with (
            mock.patch("shutil.which", return_value=None),  # overwriting class default patch
            pytest.raises(exceptions.FZFNotFoundError),
        ):
            fzf(["one", "two", "three"])

    def test_fzf_exit_code_non_zero(self, mock_run, _):
        """Raises FZFError if fzf exits with non-zero code other than 130."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=["fzf"],
            returncode=1,
            stdout="",
            stderr="error",
        )

        with pytest.raises(exceptions.FZFError):
            fzf(["one", "two", "three"])

    def test_keyboard_interrupt(self, mock_run, _):
        """Raises KeyboardInterrupt if fzf returns exit code 130."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=["fzf"],
            returncode=130,
            stdout="",
            stderr="",
        )

        with pytest.raises(KeyboardInterrupt):
            fzf(["one", "two", "three"])
