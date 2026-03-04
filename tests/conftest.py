"""
Session-level pytest configuration.

Redirects XDG_STATE_HOME to a temporary directory for the entire test
session so that no log files are ever written to the real user state
directory (~/.local/state/makefiles-cli/) during test runs.

The temporary directory is created once per session and removed
automatically when pytest exits.
"""

import logging
import pathlib

import pytest


@pytest.fixture(autouse=True, scope="session")
def _redirect_xdg_state_home(tmp_path_factory: pytest.TempPathFactory) -> None:
    """
    Points XDG_STATE_HOME at a throwaway directory for the whole session.

    Marked *autouse* so every test automatically benefits without needing
    to request the fixture explicitly.  Scoped to *session* because the
    log directory only needs to be created once and the same redirect is
    correct for all tests.

    Args:
        tmp_path_factory (pytest.TempPathFactory): Built-in pytest factory
            for session-scoped temporary directories.
    """
    tmp_state: pathlib.Path = tmp_path_factory.mktemp("xdg_state_home", numbered=False)

    import os

    os.environ["XDG_STATE_HOME"] = str(tmp_state)


@pytest.fixture(autouse=True)
def _reset_app_logger() -> None:
    """
    Removes all handlers from the application logger before each test.

    Runs as setup (not teardown) so each test starts with a clean logger
    regardless of whether the previous test failed mid-way.
    """
    from makefiles.logger import _APP_NAME

    app_logger: logging.Logger = logging.getLogger(_APP_NAME)  # ← stays in sync
    for handler in list(app_logger.handlers):
        handler.close()
        app_logger.removeHandler(handler)


@pytest.fixture()
def tempdir(tmp_path: pathlib.Path) -> pathlib.Path:
    """
    Provides a fresh empty directory for each test.

    Delegates to pytest's built-in ``tmp_path`` fixture, which guarantees a
    unique directory per test and removes it automatically afterwards.

    Args:
        tmp_path: Built-in pytest fixture providing a per-test temporary
            directory.

    Returns:
        pathlib.Path: Path to the empty temporary directory.
    """
    return tmp_path


@pytest.fixture()
def templates_dir(tempdir: pathlib.Path) -> pathlib.Path:
    """
    Provides a templates directory pre-populated with one sample template.

    Created as a subdirectory of the `tempdir` fixture so it is removed
    automatically at the end of the test.  Individual tests can create
    additional templates inside the returned directory.

    Args:
        tempdir: The per-test temporary directory fixture.

    Returns:
        pathlib.Path: Path to the populated templates directory.
    """
    import tests.utils as test_utils

    t_dir: pathlib.Path = tempdir.joinpath("templates")
    t_dir.mkdir()
    test_utils.create_file(t_dir.joinpath("script.py"))

    return t_dir
