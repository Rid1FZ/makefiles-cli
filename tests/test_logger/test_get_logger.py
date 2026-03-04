import logging

import makefiles.logger as logger_mod
from makefiles.logger import get_logger


class TestGetLogger:
    def test_none_returns_root_app_logger(self) -> None:
        """get_logger(None) should return the root application logger."""
        result: logging.Logger = get_logger(None)

        assert result.name == logger_mod._APP_NAME

    def test_name_appended(self) -> None:
        """get_logger('foo') should return a child logger."""
        result: logging.Logger = get_logger("foo")

        assert result.name == f"{logger_mod._APP_NAME}.foo"

    def test_module_name_appended(self) -> None:
        """get_logger(__name__) embeds the full module path."""
        result: logging.Logger = get_logger("makefiles.utils.fileutils.copy_file")

        assert result.name == f"{logger_mod._APP_NAME}.makefiles.utils.fileutils.copy_file"
