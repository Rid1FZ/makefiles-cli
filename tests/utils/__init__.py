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


def _ensure_natural_number(num: int, name: str) -> None:
    """
    Ensure that given number is a natural number greater than 0.

    Parameters:
        num(int): number to check.
        name(int): name of the variable. Used for error message.

    Raises:
        ValueError: if given number is not an integer or is not greater
            than 0.
    """
    if not (isinstance(num, int) and num > 0):
        raise ValueError(f"{name} must be an integer greater then 0")


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


def generate_tree(
    root_dir: pathlib.Path,
    *,
    max_depth: int = 3,
    max_children: int = 5,
    max_files: int = 3,
    hidden: bool = False,
) -> list[str]:
    """
    Generate a filetree with random files and random subdirectories.

    Parameters:
        root_dir(pathlib.Path): root directory in which tree will be generated.
        max_depth(int): maximum depth of tree. Default is 3.
        max_children(int): maximum children per directory. Default is 3.
        max_files(int): maximum files per directory.
        hidden(bool): if `True`, randomly add hidden files and directories.

    Returns(list[str]):
        A list of all the files created relative to `root_dir`.

    Raises:
        ValueError: if any of `max_depth`, `max_children`, `max_files` is not an
            instance of `int` class or not is greater than 0.
    """
    _ensure_natural_number(max_depth, name="max_depth")
    _ensure_natural_number(max_children, name="max_children")
    _ensure_natural_number(max_files, name="max_files")

    root_dir = root_dir.absolute()
    all_files: list[str] = []

    # Randomly choose between hidden, and non hidden if `hidden` is `True`
    def maybe_hide(name: str) -> str:
        return f".{name}" if hidden and random.choice([True, False]) else name

    def _create_tree(current_path: pathlib.Path, *, depth: int = 1):
        nonlocal all_files, max_children, max_files, maybe_hide

        if depth > max_depth:
            return
        # Create files
        for _ in range(random.randint(1, max_files)):
            file_name: str = maybe_hide(get_random_str(random.randint(16, 32), special_chars=False))
            file_path: pathlib.Path = current_path.joinpath(file_name)

            create_file(file_path, empty=False)
            all_files.append(str(file_path.relative_to(root_dir, walk_up=False)))

        # Create subdirectories
        for _ in range(random.randint(1, max_children)):
            dir_name: str = maybe_hide(get_random_str(random.randint(16, 32), special_chars=False))
            dir_path: pathlib.Path = current_path.joinpath(dir_name)
            dir_path.mkdir(exist_ok=True)
            _create_tree(dir_path, depth=depth + 1)

    root_dir.mkdir(exist_ok=True)
    _create_tree(root_dir, depth=random.randint(1, max_depth))
    return all_files


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
    _ensure_natural_number(length, name="length")

    return "".join(random.choices(string.printable if special_chars else string.ascii_letters, k=length))


def get_random_name() -> str:
    return get_random_str(random.randint(16, 64), special_chars=False)
