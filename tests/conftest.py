from __future__ import annotations

import os
import subprocess
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


@pytest.fixture
def git_bobr_repo(bobr_repo):
    """A bobr repo with an initial git commit."""
    env = {
        "GIT_AUTHOR_NAME": "test",
        "GIT_AUTHOR_EMAIL": "test@test.com",
        "GIT_COMMITTER_NAME": "test",
        "GIT_COMMITTER_EMAIL": "test@test.com",
        "HOME": str(bobr_repo),
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
    }
    subprocess.run(["git", "init"], cwd=bobr_repo, capture_output=True, check=True)
    subprocess.run(["git", "add", "."], cwd=bobr_repo, capture_output=True, check=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=bobr_repo,
        capture_output=True,
        env=env,
        check=True,
    )
    return bobr_repo
