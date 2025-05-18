import os
import pathlib
import shutil

import makefiles.exceptions as exceptions


class TestMKFile:
    @property
    def project_root(self) -> pathlib.Path:
        path: pathlib.Path = pathlib.Path(__file__).absolute().parent
        while True:
            if str(path) == path.root:
                raise exceptions.PathNotFoundError("could not detect project root")
            elif "pyproject.toml" in os.listdir(path):
                return path

            path = path.parent

    def setup_method(self, method) -> None:
        self.tempdir: pathlib.Path = self.project_root.joinpath("tempdir")
        self.tempdir.mkdir(parents=False, exist_ok=False)

    def teardown_method(self, method) -> None:
        shutil.rmtree(self.tempdir)
        del self.tempdir
