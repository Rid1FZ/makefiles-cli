import filecmp
import functools
import pathlib
import random
import string

from tests.utils.setup_test import TestMKFile

__all__: list[str] = [
    "TestMKFile",
    "compare_files",
    "create_file",
    "create_symlink",
    "get_random_str",
]

compare_files: functools.partial = functools.partial(filecmp.cmp, shallow=False)


def create_file(path: pathlib.Path, *, empty: bool = False) -> None:
    """
    Create a file.

    Parameters:
        path(pathlib.Path): path to file.
        empty(bool): if `True`, create and empty file with no content.
            Default is `False`
    """
    path = path.absolute()
    path.parent.mkdir(parents=True, exist_ok=True)

    if empty:
        path.touch(exist_ok=False)
    else:
        with open(path, mode="w") as file:
            file.write(get_random_str(random.randint(32, 256), special_chars=True))


def create_symlink(path: pathlib.Path, target: pathlib.Path) -> None:
    """
    Create a symlink.

    Parameters:
        path(pathlib.Path): path, where to create symlink.
        target(pathlib.Path): path to the file/directory the symlink will
            point to.
    """
    path = path.absolute()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.symlink_to(target, target_is_directory=False)


def get_random_str(length: int = 32, *, special_chars: bool = True) -> str:
    """
    Return a string of random charecters.

    Parameters:
        length(int): length of string.
        special_chars(bool): if `True`, use special chars alongside ascii_Letters.

    Returns(str):
        A random string of given length from `string.printable` or `string.ascii_letters`.

    Raises:
        ValueError: if `length` is not an integer or not greater than 0.
    """
    _ensure_natural_number(length, "length")

    return "".join(random.choices(string.printable if special_chars else string.ascii_letters, k=length))
