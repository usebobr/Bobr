import json

from typer.testing import CliRunner

from bobr.cli.main import app

runner = CliRunner()


class TestChangeNew:
    def test_new_creates_change(self, bobr_repo, monkeypatch):
        """GIVEN an initialized repo WHEN change new THEN a change directory with proposal.md is created."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(app, ["change", "new", "Implement auth"])
        assert result.exit_code == 0
        assert "CH-" in result.output
        assert (bobr_repo / ".bobr" / "specs" / "changes" / "implement-auth" / "proposal.md").exists()

    def test_new_json_output(self, bobr_repo, monkeypatch):
        """GIVEN an initialized repo WHEN change new --output json THEN valid JSON with change metadata."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(app, ["change", "new", "Add caching", "-o", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["title"] == "Add caching"
        assert data["status"] == "proposal"
        assert data["name"] == "add-caching"

    def test_new_with_promotes(self, bobr_repo, monkeypatch):
        """GIVEN a backlog item WHEN change new --promotes BL-xxxx THEN change links to backlog item."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(
            app, ["change", "new", "Fix bug", "--promotes", "BL-1234", "-o", "json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["promotes"] == "BL-1234"

    def test_new_duplicate_name_fails(self, bobr_repo, monkeypatch):
        """GIVEN an existing change WHEN creating another with same name THEN error."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Same name"])
        result = runner.invoke(app, ["change", "new", "Same name"])
        assert result.exit_code == 1
        assert "already exists" in result.output


