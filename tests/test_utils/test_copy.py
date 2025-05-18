import pathlib
import random

import pytest

import makefiles.exceptions as exceptions
import makefiles.utils.copy as copy
import tests.utils as utils


class TestCopy(utils.TestMKFile):
    @pytest.fixture
    def filepath(self) -> pathlib.Path:
        path: pathlib.Path = self.tempdir.joinpath("file")
        utils.create_file(path)
        return path

    def test_one_regular_file(self, filepath: pathlib.Path) -> None:
        copypath: pathlib.Path = self.tempdir.joinpath("copy")

        copy.copy(filepath, copypath)

        assert utils.compare_files(filepath, copypath)

    def test_multiple_regular_files(self, filepath: pathlib.Path) -> None:
        copypaths: list[pathlib.Path] = [
            self.tempdir.joinpath("copy" + str(count)) for count in range(1, random.randint(5, 20))
        ]

        for cpath in copypaths:
            copy.copy(filepath, cpath)

        assert all(utils.compare_files(filepath, cpath) for cpath in copypaths)

    def test_symlink(self, filepath: pathlib.Path) -> None:
        linkpath: pathlib.Path = self.tempdir.joinpath("symlink")
        copypath: pathlib.Path = self.tempdir.joinpath("copy")

        utils.create_symlink(linkpath, filepath)

        copy.copy(linkpath, copypath)

        assert utils.compare_files(filepath, copypath)

    def test_nofile(self) -> None:
        filepath: pathlib.Path = self.tempdir.joinpath("file")
        copypath: pathlib.Path = self.tempdir.joinpath("copy")

        with pytest.raises(exceptions.SourceNotFoundError):
            copy.copy(filepath, copypath)

    def test_non_file(self) -> None:
        dirpath: pathlib.Path = self.tempdir.joinpath("directory")
        copypath: pathlib.Path = self.tempdir.joinpath("copy")

        dirpath.mkdir(parents=True, exist_ok=False)

        with pytest.raises(exceptions.InvalidSourceError):
            copy.copy(dirpath, copypath)

    def test_existing_file(self, filepath: pathlib.Path) -> None:
        copypath: pathlib.Path = self.tempdir.joinpath("copy")

        utils.create_file(copypath)

        with pytest.raises(exceptions.DestinationExistsError):
            copy.copy(filepath, copypath)
