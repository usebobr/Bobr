import json

from typer.testing import CliRunner

from bobr.cli.main import app

runner = CliRunner()


class TestContextGenerate:
    def test_generate_empty_project(self, bobr_repo, monkeypatch):
        """GIVEN an empty initialized repo WHEN context generate THEN produces header and backlog section."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(app, ["context", "generate"])
        assert result.exit_code == 0
        assert "Agent Context" in result.output
        assert "Backlog" in result.output

    def test_generate_includes_requirements(self, bobr_repo, monkeypatch):
        """GIVEN requirements exist WHEN context generate THEN requirements section included."""
        monkeypatch.chdir(bobr_repo)
        req_dir = bobr_repo / ".bobr" / "requirements"
        req_dir.mkdir(exist_ok=True)
        (req_dir / "PRD.md").write_text("# Product Requirements\n\nWe need X.\n")

        result = runner.invoke(app, ["context", "generate"])
        assert result.exit_code == 0
        assert "Requirements" in result.output
        assert "Product Requirements" in result.output

    def test_generate_includes_specs(self, bobr_repo, monkeypatch):
        """GIVEN specs exist WHEN context generate THEN specs section included."""
        monkeypatch.chdir(bobr_repo)
        spec_dir = bobr_repo / ".bobr" / "specs" / "auth"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Auth Module\n\nJWT-based auth.\n")

        result = runner.invoke(app, ["context", "generate"])
        assert result.exit_code == 0
        assert "Specifications" in result.output
        assert "Auth Module" in result.output

    def test_generate_includes_active_changes(self, bobr_repo, monkeypatch):
        """GIVEN active changes WHEN context generate THEN active changes listed."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["change", "new", "Add logging"])

        result = runner.invoke(app, ["context", "generate"])
        assert result.exit_code == 0
        assert "Active Changes" in result.output
        assert "Add logging" in result.output

    def test_generate_includes_backlog_items(self, bobr_repo, monkeypatch):
        """GIVEN backlog items WHEN context generate THEN backlog summary shown."""
        monkeypatch.chdir(bobr_repo)
        runner.invoke(app, ["backlog", "add", "Fix auth bug", "-t", "bug"])
        runner.invoke(app, ["backlog", "add", "Add caching"])

        result = runner.invoke(app, ["context", "generate"])
        assert result.exit_code == 0
        assert "Total items" in result.output
        assert "Ready" in result.output

    def test_generate_with_task_filter(self, bobr_repo, monkeypatch):
        """GIVEN a specific task WHEN context generate --task BL-xxxx THEN includes task details."""
        monkeypatch.chdir(bobr_repo)
        add_result = runner.invoke(app, ["backlog", "add", "Target task", "-o", "json"])
        item_id = json.loads(add_result.output)["id"]

        result = runner.invoke(app, ["context", "generate", "--task", item_id])
        assert result.exit_code == 0
        assert "Current Task" in result.output
        assert "Target task" in result.output

    def test_generate_to_file(self, bobr_repo, monkeypatch):
        """GIVEN a project WHEN context generate --file AGENTS.md THEN writes file."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(app, ["context", "generate", "--file", "AGENTS.md"])
        assert result.exit_code == 0
        assert "Context written to" in result.output
        assert (bobr_repo / "AGENTS.md").exists()
        content = (bobr_repo / "AGENTS.md").read_text()
        assert "Agent Context" in content

    def test_generate_includes_conventions(self, bobr_repo, monkeypatch):
        """GIVEN a conventions file WHEN context generate THEN conventions section included."""
        monkeypatch.chdir(bobr_repo)
        knowledge_dir = bobr_repo / ".bobr" / "knowledge"
        knowledge_dir.mkdir(exist_ok=True)
        (knowledge_dir / "conventions.md").write_text(
            "# Coding Standards\n\n- Use snake_case for Python\n- GIVEN/WHEN/THEN for tests\n"
        )

        result = runner.invoke(app, ["context", "generate"])
        assert result.exit_code == 0
        assert "Conventions" in result.output
        assert "snake_case" in result.output

    def test_generate_truncates_long_content(self, bobr_repo, monkeypatch):
        """GIVEN a very long requirement WHEN context generate THEN content truncated."""
        monkeypatch.chdir(bobr_repo)
        req_dir = bobr_repo / ".bobr" / "requirements"
        req_dir.mkdir(exist_ok=True)
        long_text = "# Long Doc\n\n" + "\n".join(f"Line {i}" for i in range(100))
        (req_dir / "long.md").write_text(long_text)

        result = runner.invoke(app, ["context", "generate"])
        assert result.exit_code == 0
        assert "truncated" in result.output
