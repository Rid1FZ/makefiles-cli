import filecmp
import functools
import pathlib
import random
import string

from tests.utils.setup_test import TestMKFile

__all__: list[str] = [
    "compare_files",
    "TestMKFile",
    "create_file",
    "create_empty_file",
    "create_symlink",
    "get_random_str",
]

compare_files = functools.partial(filecmp.cmp, shallow=False)


def create_file(path: pathlib.Path) -> None:
    """Create a file with random string in it"""
    path = path.absolute()
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, mode="w") as file:
        file.write(get_random_str(random.randint(32, 256)))


def create_empty_file(path: pathlib.Path) -> None:
    """Create an empty file in `path`"""
    path = path.absolute()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=False)


def create_symlink(path: pathlib.Path, target: pathlib.Path) -> None:
    """Create a symlink of `path` to `target`"""
    path = path.absolute()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.symlink_to(target, target_is_directory=False)


def get_random_str(length: int = 32) -> str:
    """Return a string of random printable charecters of given length"""
    return "".join(random.choice(string.printable) for _ in range(length))
