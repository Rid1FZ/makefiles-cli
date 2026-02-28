from pathlib import Path

import makefiles.utils as utils
import tests.utils as test_utils


class TestIsLinkD(test_utils.MakefilesTestBase):
    def test_returns_true_for_symlink_to_directory(self) -> None:
        """islinkd() should return True for a symlink pointing to a directory."""
        real_dir: Path = self.tempdir.joinpath(test_utils.get_random_name())
        real_dir.mkdir()

        link: Path = self.tempdir.joinpath(test_utils.get_random_name())
        link.symlink_to(real_dir, target_is_directory=True)

        assert utils.islinkd(link) is True

    def test_returns_false_for_symlink_to_file(self) -> None:
        """islinkd() should return False for a symlink pointing to a file."""
        target: Path = self.tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(target)

        link: Path = self.tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_symlink(link, target)

        assert utils.islinkd(link) is False

    def test_returns_false_for_regular_directory(self) -> None:
        """islinkd() should return False for a plain directory (not a symlink)."""
        path: Path = self.tempdir.joinpath(test_utils.get_random_name())
        path.mkdir()

        assert utils.islinkd(path) is False

    def test_returns_false_for_broken_symlink(self) -> None:
        """islinkd() should return False for a broken symlink."""
        missing: Path = self.tempdir.joinpath(test_utils.get_random_name())
        link: Path = self.tempdir.joinpath(test_utils.get_random_name())
        link.symlink_to(missing)

        assert utils.islinkd(link) is False
