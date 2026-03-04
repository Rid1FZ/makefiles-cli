from pathlib import Path
from unittest import mock

import pytest

import makefiles.exceptions as exceptions
import makefiles.mkfile as mkfile
from makefiles.types import NaturalNumber


class TestGetTemplateFromPrompt:
    def test_uses_manual_picker(self, populated_templates_dir: tuple[Path, bytes]) -> None:
        """Should delegate to picker.manual() when picker='manual'."""
        templates_dir: Path
        templates_dir, _ = populated_templates_dir

        with mock.patch("makefiles.utils.picker.manual", return_value="sample_template.txt") as mock_manual:
            result = mkfile._get_template_from_prompt(
                t_picker="manual",
                templates_dir=templates_dir,
            )

        mock_manual.assert_called_once()
        assert result == "sample_template.txt"

    def test_uses_fzf_picker(self, populated_templates_dir: tuple[Path, bytes]) -> None:
        """Should delegate to picker.fzf() when picker='fzf'."""
        templates_dir: Path
        templates_dir, _ = populated_templates_dir

        with mock.patch("makefiles.utils.picker.fzf", return_value="sample_template.txt") as mock_fzf:
            result = mkfile._get_template_from_prompt(
                t_picker="fzf",
                fzf_height=NaturalNumber(10),
                templates_dir=templates_dir,
            )

        mock_fzf.assert_called_once()
        assert result == "sample_template.txt"

    def test_raises_when_no_templates_available(self, tempdir: Path) -> None:
        """Should raise NoTemplatesAvailableError when template dir is empty."""
        with pytest.raises(exceptions.NoTemplatesAvailableError):
            mkfile._get_template_from_prompt(
                t_picker="manual",
                templates_dir=tempdir,
            )
