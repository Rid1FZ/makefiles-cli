from pathlib import Path

import makefiles.utils as utils
import tests.utils as test_utils


class TestExists(test_utils.MakefilesTestBase):
    def test_returns_true_for_regular_file(self) -> None:
        """exists() should return True for a regular file."""
        path: Path = self.tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(path)

        assert utils.exists(path) is True

    def test_returns_true_for_directory(self) -> None:
        """exists() should return True for a directory."""
        path: Path = self.tempdir.joinpath(test_utils.get_random_name())
        path.mkdir()

        assert utils.exists(path) is True

    def test_returns_true_for_valid_symlink(self) -> None:
        """exists() should return True for a valid symlink."""
        target: Path = self.tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(target)

        link: Path = self.tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_symlink(link, target)

        assert utils.exists(link) is True

    def test_returns_true_for_broken_symlink(self) -> None:
        """exists() should return True even for a broken symlink (is_symlink() is True)."""
        missing_target: Path = self.tempdir.joinpath(test_utils.get_random_name())
        link: Path = self.tempdir.joinpath(test_utils.get_random_name())
        link.symlink_to(missing_target)

        assert utils.exists(link) is True

    def test_returns_false_for_nonexistent_path(self) -> None:
        """exists() should return False for a path that does not exist."""
        path: Path = self.tempdir.joinpath(test_utils.get_random_name())

        assert utils.exists(path) is False
