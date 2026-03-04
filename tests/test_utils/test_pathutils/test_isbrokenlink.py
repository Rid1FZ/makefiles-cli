from pathlib import Path

import makefiles.utils as utils
import tests.utils as test_utils


class TestIsBrokenLink:
    def test_returns_true_for_broken_symlink(self, tempdir: Path) -> None:
        """isbrokenlink() should return True for a symlink whose target is missing."""
        missing: Path = tempdir.joinpath(test_utils.get_random_name())
        link: Path = tempdir.joinpath(test_utils.get_random_name())
        link.symlink_to(missing)

        assert utils.isbrokenlink(link) is True

    def test_returns_false_for_valid_symlink(self, tempdir: Path) -> None:
        """isbrokenlink() should return False for a working symlink."""
        target: Path = tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(target)

        link: Path = tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_symlink(link, target)

        assert utils.isbrokenlink(link) is False

    def test_returns_false_for_regular_file(self, tempdir: Path) -> None:
        """isbrokenlink() should return False for a plain file (not a symlink)."""
        path: Path = tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(path)

        assert utils.isbrokenlink(path) is False

    def test_returns_false_for_nonexistent_path(self, tempdir: Path) -> None:
        """isbrokenlink() should return False for a missing path (not a symlink at all)."""
        path: Path = tempdir.joinpath(test_utils.get_random_name())

        assert utils.isbrokenlink(path) is False
