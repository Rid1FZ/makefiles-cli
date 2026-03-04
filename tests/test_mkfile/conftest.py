"""
Shared fixtures for the test_mkfile package.
"""

import pathlib

import pytest

import tests.utils as test_utils


@pytest.fixture()
def populated_templates_dir(tempdir: pathlib.Path) -> tuple[pathlib.Path, bytes]:
    """
    Creates a templates directory with a single `sample_template.txt` template containing
    random binary content.

    Returns:
        tuple[pathlib.Path, bytes]: The templates directory path and the exact
        bytes written to the template file, so tests can assert content equality.
    """
    templates_dir: pathlib.Path = tempdir.joinpath("templates")
    templates_dir.mkdir()

    content: bytes = test_utils.get_random_str(special_chars=True).encode()
    templates_dir.joinpath("sample_template.txt").write_bytes(content)

    return templates_dir, content
