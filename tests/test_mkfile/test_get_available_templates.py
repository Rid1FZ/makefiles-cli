from pathlib import Path

import pytest

import makefiles.exceptions as exceptions
import makefiles.mkfile as mkfile
import tests.utils as test_utils


class TestGetAvailableTemplates(test_utils.MakefilesTestBase):
    def test_returns_list_of_templates(self) -> None:
        """Should return relative file paths from a non-empty template directory."""
        test_utils.create_file(self.tempdir.joinpath("mytemplate.py"))
        test_utils.create_file(self.tempdir.joinpath("shell.sh"))

        result: list[str] = mkfile._get_available_templates(self.tempdir)
        assert set(result) == {"mytemplate.py", "shell.sh"}

    def test_raises_when_dir_is_empty(self) -> None:
        """Should raise NoTemplatesAvailableError when template dir has no files."""
        with pytest.raises(exceptions.NoTemplatesAvailableError):
            mkfile._get_available_templates(self.tempdir)

    def test_raises_when_dir_does_not_exist(self) -> None:
        """Should raise NoTemplatesAvailableError when template dir doesn't exist."""
        nonexistent: Path = self.tempdir.joinpath("no_such_dir")

        with pytest.raises(exceptions.NoTemplatesAvailableError):
            mkfile._get_available_templates(nonexistent)

    def test_raises_when_path_is_a_file(self) -> None:
        """Should raise NoTemplatesAvailableError when given a file path, not a dir."""
        file_path: Path = self.tempdir.joinpath("file.txt")
        test_utils.create_file(file_path)

        with pytest.raises(exceptions.NoTemplatesAvailableError):
            mkfile._get_available_templates(file_path)
