from pathlib import Path
from unittest import mock

import makefiles.exceptions as exceptions
import makefiles.mkfile as mkfile
import makefiles.utils.cli_io as cli_io
import tests.utils as test_utils
from makefiles.types import ExitCode


class TestMain(test_utils.MakefilesTestBase):
    """Integration-level tests for main() entry point."""

    def test_main_returns_exit_code_int(self) -> None:
        """main() should always return an ExitCode."""
        with (
            mock.patch("sys.argv", ["mkfile", "--version"]),
            mock.patch.object(cli_io, "print"),
        ):
            result: ExitCode = mkfile.main()

        assert isinstance(result, ExitCode)

    def test_main_keyboard_interrupt_returns_130(self) -> None:
        """KeyboardInterrupt inside runner should yield ExitCode(130)."""
        with (
            mock.patch("sys.argv", ["mkfile", "file.txt"]),
            mock.patch("makefiles.mkfile.runner", side_effect=KeyboardInterrupt),
        ):
            result: ExitCode = mkfile.main()

        assert result == ExitCode(130)

    def test_main_mkfile_exception_returns_1(self) -> None:
        """MKFileException inside runner should be caught and return ExitCode(1)."""
        with (
            mock.patch("sys.argv", ["mkfile", "file.txt"]),
            mock.patch(
                "makefiles.mkfile.runner",
                side_effect=exceptions.MKFileException("something went wrong"),
            ),
            mock.patch.object(cli_io, "eprint"),
        ):
            result: ExitCode = mkfile.main()

        assert result == ExitCode(1)

    def test_main_creates_file_end_to_end(self) -> None:
        """End-to-end: main() with a real file path should create that file."""
        dest: Path = self.tempdir.joinpath("e2e_output.txt")

        templates_dir: Path = self.tempdir.joinpath("templates")
        templates_dir.mkdir()

        with (
            mock.patch("sys.argv", ["mkfile", str(dest)]),
            mock.patch("makefiles.mkfile.TEMPLATES_DIR", str(templates_dir)),
        ):
            result: ExitCode = mkfile.main()

        assert result == ExitCode(0)
        assert dest.is_file()

    def test_main_prints_error_message_on_exception(self) -> None:
        """main() should print the exception message to stderr on MKFileException."""
        with (
            mock.patch("sys.argv", ["mkfile", "file.txt"]),
            mock.patch(
                "makefiles.mkfile.runner",
                side_effect=exceptions.MKFileException("custom error text"),
            ),
            mock.patch.object(cli_io, "eprint") as mock_eprint,
        ):
            mkfile.main()

        printed: list[str] = mock_eprint.call_args[0][0]

        assert "custom error text" in printed
