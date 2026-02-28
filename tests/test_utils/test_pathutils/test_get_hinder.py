from pathlib import Path

import makefiles.utils as utils
import tests.utils as test_utils


class TestGetHinder(test_utils.MakefilesTestBase):
    def test_returns_none_for_existing_directory(self) -> None:
        """get_hinder() should return None when the path is a valid directory."""
        assert utils.get_hinder(self.tempdir) is None

    def test_returns_none_for_symlink_to_dir(self) -> None:
        """get_hinder() should return None for a symlink pointing to a directory."""
        real_dir: Path = self.tempdir.joinpath(test_utils.get_random_name())
        real_dir.mkdir()

        link: Path = self.tempdir.joinpath(test_utils.get_random_name())
        link.symlink_to(real_dir, target_is_directory=True)

        assert utils.get_hinder(link) is None

    def test_returns_path_for_broken_symlink(self) -> None:
        """get_hinder() should return the path string for a broken symlink."""
        missing: Path = self.tempdir.joinpath(test_utils.get_random_name())
        link: Path = self.tempdir.joinpath(test_utils.get_random_name())
        link.symlink_to(missing)

        result: str | None = utils.get_hinder(link)
        assert result == str(link)

    def test_returns_path_for_regular_file(self) -> None:
        """get_hinder() should return the file path when the path is a file, not a dir."""
        path: Path = self.tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(path)

        result: str | None = utils.get_hinder(path)
        assert result == str(path)

    def test_returns_parent_path_when_parent_is_file(self) -> None:
        """get_hinder() should walk up and find the file blocking the parent."""
        blocking_file: Path = self.tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(blocking_file)

        nested: Path = blocking_file.joinpath("child")

        result: str | None = utils.get_hinder(nested)
        assert result == str(blocking_file)

    def test_returns_none_for_nonexistent_path_with_valid_parents(self) -> None:
        """get_hinder() should return None if all existing ancestors are valid dirs."""
        nonexistent: Path = self.tempdir.joinpath(test_utils.get_random_name()).joinpath(test_utils.get_random_name())

        result = utils.get_hinder(nonexistent)
        assert result is None
