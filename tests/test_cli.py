import json

from typer.testing import CliRunner

from bobr.cli.main import app

runner = CliRunner()


class TestInit:
    def test_init_creates_structure(self, tmp_path, monkeypatch):
        """GIVEN a directory WHEN bobr init THEN .bobr/ structure is created."""
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["init", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / ".bobr" / "backlog" / "epics").exists()
        assert (tmp_path / ".bobr" / "config.yaml").exists()

    def test_init_idempotent(self, bobr_repo):
        """GIVEN an already initialized repo WHEN bobr init again THEN no error."""
        result = runner.invoke(app, ["init", str(bobr_repo)])
        assert result.exit_code == 0


class TestBacklogAdd:
    def test_add_creates_file(self, bobr_repo, monkeypatch):
        """GIVEN an initialized repo WHEN backlog add THEN a file is created."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(app, ["backlog", "add", "Fix login bug", "-t", "bug"])
        assert result.exit_code == 0
        assert "BL-" in result.output

        files = list((bobr_repo / ".bobr" / "backlog").glob("bug-*.md"))
        assert len(files) == 1

    def test_add_json_output(self, bobr_repo, monkeypatch):
        """GIVEN an initialized repo WHEN backlog add --output json THEN valid JSON."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(app, ["backlog", "add", "New feature", "-o", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["title"] == "New feature"
        assert data["type"] == "feature"
        assert data["status"] == "open"


class TestBacklogList:
    def test_list_empty(self, bobr_repo, monkeypatch):
        """GIVEN an empty backlog WHEN list THEN shows no items."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(app, ["backlog", "list"])
        assert result.exit_code == 0
        assert "No items" in result.output

    def test_list_after_add(self, bobr_repo, monkeypatch):
        """GIVEN one item WHEN list THEN shows that item."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["backlog", "add", "Test item"])
        result = runner.invoke(app, ["backlog", "list"])
        assert result.exit_code == 0
        assert "Test item" in result.output

    def test_list_filter_by_status(self, bobr_repo, monkeypatch):
        """GIVEN items WHEN list --status done THEN only done items shown."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["backlog", "add", "Open item"])
        result = runner.invoke(app, ["backlog", "list", "--status", "done", "-o", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 0


class TestBacklogClaim:
    def test_claim_sets_status_and_assignee(self, bobr_repo, monkeypatch):
        """GIVEN an open item WHEN claimed THEN status=in-progress and assignee set."""
        monkeypatch.chdir(bobr_repo)
        add_result = runner.invoke(app, ["backlog", "add", "Claimable", "-o", "json"])
        item_id = json.loads(add_result.output)["id"]

        claim_result = runner.invoke(
            app, ["backlog", "claim", item_id, "--assignee", "claude-code", "-o", "json"]
        )
        assert claim_result.exit_code == 0
        data = json.loads(claim_result.output)
        assert data["status"] == "in-progress"
        assert data["assignee"] == "claude-code"

    def test_claim_already_claimed_fails(self, bobr_repo, monkeypatch):
        """GIVEN an in-progress item WHEN claimed again THEN error."""
        monkeypatch.chdir(bobr_repo)
        add_result = runner.invoke(app, ["backlog", "add", "Already taken", "-o", "json"])
        item_id = json.loads(add_result.output)["id"]
        runner.invoke(app, ["backlog", "claim", item_id])

        result = runner.invoke(app, ["backlog", "claim", item_id])
        assert result.exit_code == 1


class TestBacklogReady:
    def test_ready_shows_unblocked(self, bobr_repo, monkeypatch):
        """GIVEN an open item with no deps WHEN ready THEN item shown."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["backlog", "add", "Ready item"])
        result = runner.invoke(app, ["backlog", "ready", "-o", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) >= 1


class TestDep:
    def test_dep_add_and_list(self, bobr_repo, monkeypatch):
        """GIVEN two items WHEN dep add THEN dependency appears in dep list."""
        monkeypatch.chdir(bobr_repo)
        r1 = runner.invoke(app, ["backlog", "add", "Blocker", "-o", "json"])
        r2 = runner.invoke(app, ["backlog", "add", "Dependent", "-o", "json"])
        id1 = json.loads(r1.output)["id"]
        id2 = json.loads(r2.output)["id"]

        dep_result = runner.invoke(app, ["dep", "add", id2, id1])
        assert dep_result.exit_code == 0

        list_result = runner.invoke(app, ["dep", "list", id2, "-o", "json"])
        data = json.loads(list_result.output)
        assert id1 in data["depends_on"]

    def test_dep_blocks_ready(self, bobr_repo, monkeypatch):
        """GIVEN A depends on B (open) WHEN ready THEN A not in ready list."""
        monkeypatch.chdir(bobr_repo)
        r1 = runner.invoke(app, ["backlog", "add", "Must do first", "-o", "json"])
        r2 = runner.invoke(app, ["backlog", "add", "Needs first done", "-o", "json"])
        id1 = json.loads(r1.output)["id"]
        id2 = json.loads(r2.output)["id"]

        runner.invoke(app, ["dep", "add", id2, id1])

        ready = runner.invoke(app, ["backlog", "ready", "-o", "json"])
        data = json.loads(ready.output)
        ready_ids = [i["id"] for i in data]
        assert id1 in ready_ids
        assert id2 not in ready_ids


class TestStatus:
    def test_status_shows_counts(self, bobr_repo, monkeypatch):
        """GIVEN items in backlog WHEN status THEN shows counts by status."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["backlog", "add", "Item 1"])
        runner.invoke(app, ["backlog", "add", "Item 2"])
        result = runner.invoke(app, ["status", "-o", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == 2
        assert data["by_status"]["open"] == 2


class TestValidate:
    def test_validate_clean(self, bobr_repo, monkeypatch):
        """GIVEN a valid repo WHEN validate THEN exit 0."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["backlog", "add", "Valid item"])
        result = runner.invoke(app, ["validate"])
        assert result.exit_code == 0
