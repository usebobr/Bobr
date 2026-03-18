import json

from typer.testing import CliRunner

from bobr.cli.main import app
from bobr.core.worktree import WorktreeRecord, read_record, write_record

runner = CliRunner()


class TestWorktreeRecord:
    def test_roundtrip(self, tmp_path):
        """GIVEN a WorktreeRecord WHEN written and read back THEN fields are preserved."""
        record = WorktreeRecord(item_id="BL-a1b2", branch="feature/BL-a1b2-fix-login")
        path = tmp_path / "worktree.md"
        write_record(path, record)
        loaded = read_record(path)
        assert loaded.item_id == "BL-a1b2"
        assert loaded.branch == "feature/BL-a1b2-fix-login"
        assert loaded.created == record.created

    def test_frontmatter_format(self, tmp_path):
        """GIVEN a WorktreeRecord WHEN serialized THEN output is YAML frontmatter markdown."""
        record = WorktreeRecord(item_id="BL-c3d4", branch="feature/BL-c3d4-add-auth")
        path = tmp_path / "worktree.md"
        write_record(path, record)
        content = path.read_text()
        assert content.startswith("---")
        assert "item_id: BL-c3d4" in content
        assert "branch: feature/BL-c3d4-add-auth" in content


class TestWorktreeCreate:
    def test_create_worktree(self, git_bobr_repo):
        """GIVEN an initialized git repo with a backlog item WHEN worktree create THEN worktree and record are created."""
        result = runner.invoke(app, ["backlog", "add", "Fix login bug", "-t", "bug", "-o", "json"])
        assert result.exit_code == 0
        item_id = json.loads(result.output)["id"]

        result = runner.invoke(app, ["worktree", "create", item_id, "-o", "json"])
        assert result.exit_code == 0, result.output
        data = json.loads(result.output)
        assert data["item_id"] == item_id
        assert data["branch"].startswith("feature/")
        assert (git_bobr_repo / ".bobr" / ".worktrees" / item_id / "worktree.md").exists()

    def test_create_idempotent(self, git_bobr_repo):
        """GIVEN an existing worktree WHEN worktree create again THEN returns existing record without error."""
        result = runner.invoke(app, ["backlog", "add", "Test feature", "-o", "json"])
        item_id = json.loads(result.output)["id"]

        result1 = runner.invoke(app, ["worktree", "create", item_id, "-o", "json"])
        assert result1.exit_code == 0
        result2 = runner.invoke(app, ["worktree", "create", item_id, "-o", "json"])
        assert result2.exit_code == 0

        data1 = json.loads(result1.output)
        data2 = json.loads(result2.output)
        assert data1["branch"] == data2["branch"]


class TestWorktreeList:
    def test_list_empty(self, bobr_repo):
        """GIVEN no worktrees WHEN worktree list THEN shows empty."""
        result = runner.invoke(app, ["worktree", "list"])
        assert result.exit_code == 0
        assert "No worktrees" in result.output

    def test_list_json_empty(self, bobr_repo):
        """GIVEN no worktrees WHEN worktree list -o json THEN returns empty array."""
        result = runner.invoke(app, ["worktree", "list", "-o", "json"])
        assert result.exit_code == 0
        assert json.loads(result.output) == []
