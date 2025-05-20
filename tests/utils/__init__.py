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
    "create_symlink",
    "get_random_str",
]

compare_files = functools.partial(filecmp.cmp, shallow=False)


def create_file(path: pathlib.Path, *, empty: bool = False) -> None:
    """Create a file in considering `path` as path to file"""
    path = path.absolute()
    path.parent.mkdir(parents=True, exist_ok=True)

    if empty:
        path.touch(exist_ok=False)
    else:
        with open(path, mode="w") as file:
            file.write(get_random_str(random.randint(32, 256), special_chars=True))


def create_symlink(path: pathlib.Path, target: pathlib.Path) -> None:
    """Create a symlink of `path` to `target`"""
    path = path.absolute()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.symlink_to(target, target_is_directory=False)


def get_random_str(length: int = 32, *, special_chars: bool = True) -> str:
    """Return a string of random printable charecters of given length"""
    return "".join(random.choices(string.printable if special_chars else string.ascii_letters, k=length))
