import random
from pathlib import Path
from unittest import mock

import pytest

import makefiles.exceptions as exceptions
import makefiles.utils.cli_io as cli_io
import tests.utils as utils
from makefiles.types import ExitCode
from makefiles.utils.fileutils import copy_file


class TestCopy:
    @pytest.fixture
    def filepath(self, tempdir: Path) -> Path:
        """Creates a temporary regular file for testing."""
        path: Path = tempdir.joinpath(utils.get_random_name())

        utils.create_file(path)

        return path

    @pytest.fixture
    def symlink_to_file(self, tempdir: Path, filepath: Path) -> Path:
        """Creates a symlink to a regular file."""
        link: Path = tempdir.joinpath(utils.get_random_name())

        utils.create_symlink(link, filepath)

        return link

    def test_copy_single_file(self, tempdir: Path, filepath: Path) -> None:
        """Copies a regular file to a single destination."""
        dest: Path = tempdir.joinpath(utils.get_random_name())

        assert copy_file(filepath, (dest,)) == ExitCode(0)
        assert utils.compare_files(filepath, dest)

    def test_copy_multiple_files(self, tempdir: Path, filepath: Path) -> None:
        """Copies a file to multiple destinations."""
        destinations: tuple[Path, ...] = tuple(
            tempdir.joinpath(utils.get_random_name()) for _ in range(random.randint(5, 10))
        )

        result: ExitCode = copy_file(filepath, destinations)
        assert result == ExitCode(0)
        for dest in destinations:
            assert utils.compare_files(filepath, dest)

    def test_copy_with_no_destination(self, filepath: Path) -> None:
        """Raises ValueError when no destination is given."""
        with pytest.raises(ValueError, match="at least 1 destination expected"):
            copy_file(filepath)

    def test_copy_symlink_source(self, tempdir: Path, symlink_to_file: Path, filepath: Path) -> None:
        """Copies a symlink to a file, content should match the target."""
        dest: Path = tempdir.joinpath(utils.get_random_name())

        assert copy_file(symlink_to_file, (dest,)) == ExitCode(0)
        assert utils.compare_files(filepath, dest)

    def test_copy_nonexistent_source_raises(self, tempdir: Path) -> None:
        """Raises SourceNotFoundError if source does not exist."""
        missing: Path = tempdir.joinpath(utils.get_random_name())
        dest: Path = tempdir.joinpath(utils.get_random_name())

        with pytest.raises(exceptions.SourceNotFoundError):
            copy_file(missing, (dest,))

    def test_copy_non_file_source_raises(self, tempdir: Path) -> None:
        """Raises InvalidSourceError if source is a directory."""
        dir_path: Path = tempdir.joinpath(utils.get_random_name())
        dest: Path = tempdir.joinpath(utils.get_random_name())

        dir_path.mkdir()

        with pytest.raises(exceptions.InvalidSourceError):
            copy_file(dir_path, (dest,))

    def test_copy_broken_symlink_raises(self, tempdir: Path) -> None:
        """Raises SourceNotFoundError for a broken symlink."""
        broken_target: Path = tempdir.joinpath("nonexistent")
        broken_symlink: Path = tempdir.joinpath(utils.get_random_name())
        dest: Path = tempdir.joinpath(utils.get_random_name())

        broken_symlink.symlink_to(broken_target)

        with pytest.raises(exceptions.InvalidSourceError):
            copy_file(broken_symlink, (dest,))

    def test_copy_over_existing_dest(self, tempdir: Path, filepath: Path) -> None:
        """Handles overwriting and not overwriting an existing destination."""
        dest: Path = tempdir.joinpath(utils.get_random_name())

        utils.create_file(dest)

        # Without overwrite
        result = copy_file(filepath, (dest,), overwrite=False)
        assert result == ExitCode(1)
        assert not utils.compare_files(filepath, dest)

        # With overwrite
        result = copy_file(filepath, (dest,), overwrite=True)
        assert result == ExitCode(0)
        assert utils.compare_files(filepath, dest)

    def test_copy_to_nested_path_without_parents(self, tempdir: Path, filepath: Path) -> None:
        """Fails when parent dir doesn't exist and parents=False, succeeds with parents=True."""
        result: ExitCode
        nested: Path = tempdir.joinpath(utils.get_random_name(), utils.get_random_name())

        # Without creating parents
        result = copy_file(filepath, (nested,), parents=False)
        assert result == ExitCode(1)
        assert not nested.exists()

        # With parent creation
        result = copy_file(filepath, (nested,), parents=True)
        assert result == ExitCode(0)
        assert utils.compare_files(filepath, nested)

    def test_copy_to_multiple_existing_dests(self, tempdir: Path, filepath: Path) -> None:
        """Fails if all destinations exist and overwrite=False."""
        dests: tuple[Path, ...] = tuple(tempdir.joinpath(utils.get_random_name()) for _ in range(3))

        for d in dests:
            utils.create_file(d)

        result: ExitCode = copy_file(filepath, dests, overwrite=False)
        assert result == ExitCode(1)

    def test_copy_to_partial_existing_dests(self, tempdir: Path, filepath: Path) -> None:
        """Partial overwrite failure with mixed destination state."""
        existing: Path = tempdir.joinpath(utils.get_random_name())
        new: Path = tempdir.joinpath(utils.get_random_name())

        utils.create_file(existing)

        result: ExitCode = copy_file(filepath, (existing, new), overwrite=False)
        assert result == ExitCode(1)
        assert not utils.compare_files(filepath, existing)
        assert utils.compare_files(filepath, new)

    def test_copy_symlink_to_directory_raises(self, tempdir: Path) -> None:
        """Raises InvalidSourceError for symlink to directory."""
        dir_path: Path = tempdir.joinpath(utils.get_random_name())
        link: Path = tempdir.joinpath(utils.get_random_name())
        dest: Path = tempdir.joinpath(utils.get_random_name())

        dir_path.mkdir()
        link.symlink_to(dir_path)

        with pytest.raises(exceptions.InvalidSourceError):
            copy_file(link, (dest,))

    def test_dest_parent_is_file(self, tempdir: Path, filepath: Path) -> None:
        """Fails when parent of dest is a file, not a directory."""
        parent_file: Path = tempdir.joinpath(utils.get_random_name())
        dest: Path = parent_file.joinpath("child.txt")

        utils.create_file(parent_file, empty=True)

        result: ExitCode = copy_file(filepath, (dest,), parents=False)
        assert result == ExitCode(1)

        with pytest.raises(exceptions.InvalidPathError):
            copy_file(filepath, (dest,), parents=True)

    def test_verbose_prints_confirmation_on_copy(self, tempdir: Path, filepath: Path) -> None:
        """verbose=True should print a confirmation message after a successful copy."""
        dest: Path = tempdir.joinpath(utils.get_random_name())

        with mock.patch.object(cli_io, "print") as mock_print:
            result: ExitCode = copy_file(filepath, (dest,), verbose=True)

        assert result == ExitCode(0)
        assert dest.is_file()
        mock_print.assert_called_once()

        printed: str = mock_print.call_args[0][0]
        assert str(dest) in printed

    def test_dry_run_does_not_create_file(self, tempdir: Path, filepath: Path) -> None:
        """dry_run=True must not modify the filesystem."""
        dest: Path = tempdir.joinpath(utils.get_random_name())

        with mock.patch.object(cli_io, "print") as mock_print:
            result: ExitCode = copy_file(filepath, (dest,), dry_run=True)

        assert result == ExitCode(0)
        assert not dest.exists()
        mock_print.assert_called_once()

        printed: str = mock_print.call_args[0][0]
        assert "[dry-run]" in printed
        assert str(dest) in printed

    def test_dry_run_reports_existing_dest(self, tempdir: Path, filepath: Path) -> None:
        """dry_run should still warn when destination already exists and overwrite=False."""
        dest: Path = tempdir.joinpath(utils.get_random_name())
        utils.create_file(dest)

        with mock.patch.object(cli_io, "eprint") as mock_eprint:
            result: ExitCode = copy_file(filepath, (dest,), dry_run=True, overwrite=False)

        assert result == ExitCode(1)
        mock_eprint.assert_called()

    def test_verbose_false_does_not_print_on_copy(self, tempdir: Path, filepath: Path) -> None:
        """verbose=False (default) must not print any confirmation."""
        dest: Path = tempdir.joinpath(utils.get_random_name())

        with mock.patch.object(cli_io, "print") as mock_print:
            copy_file(filepath, (dest,), verbose=False)

        mock_print.assert_not_called()
