import pathlib
import random

import pytest

import makefiles.exceptions as exceptions
import makefiles.utils.dirwalker as dirwalker
import tests.utils as utils
from tests.utils.setup_test import TestMKFile


class TestDirWalker(TestMKFile):
    @pytest.fixture
    def filetree(self) -> list[str]:
        return utils.generate_tree(
            self.tempdir,
            max_depth=random.randint(1, 10),
            max_children=random.randint(1, 10),
            max_files=random.randint(1, 10),
            hidden=False,
        )

    def test_filetree(self, filetree: list[str]) -> None:
        assert set(dirwalker.listf(self.tempdir)) == set(filetree)

    def test_invalid_path(self) -> None:
        with pytest.raises(exceptions.InvalidPathError):
            dirwalker.listf(self.tempdir.joinpath(utils.get_random_str(32, special_chars=False)))
