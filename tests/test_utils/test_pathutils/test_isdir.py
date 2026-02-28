from pathlib import Path

import makefiles.utils as utils
import tests.utils as test_utils


class TestIsDir(test_utils.MakefilesTestBase):
    def test_returns_true_for_plain_directory(self) -> None:
        """isdir() should return True for a plain directory."""
        path: Path = self.tempdir.joinpath(test_utils.get_random_name())
        path.mkdir()

        assert utils.isdir(path) is True

    def test_returns_false_for_symlink_to_dir(self) -> None:
        """isdir() should return False for a symlink to a directory."""
        real_dir: Path = self.tempdir.joinpath(test_utils.get_random_name())
        real_dir.mkdir()

        link: Path = self.tempdir.joinpath(test_utils.get_random_name())
        link.symlink_to(real_dir, target_is_directory=True)

        assert utils.isdir(link) is False

    def test_returns_false_for_regular_file(self) -> None:
        """isdir() should return False for a regular file."""
        path: Path = self.tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(path)

        assert utils.isdir(path) is False

    def test_returns_false_for_nonexistent_path(self) -> None:
        """isdir() should return False for a missing path."""
        path: Path = self.tempdir.joinpath(test_utils.get_random_name())

        assert utils.isdir(path) is False
