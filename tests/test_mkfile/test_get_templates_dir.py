import os
import unittest.mock as mock
from pathlib import Path

import pytest

import makefiles.mkfile as mkfile


class TestGetTemplatesDir:
    @pytest.mark.parametrize(
        "platform",
        [
            "Linux",
            "FreeBSD",
            "OpenBSD",
            "NetBSD",
        ],
    )
    def test_supported_platforms_with_valid_env_var(self, templates_dir: Path, platform: str) -> None:
        "Should return XDG_TEMPLATES_DIR if set and platform is supported"
        tmp_templates_dir: Path = templates_dir

        with (
            mock.patch.dict(os.environ, {"XDG_TEMPLATES_DIR": str(tmp_templates_dir)}),
            mock.patch("makefiles.mkfile.system", return_value=platform),
        ):
            assert mkfile._get_templates_dir() == tmp_templates_dir

    def test_unsupported_platform(self, templates_dir: Path) -> None:
        "Should return `None` if platform is not supported"
        tmp_templates_dir: Path = templates_dir

        with (
            mock.patch.dict(os.environ, {"XDG_TEMPLATES_DIR": str(tmp_templates_dir)}),
            mock.patch("makefiles.mkfile.system", return_value="NotSupported"),
        ):
            assert mkfile._get_templates_dir() is None


class TestGetTemplatesDirOnFreeBSD:
    def test_linux_with_invalid_env_var(self, tmp_path: Path) -> None:
        "Should return ~/Templates if XDG_TEMPLATES_DIR is not set on FreeBSD"
        with (
            mock.patch.dict(os.environ, {}),
            mock.patch("makefiles.mkfile.system", return_value="FreeBSD"),
            mock.patch("makefiles.mkfile.Path.home", return_value=tmp_path),
        ):
            assert mkfile._get_templates_dir() == tmp_path.joinpath("Templates")


class TestGetTemplatesDirOnOpenBSD:
    def test_linux_with_invalid_env_var(self, tmp_path: Path) -> None:
        "Should return ~/Templates if XDG_TEMPLATES_DIR is not set on OpenBSD"
        with (
            mock.patch.dict(os.environ, {}),
            mock.patch("makefiles.mkfile.system", return_value="OpenBSD"),
            mock.patch("makefiles.mkfile.Path.home", return_value=tmp_path),
        ):
            assert mkfile._get_templates_dir() == tmp_path.joinpath("Templates")


class TestGetTemplatesDirOnNetBSD:
    def test_linux_with_invalid_env_var(self, tmp_path: Path) -> None:
        "Should return ~/Templates if XDG_TEMPLATES_DIR is not set on NetBSD"
        with (
            mock.patch.dict(os.environ, {}),
            mock.patch("makefiles.mkfile.system", return_value="NetBSD"),
            mock.patch("makefiles.mkfile.Path.home", return_value=tmp_path),
        ):
            assert mkfile._get_templates_dir() == tmp_path.joinpath("Templates")
