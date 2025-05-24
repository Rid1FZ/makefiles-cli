import pathlib
import random

import pytest

import makefiles.exceptions as exceptions
import tests.utils as utils
from makefiles.utils.fileutils import create_empty_files


def _is_file(path: pathlib.Path) -> bool:
    return path.is_file() and not path.is_symlink()


class TestCreateEmptyFile(utils.TestMKFile):
    def test_one_file(self) -> None:
        filepath: pathlib.Path = self.tempdir.joinpath("file")

        create_empty_files(filepath)

        assert _is_file(filepath)

    def test_multiple_files(self) -> None:
        filepaths: list[pathlib.Path] = [
            self.tempdir.joinpath("file" + str(count)) for count in range(1, random.randint(5, 20))
        ]

        create_empty_files(*filepaths)

        assert all(_is_file(filepath) for filepath in filepaths)

    def test_existing_file(self) -> None:
        filepath: pathlib.Path = self.tempdir.joinpath("file")

        utils.create_file(filepath)

        with pytest.raises(exceptions.DestinationExistsError):
            create_empty_files(filepath)
