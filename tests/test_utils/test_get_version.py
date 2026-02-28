from unittest import mock

import makefiles.utils as utils


class TestGetVersion:
    """
    Tests for utils.get_version()
    """

    _MODULE_KEY: str = "makefiles._version"

    @staticmethod
    def _scrub(module_key: str) -> None:
        """Remove makefiles._version from caches."""
        import sys

        import makefiles as _pkg

        sys.modules.pop(module_key, None)
        _pkg.__dict__.pop("_version", None)

    def setup_method(self, _) -> None:
        self._scrub(self._MODULE_KEY)

    def teardown_method(self, _) -> None:
        self._scrub(self._MODULE_KEY)

    def test_returns_string(self) -> None:
        """get_version() should always return a string."""
        result: str = utils.get_version()
        assert isinstance(result, str)

    def test_returns_unknown_when_version_module_missing(self) -> None:
        """get_version() should return 'unknown' when the _version module cannot be imported."""
        with mock.patch.dict("sys.modules", {self._MODULE_KEY: None}):
            result: str = utils.get_version()
        assert result == "unknown"

    def test_returns_version_string_from_module(self) -> None:
        """get_version() should return the version string from _version.py when available."""
        import makefiles as _pkg

        fake_module: mock.MagicMock = mock.MagicMock()
        fake_module.version = "1.2.3"

        with (
            mock.patch.dict("sys.modules", {self._MODULE_KEY: fake_module}),
            mock.patch.object(_pkg, "_version", fake_module, create=True),
        ):
            result: str = utils.get_version()

        assert result == "1.2.3"
