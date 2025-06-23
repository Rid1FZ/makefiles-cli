import os
import pathlib
import shutil

import makefiles.exceptions as exceptions


class MakefilesTestBase:
    """
    Base class for pytest test cases that require access to the project root and temporary directories.

    This class is intended to be inherited by all test classes in the project that require setup and
    teardown of a temporary directory within the project root. It provides a mechanism to locate the
    project's root directory dynamically by searching for the presence of a `pyproject.toml` file.

    Attributes:
        tempdir (pathlib.Path): A temporary directory created before each test method and deleted after.

    Properties:
        project_root (pathlib.Path): Lazily evaluated property that returns the root directory of the
            project, identified by the presence of a `pyproject.toml` file.

    Methods:
        setup_method(method): Creates a temporary directory under the project root before each test method.
        teardown_method(method): Removes the temporary directory created for the test method.

    Raises:
        PathNotFoundError: If the project root cannot be found by traversing up the directory tree.
    """

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
