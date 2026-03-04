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
