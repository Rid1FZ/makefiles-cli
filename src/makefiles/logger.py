"""
Logging configuration for the makefiles-cli application.

Logs are written to a rotating file at:
    $XDG_STATE_HOME/makefiles-cli/makefiles.log
falling back to ~/.local/state/makefiles-cli/makefiles.log when
XDG_STATE_HOME is not set.

Typical usage:

    # Once, in main():
    from makefiles.logger import setup_logging
    setup_logging()

    # Everywhere else:
    from makefiles.logger import get_logger
    _logger = get_logger(__name__)
    _logger.debug("something happened")
"""

from __future__ import annotations

import logging
import logging.handlers
import os
import pathlib
from typing import Final

_APP_NAME: Final[str] = "makefiles-cli"
_LOG_FILENAME: Final[str] = "makefiles.log"
_MAX_BYTES: Final[int] = 5 * 1024 * 1024  # 5MiB maximum
_BACKUP_COUNT: Final[int] = 2
_LOG_FORMAT: Final[str] = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
_DATE_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%S"


def get_log_dir() -> pathlib.Path:
    """
    Returns the application log directory, honouring `XDG_STATE_HOME`.

    Follows the XDG Base Directory Specification:
    `$XDG_STATE_HOME/makefiles-cli/`.  Defaults to
    `~/.local/state/makefiles-cli/` when the variable is unset.

    Returns:
        pathlib.Path: Absolute log-directory path (not guaranteed to exist yet).
    """
    xdg_state_home: pathlib.Path = pathlib.Path(
        os.environ.get("XDG_STATE_HOME", str(pathlib.Path.home().joinpath(".local", "state")))
    )
    return xdg_state_home.joinpath(_APP_NAME)


def setup_logging() -> logging.Logger:
    """
    Initialises and returns the root application logger.

    Creates the log directory on first call.  Attaches a
    `RotatingFileHandler` that captures `DEBUG`-level records and above.

    This function is **idempotent**: multiple calls never add duplicate
    handlers (safe for test suites that re-import the module).

    Returns:
        logging.Logger: Configured root logger for `makefiles-cli`.

    Raises:
        OSError: If the log directory cannot be created (e.g. permissions).
    """
    log_dir: pathlib.Path = get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file: pathlib.Path = log_dir.joinpath(_LOG_FILENAME)
    logger: logging.Logger = logging.getLogger(_APP_NAME)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler: logging.handlers.RotatingFileHandler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=_MAX_BYTES,
            backupCount=_BACKUP_COUNT,
            encoding="utf-8",
        )
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(fmt=_LOG_FORMAT, datefmt=_DATE_FORMAT))
        logger.addHandler(handler)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Returns a named child logger scoped under the application namespace.

    Pass `__name__` so records embed the full dotted module path, e.g.
    `makefiles-cli.makefiles.utils.fileutils.copy_file`.

    Args:
        name (str | None): Dotted sub-name appended to the app logger name.
            `None` returns the root application logger.

    Returns:
        logging.Logger: A :class:`logging.Logger` instance.

    Example::

        _logger = get_logger(__name__)
        _logger.debug("copying %s -> %s", src, dest)
    """
    if name is None:
        return logging.getLogger(_APP_NAME)
    return logging.getLogger(f"{_APP_NAME}.{name}")
