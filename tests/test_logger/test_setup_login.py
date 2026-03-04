import logging
import os
import pathlib
from unittest import mock

import makefiles.logger as logger_mod
from makefiles.logger import setup_logging


class TestSetupLogging:
    def test_creates_log_directory(self, tmp_path: pathlib.Path) -> None:
        """setup_logging() should create the log directory if absent."""
        log_dir: pathlib.Path = tmp_path.joinpath("state", "makefiles-cli")

        with mock.patch.dict(os.environ, {"XDG_STATE_HOME": str(tmp_path.joinpath("state"))}):
            setup_logging()

        assert log_dir.is_dir()

    def test_returns_logger(self, tmp_path: pathlib.Path) -> None:
        """setup_logging() should return a Logger instance."""
        with mock.patch.dict(os.environ, {"XDG_STATE_HOME": str(tmp_path)}):
            result = setup_logging()

        assert isinstance(result, logging.Logger)

    def test_idempotent_no_duplicate_handlers(self, tmp_path: pathlib.Path) -> None:
        """Calling setup_logging() twice must not add duplicate handlers."""
        with mock.patch.dict(os.environ, {"XDG_STATE_HOME": str(tmp_path)}):
            setup_logging()
            setup_logging()

        logger: logging.Logger = logging.getLogger(logger_mod._APP_NAME)
        assert len(logger.handlers) == 1

    def test_log_file_created(self, tmp_path: pathlib.Path) -> None:
        """A log file should appear after the first write."""
        with mock.patch.dict(os.environ, {"XDG_STATE_HOME": str(tmp_path)}):
            lg = setup_logging()
            lg.info("hello from test")

        log_file: pathlib.Path = tmp_path.joinpath("makefiles-cli", "makefiles.log")
        assert log_file.is_file()
        assert "hello from test" in log_file.read_text(encoding="utf-8")
