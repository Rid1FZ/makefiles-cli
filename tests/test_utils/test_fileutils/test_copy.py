import pathlib
import random

import pytest

import makefiles.exceptions as exceptions
import tests.utils as utils
from makefiles.types import ExitCode
from makefiles.utils.fileutils import copy


class TestCopy(utils.TestMKFile):
    @pytest.fixture
    def filepath(self) -> pathlib.Path:
        path: pathlib.Path = self.tempdir.joinpath("file")
        utils.create_file(path)
        return path

    def test_one_regular_file(self, filepath: pathlib.Path) -> None:
        copypath: pathlib.Path = self.tempdir.joinpath("copy")

        assert copy(filepath, copypath) == ExitCode(0)
        assert utils.compare_files(filepath, copypath)

    def test_multiple_regular_files(self, filepath: pathlib.Path) -> None:
        copypaths: list[pathlib.Path] = [
            self.tempdir.joinpath("copy" + str(count)) for count in range(1, random.randint(5, 20))
        ]

        for cpath in copypaths:
            assert copy(filepath, cpath) == ExitCode(0)

        assert all(utils.compare_files(filepath, cpath) for cpath in copypaths)

    def test_symlink(self, filepath: pathlib.Path) -> None:
        linkpath: pathlib.Path = self.tempdir.joinpath("symlink")
        copypath: pathlib.Path = self.tempdir.joinpath("copy")

        utils.create_symlink(linkpath, filepath)

        assert copy(linkpath, copypath) == ExitCode(0)
        assert utils.compare_files(filepath, copypath)

    def test_nofile(self) -> None:
        filepath: pathlib.Path = self.tempdir.joinpath("file")
        copypath: pathlib.Path = self.tempdir.joinpath("copy")

        with pytest.raises(exceptions.SourceNotFoundError):
            copy(filepath, copypath)

    def test_non_file(self) -> None:
        dirpath: pathlib.Path = self.tempdir.joinpath("directory")
        copypath: pathlib.Path = self.tempdir.joinpath("copy")

        dirpath.mkdir(parents=True, exist_ok=False)

        with pytest.raises(exceptions.InvalidSourceError):
            copy(dirpath, copypath)

    def test_existing_file(self, filepath: pathlib.Path) -> None:
        copypath: pathlib.Path = self.tempdir.joinpath("copy")

        utils.create_file(copypath)

        assert copy(filepath, copypath) == ExitCode(1)

    def test_non_existing_body(self, filepath: pathlib.Path) -> None:
        copypath: pathlib.Path = self.tempdir.joinpath("random/body/copy")

        assert copy(filepath, copypath, parents=False) == ExitCode(1)
        assert copy(filepath, copypath, parents=True) == ExitCode(0)
        assert utils.compare_files(filepath, copypath)
