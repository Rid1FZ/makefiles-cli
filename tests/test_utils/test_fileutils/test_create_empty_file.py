import pathlib
import random

import pytest

import tests.utils as utils
from makefiles.types import ExitCode
from makefiles.utils.fileutils import create_empty_files


def _is_file(path: pathlib.Path) -> bool:
    return path.is_file() and not path.is_symlink()


class TestCreateEmptyFile(utils.MakefilesTestBase):
    def test_one_file(self) -> None:
        filepath: pathlib.Path = self.tempdir.joinpath(utils.get_random_name())

        assert create_empty_files(filepath) == ExitCode(0)
        assert _is_file(filepath)

    def test_multiple_files(self) -> None:
        filepaths: list[pathlib.Path] = [
            self.tempdir.joinpath(utils.get_random_name()) for _ in range(1, random.randint(5, 20))
        ]

        assert create_empty_files(*filepaths) == ExitCode(0)
        assert all(_is_file(filepath) for filepath in filepaths)

    def test_no_destination(self) -> None:
        with pytest.raises(ValueError):
            create_empty_files()

    def test_existing_file(self) -> None:
        filepath: pathlib.Path = self.tempdir.joinpath(utils.get_random_name())

        utils.create_file(filepath)

        assert create_empty_files(filepath, overwrite=False) == ExitCode(1)
        assert create_empty_files(filepath, overwrite=True) == ExitCode(0)
        assert _is_file(filepath)

    def test_non_existing_body(self) -> None:
        filepath: pathlib.Path = self.tempdir.joinpath(f"{utils.get_random_name()}/{utils.get_random_name()}")

        assert create_empty_files(filepath, parents=False) == ExitCode(1)
        assert create_empty_files(filepath, parents=True) == ExitCode(0)
        assert _is_file(filepath)
