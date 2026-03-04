from argparse import Namespace
from unittest import mock

import pytest

import makefiles.cli_parser as cli_parser
from makefiles.types import NaturalNumber


class TestGetCliArgs:
    """Tests for get_cli_args() validation logic."""

    def setup_method(self, _) -> None:
        self.parser = cli_parser.get_parser()

    def _parse(self, argv: list[str]) -> Namespace:
        with mock.patch("sys.argv", ["mkfile"] + argv):
            return cli_parser.get_cli_args(self.parser)

    def test_valid_files_returns_namespace(self) -> None:
        """Providing file arguments should return a valid Namespace."""
        with mock.patch("sys.argv", ["mkfile", "output.txt"]):
            namespace: Namespace = cli_parser.get_cli_args(self.parser)

        assert namespace.files == ["output.txt"]

    def test_no_files_without_version_or_list_raises(self) -> None:
        """No files and no --version/--list should trigger parser.error() -> SystemExit."""
        with mock.patch("sys.argv", ["mkfile"]):
            with pytest.raises(SystemExit):
                cli_parser.get_cli_args(self.parser)

    def test_version_flag_without_files_does_not_raise(self) -> None:
        """--version alone should not raise even without file arguments."""
        with mock.patch("sys.argv", ["mkfile", "--version"]):
            namespace: Namespace = cli_parser.get_cli_args(self.parser)

        assert namespace.version is True

    def test_list_flag_without_files_does_not_raise(self) -> None:
        """--list alone should not raise even without file arguments."""
        with mock.patch("sys.argv", ["mkfile", "--list"]):
            namespace: Namespace = cli_parser.get_cli_args(self.parser)

        assert namespace.list is True

    def test_multiple_files_parsed_correctly(self) -> None:
        """Multiple file arguments should all appear in namespace.files."""
        with mock.patch("sys.argv", ["mkfile", "a.txt", "b.txt", "c.txt"]):
            namespace: Namespace = cli_parser.get_cli_args(self.parser)

        assert namespace.files == ["a.txt", "b.txt", "c.txt"]

    def test_all_options_together(self) -> None:
        """All options combined should parse without error."""
        with mock.patch(
            "sys.argv",
            ["mkfile", "out.py", "--template=pytemplate.py", "--parents", "--picker=fzf", "--height=15"],
        ):
            namespace: Namespace = cli_parser.get_cli_args(self.parser)

        assert namespace.files == ["out.py"]
        assert namespace.template == "pytemplate.py"
        assert namespace.parents is True
        assert namespace.picker == ["fzf"]
        assert namespace.height == [NaturalNumber(15)]
