import filecmp
import functools
import pathlib
import random
import string

from tests.utils.setup_test import MakefilesTestBase

__all__: list[str] = [
    "MakefilesTestBase",
    "compare_files",
    "create_file",
    "generate_tree",
    "create_symlink",
    "get_random_str",
    "get_random_name",
]

compare_files: functools.partial = functools.partial(filecmp.cmp, shallow=False)


def _ensure_natural_number(num: int, name: str) -> None:
    """
    Validates that a given number is a natural number (positive integer).

    Args:
        num (int): The number to validate.
        name (str): The name of the variable being validated, used in the error message.

    Raises:
        ValueError: If the number is not an integer greater than 0.
    """
    if not (isinstance(num, int) and num > 0):
        raise ValueError(f"{name} must be an integer greater then 0")


def create_file(path: pathlib.Path, *, empty: bool = False) -> None:
    """
    Creates a file at the specified path, optionally with random content.

    Args:
        path (pathlib.Path): The full path where the file will be created.
        empty (bool, optional): If True, creates an empty file. If False (default),
            writes random content to the file.

    Raises:
        FileExistsError: If `empty` is True and the file already exists.
        OSError: For any underlying OS-related issues during directory or file creation.
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
    Generates a random directory tree with files and subdirectories.

    Args:
        root_dir (pathlib.Path): The root directory where the tree will be generated.
        max_depth (int, optional): Maximum depth of the directory tree. Must be > 0. Default is 3.
        max_children (int, optional): Maximum number of subdirectories per directory. Must be > 0. Default is 5.
        max_files (int, optional): Maximum number of files per directory. Must be > 0. Default is 3.
        hidden (bool, optional): If True, some files and directories will be hidden (prefixed with '.'). Default is False.

    Returns:
        list[str]: A list of all file paths created, relative to `root_dir`.

    Raises:
        ValueError: If `max_depth`, `max_children`, or `max_files` is not a positive integer.
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
    Creates a symbolic link at the specified path pointing to the target.

    Args:
        path (pathlib.Path): The location where the symlink will be created.
        target (pathlib.Path): The file or directory the symlink will point to.

    Raises:
        FileExistsError: If the symlink already exists.
        OSError: For other OS-level errors such as permission issues.
    """
    path = path.absolute()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.symlink_to(target, target_is_directory=False)


def get_random_str(length: int = 32, *, special_chars: bool = True) -> str:
    """
    Generates a random string of the specified length.

    Args:
        length (int): The desired length of the string. Must be greater than 0.
        special_chars (bool, optional): If True, includes special characters from `string.printable`.
            If False, uses only ASCII letters. Default is True.

    Returns:
        str: A random string composed of either `string.printable` or `string.ascii_letters`.

    Raises:
        ValueError: If `length` is not a positive integer.
    """
    _ensure_natural_number(length, name="length")

    return "".join(random.choices(string.printable if special_chars else string.ascii_letters, k=length))


def get_random_name() -> str:
    """
    Generates a random name-like string consisting of ASCII letters.

    Returns:
        str: A random string of 16 to 64 ASCII letters, with no special characters.

    Note:
        This function is a convenience wrapper around `get_random_str` with
        a randomized length and `special_chars=False`.
    """
    return get_random_str(random.randint(16, 64), special_chars=False)
