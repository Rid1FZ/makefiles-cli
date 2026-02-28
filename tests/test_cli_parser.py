import argparse
from argparse import Namespace
from unittest import mock

import pytest

import makefiles.cli_parser as cli_parser
from makefiles.types import NaturalNumber


class TestGetParser:
    """Tests for the argument parser structure returned by get_parser()."""

    def setup_method(self, _) -> None:
        self.parser: argparse.ArgumentParser = cli_parser.get_parser()

    def test_returns_argument_parser(self) -> None:
        """get_parser() should return an ArgumentParser instance."""
        assert isinstance(self.parser, argparse.ArgumentParser)

    def test_prog_name_is_mkfile(self) -> None:
        """Parser prog should be 'mkfile'."""
        assert self.parser.prog == "mkfile"

    # --- files argument ---

    def test_files_accepts_multiple_paths(self) -> None:
        """'files' positional argument should accept multiple values."""
        namespace: Namespace = self.parser.parse_args(["a.txt", "b.txt", "c.txt"])

        assert namespace.files == ["a.txt", "b.txt", "c.txt"]

    def test_files_defaults_to_empty_list(self) -> None:
        """'files' should be empty list when --version is used and files omitted."""
        namespace: Namespace = self.parser.parse_args(["--version"])

        assert namespace.files == []

    # --- --version flag ---

    def test_version_flag_defaults_to_false(self) -> None:
        """--version should default to False."""
        namespace: Namespace = self.parser.parse_args(["dummy.txt"])

        assert namespace.version is False

    def test_version_flag_sets_true(self) -> None:
        """--version flag should set version=True."""
        namespace: Namespace = self.parser.parse_args(["--version"])

        assert namespace.version is True

    # --- --template / -t argument ---

    def test_template_defaults_to_none(self) -> None:
        """--template should default to None when not provided."""
        namespace: Namespace = self.parser.parse_args(["file.txt"])

        assert namespace.template is None

    def test_template_with_value(self) -> None:
        """--template=X should set template to the string 'X'."""
        namespace: Namespace = self.parser.parse_args(["file.txt", "--template=mytemplate.py"])

        assert namespace.template == "mytemplate.py"

    def test_template_short_flag(self) -> None:
        """-t X should set template to 'X'."""
        namespace: Namespace = self.parser.parse_args(["file.txt", "-t", "mytemplate.py"])

        assert namespace.template == "mytemplate.py"

    def test_template_without_value_sets_sentinel(self) -> None:
        """--template with no value should set template to the sentinel object (not str/None)."""
        namespace: Namespace = self.parser.parse_args(["file.txt", "--template"])

        assert namespace.template is not None
        assert not isinstance(namespace.template, str)

    # --- --parents / -p flag ---

    def test_parents_defaults_to_false(self) -> None:
        """--parents should default to False."""
        namespace: Namespace = self.parser.parse_args(["file.txt"])

        assert namespace.parents is False

    def test_parents_flag_sets_true(self) -> None:
        """--parents flag should set parents=True."""
        namespace: Namespace = self.parser.parse_args(["file.txt", "--parents"])

        assert namespace.parents is True

    def test_parents_short_flag(self) -> None:
        """-p flag should set parents=True."""
        namespace: Namespace = self.parser.parse_args(["file.txt", "-p"])

        assert namespace.parents is True

    # --- --picker / -P argument ---

    def test_picker_defaults_to_manual(self) -> None:
        """--picker should default to ['manual']."""
        namespace: Namespace = self.parser.parse_args(["file.txt"])

        assert namespace.picker == ["manual"]

    def test_picker_fzf(self) -> None:
        """--picker=fzf should set picker to ['fzf']."""
        namespace: Namespace = self.parser.parse_args(["file.txt", "--picker=fzf"])

        assert namespace.picker == ["fzf"]

    def test_picker_invalid_choice_raises(self) -> None:
        """--picker with invalid choice should raise SystemExit."""
        with pytest.raises(SystemExit):
            self.parser.parse_args(["file.txt", "--picker=rofi"])

    # --- --height / -H argument ---

    def test_height_defaults_to_10(self) -> None:
        """--height should default to [NaturalNumber(10)]."""
        namespace: Namespace = self.parser.parse_args(["file.txt"])

        assert namespace.height == [NaturalNumber(10)]

    def test_height_custom_value(self) -> None:
        """--height=20 should set height to [NaturalNumber(20)]."""
        namespace: Namespace = self.parser.parse_args(["file.txt", "--height=20"])

        assert namespace.height == [NaturalNumber(20)]

    def test_height_zero_raises(self) -> None:
        """--height=0 should raise SystemExit because NaturalNumber(0) is invalid."""
        with pytest.raises(SystemExit):
            self.parser.parse_args(["file.txt", "--height=0"])

    # --- --list / -l flag ---

    def test_list_defaults_to_false(self) -> None:
        """--list should default to False."""
        namespace: Namespace = self.parser.parse_args(["file.txt"])

        assert namespace.list is False

    def test_list_flag_sets_true(self) -> None:
        """--list flag should set list=True."""
        namespace: Namespace = self.parser.parse_args(["--list"])

        assert namespace.list is True

    def test_list_short_flag(self) -> None:
        """-l flag should set list=True."""
        namespace: Namespace = self.parser.parse_args(["-l"])

        assert namespace.list is True


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