class TestChangeList:
    def test_list_empty(self, bobr_repo, monkeypatch):
        """GIVEN no changes WHEN change list THEN shows no changes."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(app, ["change", "list"])
        assert result.exit_code == 0
        assert "No changes" in result.output

    def test_list_after_new(self, bobr_repo, monkeypatch):
        """GIVEN one change WHEN change list THEN shows that change."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "My change"])
        result = runner.invoke(app, ["change", "list"])
        assert result.exit_code == 0
        assert "my-change" in result.output

    def test_list_json(self, bobr_repo, monkeypatch):
        """GIVEN changes WHEN list --output json THEN valid JSON array."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "First"])
        runner.invoke(app, ["change", "new", "Second"])
        result = runner.invoke(app, ["change", "list", "-o", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 2

    def test_list_filter_by_status(self, bobr_repo, monkeypatch):
        """GIVEN changes WHEN list --status tasks THEN only matching changes shown."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Only proposal"])
        result = runner.invoke(app, ["change", "list", "--status", "tasks", "-o", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 0


class TestChangeShow:
    def test_show_existing(self, bobr_repo, monkeypatch):
        """GIVEN a change WHEN show THEN displays details."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Show me"])
        result = runner.invoke(app, ["change", "show", "show-me"])
        assert result.exit_code == 0
        assert "Show me" in result.output

    def test_show_not_found(self, bobr_repo, monkeypatch):
        """GIVEN no such change WHEN show THEN error."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(app, ["change", "show", "nonexistent"])
        assert result.exit_code == 1


class TestChangeContinue:
    def test_continue_creates_design(self, bobr_repo, monkeypatch):
        """GIVEN a change with only proposal WHEN continue THEN design.md created."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Step by step"])
        result = runner.invoke(app, ["change", "continue", "step-by-step"])
        assert result.exit_code == 0
        assert "design.md" in result.output
        assert (bobr_repo / ".bobr" / "specs" / "changes" / "step-by-step" / "design.md").exists()

    def test_continue_creates_tasks_after_design(self, bobr_repo, monkeypatch):
        """GIVEN a change with proposal+design WHEN continue THEN tasks.md created."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Full flow"])
        runner.invoke(app, ["change", "continue", "full-flow"])
        result = runner.invoke(app, ["change", "continue", "full-flow"])
        assert result.exit_code == 0
        assert "tasks.md" in result.output

    def test_continue_all_exist(self, bobr_repo, monkeypatch):
        """GIVEN all artifacts exist WHEN continue THEN informs user."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "All done"])
        runner.invoke(app, ["change", "continue", "all-done"])
        runner.invoke(app, ["change", "continue", "all-done"])
        result = runner.invoke(app, ["change", "continue", "all-done"])
        assert result.exit_code == 0
        assert "All artifacts already exist" in result.output


class TestChangeFf:
    def test_ff_creates_all_remaining(self, bobr_repo, monkeypatch):
        """GIVEN a change with only proposal WHEN ff THEN design.md and tasks.md created."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Fast forward"])
        result = runner.invoke(app, ["change", "ff", "fast-forward"])
        assert result.exit_code == 0
        assert "design.md" in result.output
        assert "tasks.md" in result.output
        cdir = bobr_repo / ".bobr" / "specs" / "changes" / "fast-forward"
        assert (cdir / "design.md").exists()
        assert (cdir / "tasks.md").exists()

    def test_ff_when_all_exist(self, bobr_repo, monkeypatch):
        """GIVEN all artifacts exist WHEN ff THEN informs nothing to create."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Already full"])
        runner.invoke(app, ["change", "ff", "already-full"])
        result = runner.invoke(app, ["change", "ff", "already-full"])
        assert result.exit_code == 0
        assert "already exist" in result.output


class TestChangeVerify:
    def test_verify_missing_artifacts(self, bobr_repo, monkeypatch):
        """GIVEN a change with only proposal WHEN verify THEN fails with missing artifacts."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Incomplete"])
        result = runner.invoke(app, ["change", "verify", "incomplete"])
        assert result.exit_code == 1
        assert "Missing" in result.output

    def test_verify_no_tasks(self, bobr_repo, monkeypatch):
        """GIVEN all artifacts but empty tasks WHEN verify THEN fails."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "No tasks"])
        runner.invoke(app, ["change", "ff", "no-tasks"])
        result = runner.invoke(app, ["change", "verify", "no-tasks"])
        assert result.exit_code == 1

    def test_verify_incomplete_tasks(self, bobr_repo, monkeypatch):
        """GIVEN tasks with unchecked items WHEN verify THEN fails."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Half done"])
        runner.invoke(app, ["change", "ff", "half-done"])
        tasks = bobr_repo / ".bobr" / "specs" / "changes" / "half-done" / "tasks.md"
        tasks.write_text("- [x] Done\n- [ ] Not done\n")
        result = runner.invoke(app, ["change", "verify", "half-done"])
        assert result.exit_code == 1
        assert "1/2" in result.output

    def test_verify_all_done(self, bobr_repo, monkeypatch):
        """GIVEN all tasks checked WHEN verify THEN succeeds and status=done."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "All complete"])
        runner.invoke(app, ["change", "ff", "all-complete"])
        tasks = bobr_repo / ".bobr" / "specs" / "changes" / "all-complete" / "tasks.md"
        tasks.write_text("- [x] Task 1\n- [x] Task 2\n")
        result = runner.invoke(app, ["change", "verify", "all-complete", "-o", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["status"] == "done"


class TestChangeArchive:
    def test_archive_requires_done(self, bobr_repo, monkeypatch):
        """GIVEN a change not done WHEN archive THEN fails."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Not ready"])
        result = runner.invoke(app, ["change", "archive", "not-ready"])
        assert result.exit_code == 1
        assert "not 'done'" in result.output

    def test_archive_force(self, bobr_repo, monkeypatch):
        """GIVEN a change not done WHEN archive --force THEN archives anyway."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Force it"])
        result = runner.invoke(app, ["change", "archive", "force-it", "--force"])
        assert result.exit_code == 0
        assert "Archived" in result.output
        assert (bobr_repo / ".bobr" / "specs" / "changes" / "archive" / "force-it").exists()
        assert not (bobr_repo / ".bobr" / "specs" / "changes" / "force-it").exists()

    def test_archive_after_verify(self, bobr_repo, monkeypatch):
        """GIVEN a verified change WHEN archive THEN moves to archive directory."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Proper flow"])
        runner.invoke(app, ["change", "ff", "proper-flow"])
        tasks = bobr_repo / ".bobr" / "specs" / "changes" / "proper-flow" / "tasks.md"
        tasks.write_text("- [x] Done\n")
        runner.invoke(app, ["change", "verify", "proper-flow"])
        result = runner.invoke(app, ["change", "archive", "proper-flow", "-o", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["status"] == "archived"

    def test_archive_syncs_delta_specs(self, bobr_repo, monkeypatch):
        """GIVEN a change with delta spec files WHEN archive THEN specs synced to main."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "With specs"])
        runner.invoke(app, ["change", "ff", "with-specs"])
        cdir = bobr_repo / ".bobr" / "specs" / "changes" / "with-specs"
        tasks = cdir / "tasks.md"
        tasks.write_text("- [x] Done\n")
        # Add a delta spec file
        (cdir / "auth-module.md").write_text("# Auth Module Spec\n\nDetails here.\n")
        runner.invoke(app, ["change", "verify", "with-specs"])
        result = runner.invoke(app, ["change", "archive", "with-specs"])
        assert result.exit_code == 0
        assert "auth-module" in result.output
        assert (bobr_repo / ".bobr" / "specs" / "auth-module" / "spec.md").exists()

    def test_archive_marks_promoted_item_done(self, bobr_repo, monkeypatch):
        """GIVEN a change promoting a backlog item WHEN archive THEN item status=done."""
        monkeypatch.chdir(bobr_repo)
        # Create a backlog item
        add_result = runner.invoke(app, ["backlog", "add", "Fix it", "-o", "json"])
        item_id = json.loads(add_result.output)["id"]

        # Create change that promotes it
        runner.invoke(app, ["change", "new", "Fix flow", "--promotes", item_id])
        runner.invoke(app, ["change", "ff", "fix-flow"])
        tasks = bobr_repo / ".bobr" / "specs" / "changes" / "fix-flow" / "tasks.md"
        tasks.write_text("- [x] Fixed\n")
        runner.invoke(app, ["change", "verify", "fix-flow"])
        runner.invoke(app, ["change", "archive", "fix-flow"])

        # Check backlog item is done
        show_result = runner.invoke(app, ["backlog", "show", item_id, "-o", "json"])
        data = json.loads(show_result.output)
        assert data["status"] == "done"


class TestChangeWorkflowE2E:
    def test_full_lifecycle(self, bobr_repo, monkeypatch):
        """GIVEN an initialized repo WHEN running full change lifecycle THEN all steps succeed."""
        monkeypatch.chdir(bobr_repo)

        # 1. Create
        r = runner.invoke(app, ["change", "new", "E2E test", "-o", "json"])
        assert r.exit_code == 0
        name = json.loads(r.output)["name"]

        # 2. Continue (design)
        r = runner.invoke(app, ["change", "continue", name])
        assert r.exit_code == 0

        # 3. Continue (tasks)
        r = runner.invoke(app, ["change", "continue", name])
        assert r.exit_code == 0

        # 4. Complete tasks
        tasks = bobr_repo / ".bobr" / "specs" / "changes" / name / "tasks.md"
        tasks.write_text("- [x] Implement feature\n- [x] Write tests\n")

        # 5. Verify
        r = runner.invoke(app, ["change", "verify", name, "-o", "json"])
        assert r.exit_code == 0
        assert json.loads(r.output)["status"] == "done"

        # 6. Archive
        r = runner.invoke(app, ["change", "archive", name])
        assert r.exit_code == 0
        assert (bobr_repo / ".bobr" / "specs" / "changes" / "archive" / name).exists()

        # 7. Not in active list
        r = runner.invoke(app, ["change", "list", "-o", "json"])
        data = json.loads(r.output)
        assert all(c["name"] != name for c in data)
