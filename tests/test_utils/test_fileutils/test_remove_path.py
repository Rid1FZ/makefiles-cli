from pathlib import Path

import tests.utils as utils
from makefiles.utils.fileutils import remove_path


class TestRemovePath(utils.MakefilesTestBase):
    def test_removes_regular_file(self):
        """Should remove a regular file if it exists."""
        path: Path = self.tempdir.joinpath(utils.get_random_name())

        utils.create_file(path)
        assert path.exists()

        remove_path(path)
        assert not path.exists()

    def test_removes_symlink_to_file(self):
        """Should remove a symlink pointing to a file without deleting the target."""
        target: Path = self.tempdir.joinpath(utils.get_random_name())
        link: Path = self.tempdir.joinpath(utils.get_random_name())

        utils.create_file(target)
        utils.create_symlink(link, target)
        assert link.is_symlink()

        remove_path(link)
        assert not link.exists()
        assert target.exists()

    def test_removes_broken_symlink(self):
        """Should remove a broken symlink."""
        target: Path = self.tempdir.joinpath(utils.get_random_name())
        link: Path = self.tempdir.joinpath(utils.get_random_name())

        link.symlink_to(target)
        assert link.is_symlink()

        remove_path(link)
        assert not link.exists()

    def test_removes_directory(self):
        """Should recursively remove a directory and its contents."""
        dirpath: Path = self.tempdir.joinpath(utils.get_random_name())

        dirpath.mkdir()
        utils.create_file(dirpath.joinpath(utils.get_random_name()))
        assert dirpath.exists()

        remove_path(dirpath)
        assert not dirpath.exists()

    def test_handles_nonexistent_path(self):
        """Should silently ignore if the path does not exist."""
        path: Path = self.tempdir.joinpath(utils.get_random_name())

        remove_path(path)
        assert not path.exists()
