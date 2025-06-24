import pathlib
import random

import pytest

import makefiles.exceptions as exceptions
import tests.utils as utils
from makefiles.types import ExitCode
from makefiles.utils.fileutils import copy_file


class TestCopy(utils.MakefilesTestBase):
    @pytest.fixture
    def filepath(self) -> pathlib.Path:
        """Creates a temporary regular file for testing."""
        path = self.tempdir.joinpath(utils.get_random_name())

        utils.create_file(path)

        return path

    @pytest.fixture
    def symlink_to_file(self, filepath: pathlib.Path) -> pathlib.Path:
        """Creates a symlink to a regular file."""
        link = self.tempdir.joinpath(utils.get_random_name())

        utils.create_symlink(link, filepath)

        return link

    def test_copy_single_file(self, filepath: pathlib.Path) -> None:
        """Copies a regular file to a single destination."""
        dest = self.tempdir.joinpath(utils.get_random_name())

        assert copy_file(filepath, (dest,)) == ExitCode(0)
        assert utils.compare_files(filepath, dest)

    def test_copy_multiple_files(self, filepath: pathlib.Path) -> None:
        """Copies a file to multiple destinations."""
        destinations = tuple(self.tempdir.joinpath(utils.get_random_name()) for _ in range(random.randint(5, 10)))

        result = copy_file(filepath, destinations)
        assert result == ExitCode(0)
        for dest in destinations:
            assert utils.compare_files(filepath, dest)

    def test_copy_with_no_destination(self, filepath: pathlib.Path) -> None:
        """Raises ValueError when no destination is given."""
        with pytest.raises(ValueError, match="at least 1 destination expected"):
            copy_file(filepath)

    def test_copy_symlink_source(self, symlink_to_file: pathlib.Path, filepath: pathlib.Path) -> None:
        """Copies a symlink to a file, content should match the target."""
        dest = self.tempdir.joinpath(utils.get_random_name())

        assert copy_file(symlink_to_file, (dest,)) == ExitCode(0)
        assert utils.compare_files(filepath, dest)

    def test_copy_nonexistent_source_raises(self) -> None:
        """Raises SourceNotFoundError if source does not exist."""
        missing = self.tempdir.joinpath(utils.get_random_name())
        dest = self.tempdir.joinpath(utils.get_random_name())

        with pytest.raises(exceptions.SourceNotFoundError):
            copy_file(missing, (dest,))

    def test_copy_non_file_source_raises(self) -> None:
        """Raises InvalidSourceError if source is a directory."""
        dir_path = self.tempdir.joinpath(utils.get_random_name())
        dest = self.tempdir.joinpath(utils.get_random_name())

        dir_path.mkdir()

        with pytest.raises(exceptions.InvalidSourceError):
            copy_file(dir_path, (dest,))

    def test_copy_broken_symlink_raises(self) -> None:
        """Raises SourceNotFoundError for a broken symlink."""
        broken_target = self.tempdir.joinpath("nonexistent")
        broken_symlink = self.tempdir.joinpath(utils.get_random_name())
        dest = self.tempdir.joinpath(utils.get_random_name())

        broken_symlink.symlink_to(broken_target)

        with pytest.raises(exceptions.InvalidSourceError):
            copy_file(broken_symlink, (dest,))

    def test_copy_over_existing_dest(self, filepath: pathlib.Path) -> None:
        """Handles overwriting and not overwriting an existing destination."""
        dest = self.tempdir.joinpath(utils.get_random_name())

        utils.create_file(dest)

        # Without overwrite
        result = copy_file(filepath, (dest,), overwrite=False)
        assert result == ExitCode(1)
        assert not utils.compare_files(filepath, dest)

        # With overwrite
        result = copy_file(filepath, (dest,), overwrite=True)
        assert result == ExitCode(0)
        assert utils.compare_files(filepath, dest)

    def test_copy_to_nested_path_without_parents(self, filepath: pathlib.Path) -> None:
        """Fails when parent dir doesn't exist and parents=False, succeeds with parents=True."""
        nested = self.tempdir.joinpath(utils.get_random_name()).joinpath(utils.get_random_name())

        # Without creating parents
        result = copy_file(filepath, (nested,), parents=False)
        assert result == ExitCode(1)
        assert not nested.exists()

        # With parent creation
        result = copy_file(filepath, (nested,), parents=True)
        assert result == ExitCode(0)
        assert utils.compare_files(filepath, nested)

    def test_copy_to_multiple_existing_dests(self, filepath: pathlib.Path) -> None:
        """Fails if all destinations exist and overwrite=False."""
        dests = tuple(self.tempdir.joinpath(utils.get_random_name()) for _ in range(3))

        for d in dests:
            utils.create_file(d)

        result = copy_file(filepath, dests, overwrite=False)
        assert result == ExitCode(1)

    def test_copy_to_partial_existing_dests(self, filepath: pathlib.Path) -> None:
        """Partial overwrite failure with mixed destination state."""
        existing = self.tempdir.joinpath(utils.get_random_name())
        new = self.tempdir.joinpath(utils.get_random_name())

        utils.create_file(existing)

        result = copy_file(filepath, (existing, new), overwrite=False)
        assert result == ExitCode(1)
        assert not utils.compare_files(filepath, existing)
        assert utils.compare_files(filepath, new)

    def test_copy_symlink_to_directory_raises(self) -> None:
        """Raises InvalidSourceError for symlink to directory."""
        dir_path = self.tempdir.joinpath(utils.get_random_name())
        link = self.tempdir.joinpath(utils.get_random_name())
        dest = self.tempdir.joinpath(utils.get_random_name())

        dir_path.mkdir()
        link.symlink_to(dir_path)

        with pytest.raises(exceptions.InvalidSourceError):
            copy_file(link, (dest,))

    def test_dest_parent_is_file(self, filepath: pathlib.Path) -> None:
        """Fails when parent of dest is a file, not a directory."""
        parent_file = self.tempdir.joinpath(utils.get_random_name())
        dest = parent_file.joinpath("child.txt")

        utils.create_file(parent_file, empty=True)

        result = copy_file(filepath, (dest,), parents=False)
        assert result == ExitCode(1)

        with pytest.raises(OSError):
            copy_file(filepath, (dest,), parents=True)
