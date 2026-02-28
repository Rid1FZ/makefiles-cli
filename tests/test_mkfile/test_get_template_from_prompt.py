from pathlib import Path
from unittest import mock

import pytest

import makefiles.exceptions as exceptions
import makefiles.mkfile as mkfile
import tests.utils as test_utils
from makefiles.types import NaturalNumber


class TestGetTemplateFromPrompt(test_utils.MakefilesTestBase):
    def _setup_templates_dir(self) -> Path:
        templates_dir: Path = self.tempdir.joinpath("templates")
        templates_dir.mkdir()

        test_utils.create_file(templates_dir.joinpath("a.py"))
        test_utils.create_file(templates_dir.joinpath("b.sh"))

        return templates_dir

    def test_uses_manual_picker(self) -> None:
        """Should delegate to picker.manual() when picker='manual'."""
        templates_dir: Path = self._setup_templates_dir()

        with mock.patch("makefiles.utils.picker.manual", return_value="a.py") as mock_manual:
            result = mkfile._get_template_from_prompt(
                t_picker="manual",
                templates_dir=templates_dir,
            )

        mock_manual.assert_called_once()
        assert result == "a.py"

    def test_uses_fzf_picker(self) -> None:
        """Should delegate to picker.fzf() when picker='fzf'."""
        templates_dir: Path = self._setup_templates_dir()

        with mock.patch("makefiles.utils.picker.fzf", return_value="b.sh") as mock_fzf:
            result = mkfile._get_template_from_prompt(
                t_picker="fzf",
                fzf_height=NaturalNumber(10),
                templates_dir=templates_dir,
            )

        mock_fzf.assert_called_once()
        assert result == "b.sh"

    def test_raises_when_no_templates_available(self) -> None:
        """Should raise NoTemplatesAvailableError when template dir is empty."""
        with pytest.raises(exceptions.NoTemplatesAvailableError):
            mkfile._get_template_from_prompt(
                t_picker="manual",
                templates_dir=self.tempdir,
            )
