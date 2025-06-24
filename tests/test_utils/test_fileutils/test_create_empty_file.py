import pathlib
import random

import pytest

import tests.utils as utils
from makefiles.types import ExitCode
from makefiles.utils.fileutils import create_empty_files


def _is_file(path: pathlib.Path) -> bool:
    return path.is_file() and not path.is_symlink()


class TestCreateEmptyFile(utils.MakefilesTestBase):
    def test_create_one_file(self) -> None:
        """Create a single empty file."""
        path = self.tempdir.joinpath(utils.get_random_name())

        assert create_empty_files((path,)) == ExitCode(0)
        assert _is_file(path)

    def test_create_multiple_files(self) -> None:
        """Create multiple empty files at once."""
        paths = tuple(self.tempdir.joinpath(utils.get_random_name()) for _ in range(random.randint(3, 8)))

        assert create_empty_files(paths) == ExitCode(0)
        assert all(_is_file(p) for p in paths)

    def test_no_path_given_raises(self) -> None:
        """Should raise ValueError when no path is given."""
        with pytest.raises(ValueError, match="at least on path expected"):
            create_empty_files()

    def test_file_already_exists(self) -> None:
        """Should fail when file exists and overwrite=False; succeed with overwrite=True."""
        path = self.tempdir.joinpath(utils.get_random_name())

        utils.create_file(path)

        assert create_empty_files((path,), overwrite=False) == ExitCode(1)
        assert create_empty_files((path,), overwrite=True) == ExitCode(0)
        assert _is_file(path)

    def test_parent_does_not_exist(self) -> None:
        """Fails if parent directory doesn't exist and parents=False; succeeds with parents=True."""
        nested_path = self.tempdir.joinpath(utils.get_random_name()).joinpath(utils.get_random_name())

        assert create_empty_files((nested_path,), parents=False) == ExitCode(1)
        assert not nested_path.exists()

        assert create_empty_files((nested_path,), parents=True) == ExitCode(0)
        assert _is_file(nested_path)

    def test_existing_directory_path(self) -> None:
        """Overwrites a directory if overwrite=True."""
        dir_path = self.tempdir.joinpath(utils.get_random_name())

        dir_path.mkdir()

        # overwrite=False should fail
        assert create_empty_files((dir_path,), overwrite=False) == ExitCode(1)
        assert dir_path.is_dir()

        # overwrite=True should succeed and replace dir with file
        assert create_empty_files((dir_path,), overwrite=True) == ExitCode(0)
        assert _is_file(dir_path)

    def test_existing_symlink_path(self) -> None:
        """Overwrites a symlink if overwrite=True."""
        target_file = self.tempdir.joinpath(utils.get_random_name())
        symlink = self.tempdir.joinpath(utils.get_random_name())

        utils.create_file(target_file)
        symlink.symlink_to(target_file)

        assert create_empty_files((symlink,), overwrite=False) == ExitCode(1)
        assert symlink.is_symlink()

        assert create_empty_files((symlink,), overwrite=True) == ExitCode(0)
        assert _is_file(symlink)

    def test_dest_parent_is_file(self) -> None:
        """Fails when parent of target path is a file, not a directory."""
        parent = self.tempdir.joinpath(utils.get_random_name())
        dest = parent.joinpath("child.txt")

        utils.create_file(parent, empty=True)

        result = create_empty_files((dest,), parents=False)
        assert result == ExitCode(1)

        with pytest.raises(OSError):
            create_empty_files((dest,), parents=True)

    def test_partial_success_multiple_paths(self) -> None:
        """If some paths exist and overwrite=False, should succeed on others and return ExitCode 1."""
        existing = self.tempdir.joinpath(utils.get_random_name())
        new = self.tempdir.joinpath(utils.get_random_name())

        utils.create_file(existing)

        result = create_empty_files((existing, new), overwrite=False)
        assert result == ExitCode(1)
        assert _is_file(new)
        assert existing.exists()

    def test_nested_and_flat_paths_mix(self) -> None:
        """Test creation of both nested and flat paths."""
        flat = self.tempdir.joinpath(utils.get_random_name())
        nested = self.tempdir.joinpath(utils.get_random_name()).joinpath(utils.get_random_name())

        result = create_empty_files((flat, nested), parents=True)
        assert result == ExitCode(0)
        assert _is_file(flat)
        assert _is_file(nested)
