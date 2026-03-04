import os
import pathlib
from unittest import mock

from makefiles.logger import get_log_dir


class TestGetLogDir:
    def test_default_falls_back_to_home_local_state(self) -> None:
        """Without XDG_STATE_HOME the path should be ~/.local/state/makefiles-cli."""
        with mock.patch.dict(os.environ, {}, clear=True):
            # Remove XDG_STATE_HOME if present
            env: dict[str, str] = {k: v for k, v in os.environ.items() if k != "XDG_STATE_HOME"}
            with mock.patch.dict(os.environ, env, clear=True):
                result: pathlib.Path = get_log_dir()

        assert result == pathlib.Path.home().joinpath(".local", "state", "makefiles-cli")

    def test_respects_xdg_state_home(self, tmp_path: pathlib.Path) -> None:
        """XDG_STATE_HOME should be used as the base directory."""
        with mock.patch.dict(os.environ, {"XDG_STATE_HOME": str(tmp_path)}):
            result: pathlib.Path = get_log_dir()

        assert result == tmp_path.joinpath("makefiles-cli")
