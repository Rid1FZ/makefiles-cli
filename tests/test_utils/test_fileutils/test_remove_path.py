import tests.utils as utils
from makefiles.utils.fileutils import remove_path


class TestRemovePath(utils.MakefilesTestBase):
    def test_removes_regular_file(self):
        path = self.tempdir.joinpath(utils.get_random_name())

        utils.create_file(path)
        assert path.exists()

        remove_path(path)
        assert not path.exists()

    def test_removes_symlink_to_file(self):
        target = self.tempdir.joinpath(utils.get_random_name())
        link = self.tempdir.joinpath(utils.get_random_name())

        utils.create_file(target)
        utils.create_symlink(link, target)
        assert link.is_symlink()

        remove_path(link)
        assert not link.exists()
        assert target.exists()

    def test_removes_broken_symlink(self):
        target = self.tempdir.joinpath(utils.get_random_name())
        link = self.tempdir.joinpath(utils.get_random_name())

        link.symlink_to(target)
        assert link.is_symlink()

        remove_path(link)
        assert not link.exists()

    def test_removes_directory(self):
        dirpath = self.tempdir.joinpath(utils.get_random_name())

        dirpath.mkdir()
        utils.create_file(dirpath.joinpath(utils.get_random_name()))
        assert dirpath.exists()

        remove_path(dirpath)
        assert not dirpath.exists()

    def test_handles_nonexistent_path(self):
        path = self.tempdir.joinpath(utils.get_random_name())

        remove_path(path)
        assert not path.exists()
