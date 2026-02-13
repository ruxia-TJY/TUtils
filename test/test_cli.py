"""Tests for CLI module."""

import pytest
from typer.testing import CliRunner

import tutils
from tutils.cli import app

runner = CliRunner()


class TestMainCommands:
    """Test main commands."""

    def test_version_command(self) -> None:
        """Test version command."""
        test_cmd = ["version","-v","--version"]
        for cmd in test_cmd:
            result = runner.invoke(app, [cmd])
            assert result.exit_code == 0
            assert tutils.__version__ in result.output
