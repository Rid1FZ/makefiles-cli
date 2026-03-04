from pathlib import Path

import makefiles.utils as utils
import tests.utils as test_utils


class TestIsLinkF:
    def test_returns_true_for_symlink_to_file(self, tempdir: Path) -> None:
        """islinkf() should return True for a symlink pointing to a regular file."""
        target: Path = tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(target)

        link: Path = tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_symlink(link, target)

        assert utils.islinkf(link) is True

    def test_returns_false_for_symlink_to_directory(self, tempdir: Path) -> None:
        """islinkf() should return False for a symlink pointing to a directory."""
        real_dir: Path = tempdir.joinpath(test_utils.get_random_name())
        real_dir.mkdir()

        link: Path = tempdir.joinpath(test_utils.get_random_name())
        link.symlink_to(real_dir, target_is_directory=True)

        assert utils.islinkf(link) is False

    def test_returns_false_for_regular_file(self, tempdir: Path) -> None:
        """islinkf() should return False for a plain file (not a symlink)."""
        path: Path = tempdir.joinpath(test_utils.get_random_name())
        test_utils.create_file(path)

        assert utils.islinkf(path) is False

    def test_returns_false_for_broken_symlink(self, tempdir: Path) -> None:
        """islinkf() should return False for a broken symlink."""
        missing: Path = tempdir.joinpath(test_utils.get_random_name())
        link: Path = tempdir.joinpath(test_utils.get_random_name())
        link.symlink_to(missing)

        assert utils.islinkf(link) is False
