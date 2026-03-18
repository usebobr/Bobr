from __future__ import annotations

import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from bobr.cli.main import app


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def bobr_repo(tmp_path, monkeypatch):
    """Create an initialized bobr repo in tmp_path and cd into it."""
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(app, ["init", str(tmp_path)], input="y\n")
    assert result.exit_code == 0
    return tmp_path


@pytest.fixture
def bobr_paths(bobr_repo):
    """Return BobrPaths for the test repo."""
    from bobr.core.repo import get_paths

    return get_paths(bobr_repo)
