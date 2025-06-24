import random

import pytest

import makefiles.exceptions as exceptions
import makefiles.utils.dirwalker as dirwalker
import tests.utils as utils


class TestDirWalker(utils.MakefilesTestBase):
    @pytest.fixture
    def filetree(self) -> list[str]:
        """Generates a random file tree and returns relative paths of files created."""
        return utils.generate_tree(
            self.tempdir,
            max_depth=random.randint(1, 5),
            max_children=random.randint(1, 5),
            max_files=random.randint(1, 5),
            hidden=False,
        )

    def test_filetree_returns_all_files(self, filetree: list[str]) -> None:
        """Should return all non-hidden files in the file tree."""
        assert set(dirwalker.listf(self.tempdir)) == set(filetree)

    def test_invalid_path_raises(self) -> None:
        """Should raise InvalidPathError if input is not a dir or symlink to dir."""
        invalid_path = self.tempdir.joinpath(utils.get_random_name())

        with pytest.raises(exceptions.InvalidPathError):
            dirwalker.listf(invalid_path)

    def test_hidden_files_are_ignored(self) -> None:
        """Hidden files should not appear in the output."""
        hidden_file = self.tempdir.joinpath(f".{utils.get_random_name()}")

        utils.create_file(hidden_file)

        assert dirwalker.listf(self.tempdir) == []

    def test_hidden_dirs_are_ignored(self) -> None:
        """Hidden directories and their contents should be skipped."""
        hidden_dir = self.tempdir.joinpath(f".{utils.get_random_name()}")
        file_inside = hidden_dir.joinpath(utils.get_random_name())

        hidden_dir.mkdir(parents=True)
        utils.create_file(file_inside)

        assert dirwalker.listf(self.tempdir) == []

    def test_symlink_to_dir(self) -> None:
        """Should list files under a symlinked directory."""
        real_dir = self.tempdir.joinpath(utils.get_random_name())
        link_dir = self.tempdir.joinpath(utils.get_random_name())
        file_inside = real_dir.joinpath("f.txt")

        real_dir.mkdir()
        utils.create_file(file_inside)
        link_dir.symlink_to(real_dir, target_is_directory=True)

        assert dirwalker.listf(link_dir) == ["f.txt"]

    def test_symlink_inside_tree_included(self) -> None:
        """If a file symlink exists in tree, it should be included as a file."""
        target = self.tempdir.joinpath("original.txt")
        link = self.tempdir.joinpath("linked.txt")

        utils.create_file(target)
        link.symlink_to(target)

        assert sorted(dirwalker.listf(self.tempdir)) == ["linked.txt", "original.txt"]

    def test_empty_directory_returns_empty_list(self) -> None:
        """Empty directories should return an empty list."""
        assert dirwalker.listf(self.tempdir) == []

    def test_dot_files_not_in_subdirs(self) -> None:
        """Hidden files in subdirectories should be ignored."""
        subdir = self.tempdir.joinpath("sub")
        subdir.mkdir()

        visible_file = subdir.joinpath("x.txt")
        hidden_file = subdir.joinpath(".x.txt")

        utils.create_file(visible_file)
        utils.create_file(hidden_file)

        assert dirwalker.listf(self.tempdir) == ["sub/x.txt"]
