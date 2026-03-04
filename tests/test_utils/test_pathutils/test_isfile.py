from pathlib import Path

import makefiles.utils as utils
import tests.utils as test_utils


class TestIsFile:
    def test_returns_true_for_regular_file(self, tempdir: Path) -> None:
        """isfile() should return True for a plain file."""
        path: Path = tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(path)

        assert utils.isfile(path) is True

    def test_returns_false_for_symlink_to_file(self, tempdir: Path) -> None:
        """isfile() should return False for a symlink even if it points to a file."""
        target: Path = tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(target)

        link: Path = tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_symlink(link, target)

        assert utils.isfile(link) is False

    def test_returns_false_for_directory(self, tempdir: Path) -> None:
        """isfile() should return False for a directory."""
        path: Path = tempdir.joinpath(test_utils.get_random_name())
        path.mkdir()

        assert utils.isfile(path) is False

    def test_returns_false_for_nonexistent_path(self, tempdir: Path) -> None:
        """isfile() should return False for a missing path."""
        path: Path = tempdir.joinpath(test_utils.get_random_name())

        assert utils.isfile(path) is False
