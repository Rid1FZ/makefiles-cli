from pathlib import Path

import makefiles.utils as utils
import tests.utils as test_utils


class TestIsLink(test_utils.MakefilesTestBase):
    def test_returns_true_for_valid_symlink_to_file(self) -> None:
        """islink() should return True for a symlink pointing to an existing file."""
        target: Path = self.tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(target)

        link: Path = self.tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_symlink(link, target)

        assert utils.islink(link) is True

    def test_returns_false_for_broken_symlink(self) -> None:
        """islink() should return False for a broken symlink."""
        missing: Path = self.tempdir.joinpath(test_utils.get_random_name())
        link: Path = self.tempdir.joinpath(test_utils.get_random_name())
        link.symlink_to(missing)

        assert utils.islink(link) is False

    def test_returns_false_for_regular_file(self) -> None:
        """islink() should return False for a plain file."""
        path: Path = self.tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(path)

        assert utils.islink(path) is False

    def test_returns_false_for_nonexistent_path(self) -> None:
        """islink() should return False when path does not exist."""
        path: Path = self.tempdir.joinpath(test_utils.get_random_name())

        assert utils.islink(path) is False
