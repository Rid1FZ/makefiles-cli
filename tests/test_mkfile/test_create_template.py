from pathlib import Path

import pytest

import makefiles.exceptions as exceptions
import makefiles.mkfile as mkfile
import tests.utils as test_utils
from makefiles.types import ExitCode


class TestCreateTemplate(test_utils.MakefilesTestBase):
    def _setup_templates_dir(self) -> tuple[Path, bytes]:
        templates_dir: Path = self.tempdir.joinpath("templates")
        templates_dir.mkdir()

        random_content: bytes = test_utils.get_random_str(special_chars=True).encode()
        sample_template_path: Path = templates_dir.joinpath("script.py")
        templates_dir.joinpath(sample_template_path).write_bytes(random_content)

        return (templates_dir, random_content)

    def test_copies_template_to_destination(self) -> None:
        """Should copy the named template to each destination."""
        templates_dir: Path
        templates_content: bytes

        templates_dir, templates_content = self._setup_templates_dir()
        dest: Path = self.tempdir.joinpath("output.py")

        result: ExitCode = mkfile._create_template("script.py", (dest,), templates_dir, overwrite=False, parents=False)

        assert result == ExitCode(0)
        assert dest.is_file()
        assert dest.read_bytes() == templates_content

    def test_raises_template_not_found_error(self) -> None:
        """Should raise TemplateNotFoundError when the named template doesn't exist."""
        templates_dir: Path

        templates_dir, _ = self._setup_templates_dir()
        dest: Path = self.tempdir.joinpath("output.py")

        with pytest.raises(exceptions.TemplateNotFoundError):
            mkfile._create_template("nonexistent.py", (dest,), templates_dir, overwrite=False, parents=False)

    def test_returns_exit_code_1_when_dest_exists_no_overwrite(self) -> None:
        """Should return ExitCode(1) when destination exists and overwrite=False."""
        templates_dir: Path

        templates_dir, _ = self._setup_templates_dir()
        dest: Path = self.tempdir.joinpath("output.py")
        test_utils.create_file(dest)

        result: ExitCode = mkfile._create_template("script.py", (dest,), templates_dir, overwrite=False, parents=False)
        assert result == ExitCode(1)

    def test_overwrites_destination_when_overwrite_true(self) -> None:
        """Should overwrite existing destination when overwrite=True."""
        templates_dir: Path
        templates_content: bytes

        templates_dir, templates_content = self._setup_templates_dir()
        dest: Path = self.tempdir.joinpath("output.py")
        test_utils.create_file(dest, empty=False)

        result: ExitCode = mkfile._create_template("script.py", (dest,), templates_dir, overwrite=True, parents=False)
        assert result == ExitCode(0)
        assert dest.read_bytes() == templates_content
