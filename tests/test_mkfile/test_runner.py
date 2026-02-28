from argparse import Namespace
from pathlib import Path
from unittest import mock

import pytest

import makefiles.exceptions as exceptions
import makefiles.mkfile as mkfile
import makefiles.utils.cli_io as cli_io
import tests.utils as test_utils
from makefiles.types import ExitCode, NaturalNumber


def _make_namespace(**kwargs) -> Namespace:
    """Build an argparse.Namespace with sensible defaults for runner() tests."""
    defaults = dict(
        files=[],
        version=False,
        list=False,
        template=None,
        parents=False,
        picker=["manual"],
        height=[NaturalNumber(10)],
    )
    defaults.update(kwargs)
    return Namespace(**defaults)


class TestRunner(test_utils.MakefilesTestBase):
    def _get_templates_dir(self) -> tuple[Path, bytes]:
        templates_dir: Path = self.tempdir.joinpath("templates")
        templates_dir.mkdir()

        random_content: bytes = test_utils.get_random_str(special_chars=True).encode()
        templates_dir.joinpath("hello.py").write_bytes(random_content)

        return (templates_dir, random_content)

    def test_version_prints_and_returns_exitcode_1(self) -> None:
        """--version should print version info and return ExitCode(1)."""
        namespace: Namespace = _make_namespace(version=True)

        with mock.patch.object(cli_io, "print") as mock_print:
            result: ExitCode = mkfile.runner(namespace, self.tempdir)

        assert result == ExitCode(1)
        mock_print.assert_called_once()

    def test_list_prints_templates_and_returns_0(self) -> None:
        """--list should print available templates and return ExitCode(0)."""
        templates_dir: Path

        templates_dir, _ = self._get_templates_dir()
        namespace: Namespace = _make_namespace(list=True)

        with mock.patch.object(cli_io, "print") as mock_print:
            result: ExitCode = mkfile.runner(namespace, templates_dir)

        assert result == ExitCode(0)
        printed: list[str] = mock_print.call_args[0][0]
        assert "hello.py" in printed

    def test_list_raises_when_no_templates(self) -> None:
        """--list should raise NoTemplatesAvailableError if template dir is empty."""
        namespace: Namespace = _make_namespace(list=True)

        with pytest.raises(exceptions.NoTemplatesAvailableError):
            mkfile.runner(namespace, self.tempdir)

    def test_creates_empty_files_when_no_template(self) -> None:
        """Without --template, runner should create empty files."""
        dest: Path = self.tempdir.joinpath("new_file.txt")
        namespace: Namespace = _make_namespace(files=[str(dest)])

        result: ExitCode = mkfile.runner(namespace, self.tempdir)

        assert result == ExitCode(0)
        assert dest.is_file()
        assert dest.stat().st_size == 0

    def test_returns_exit_1_when_file_already_exists(self) -> None:
        """Should return ExitCode(1) if destination already exists."""
        dest: Path = self.tempdir.joinpath("existing.txt")
        test_utils.create_file(dest)

        namespace: Namespace = _make_namespace(files=[str(dest)])

        result: ExitCode = mkfile.runner(namespace, self.tempdir)
        assert result == ExitCode(1)

    def test_creates_parent_dirs_when_parents_flag_set(self) -> None:
        """With --parents, runner should create missing parent directories."""
        dest: Path = self.tempdir.joinpath("subdir").joinpath("nested.txt")
        namespace: Namespace = _make_namespace(files=[str(dest)], parents=True)
        result: ExitCode = mkfile.runner(namespace, self.tempdir)

        assert result == ExitCode(0)
        assert dest.is_file()

    def test_creates_file_from_named_template(self) -> None:
        """With --template=X, runner should copy the template to destinations."""
        templates_dir: Path
        templates_content: bytes

        templates_dir, templates_content = self._get_templates_dir()
        dest: Path = self.tempdir.joinpath("output.py")
        namespace: Namespace = _make_namespace(files=[str(dest)], template="hello.py")

        result: ExitCode = mkfile.runner(namespace, templates_dir)

        assert result == ExitCode(0)
        assert dest.read_bytes() == templates_content

    def test_raises_on_unknown_template_name(self) -> None:
        """With --template=UNKNOWN, runner should raise TemplateNotFoundError."""
        templates_dir: Path

        templates_dir, _ = self._get_templates_dir()
        dest: Path = self.tempdir.joinpath("output.py")
        namespace: Namespace = _make_namespace(files=[str(dest)], template="no_such_template.py")

        with pytest.raises(exceptions.TemplateNotFoundError):
            mkfile.runner(namespace, templates_dir)

    def test_prompts_for_template_when_sentinel_given(self) -> None:
        """When template is a sentinel (not str), runner should invoke picker."""
        templates_dir: Path
        templates_content: bytes

        templates_dir, templates_content = self._get_templates_dir()
        dest: Path = self.tempdir.joinpath("output.py")
        # Pass a non-string, non-None sentinel (as the CLI does for bare --template)
        namespace: Namespace = _make_namespace(files=[str(dest)], template=object())

        with mock.patch("makefiles.utils.picker.manual", return_value="hello.py"):
            result: ExitCode = mkfile.runner(namespace, templates_dir)

        assert result == ExitCode(0)
        assert dest.read_bytes() == templates_content
