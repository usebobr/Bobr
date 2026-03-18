import json

from typer.testing import CliRunner

from bobr.cli.main import app

runner = CliRunner()


class TestSpecList:
    def test_list_empty(self, bobr_repo, monkeypatch):
        """GIVEN no specs WHEN spec list THEN shows no specs."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(app, ["spec", "list"])
        assert result.exit_code == 0
        assert "No specs" in result.output

    def test_list_with_specs(self, bobr_repo, monkeypatch):
        """GIVEN specs exist WHEN spec list THEN shows spec names."""
        monkeypatch.chdir(bobr_repo)
        spec_dir = bobr_repo / ".bobr" / "specs" / "auth-module"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Auth Module\n\nAuthentication spec.\n")

        result = runner.invoke(app, ["spec", "list"])
        assert result.exit_code == 0
        assert "auth-module" in result.output

    def test_list_json(self, bobr_repo, monkeypatch):
        """GIVEN specs exist WHEN spec list --output json THEN valid JSON array."""
        monkeypatch.chdir(bobr_repo)
        spec_dir = bobr_repo / ".bobr" / "specs" / "payments"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Payments\n\nPayment processing.\n")

        result = runner.invoke(app, ["spec", "list", "-o", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 1
        assert data[0]["name"] == "payments"
        assert data[0]["title"] == "Payments"

    def test_list_excludes_changes(self, bobr_repo, monkeypatch):
        """GIVEN specs and changes WHEN spec list THEN changes/ directory excluded."""
        monkeypatch.chdir(bobr_repo)
        # Create a spec
        spec_dir = bobr_repo / ".bobr" / "specs" / "core"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Core\n")

        # Create a change (should not appear)
        runner.invoke(app, ["change", "new", "Some change"])

        result = runner.invoke(app, ["spec", "list", "-o", "json"])
        data = json.loads(result.output)
        names = [s["name"] for s in data]
        assert "core" in names
        assert "changes" not in names

    def test_list_multiple_sorted(self, bobr_repo, monkeypatch):
        """GIVEN multiple specs WHEN spec list THEN sorted alphabetically."""
        monkeypatch.chdir(bobr_repo)
        for name in ["zeta", "alpha", "mid"]:
            d = bobr_repo / ".bobr" / "specs" / name
            d.mkdir(parents=True)
            (d / "spec.md").write_text(f"# {name.title()}\n")

        result = runner.invoke(app, ["spec", "list", "-o", "json"])
        data = json.loads(result.output)
        names = [s["name"] for s in data]
        assert names == ["alpha", "mid", "zeta"]


class TestSpecShow:
    def test_show_existing(self, bobr_repo, monkeypatch):
        """GIVEN a spec WHEN spec show THEN displays content."""
        monkeypatch.chdir(bobr_repo)
        spec_dir = bobr_repo / ".bobr" / "specs" / "auth"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Auth\n\nHandles authentication.\n")

        result = runner.invoke(app, ["spec", "show", "auth"])
        assert result.exit_code == 0
        assert "auth" in result.output

    def test_show_json(self, bobr_repo, monkeypatch):
        """GIVEN a spec WHEN spec show --output json THEN returns name and content."""
        monkeypatch.chdir(bobr_repo)
        spec_dir = bobr_repo / ".bobr" / "specs" / "api"
        spec_dir.mkdir(parents=True)
        content = "# API Spec\n\nREST endpoints.\n"
        (spec_dir / "spec.md").write_text(content)

        result = runner.invoke(app, ["spec", "show", "api", "-o", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["name"] == "api"
        assert data["content"] == content

    def test_show_not_found(self, bobr_repo, monkeypatch):
        """GIVEN no such spec WHEN spec show THEN error."""
        monkeypatch.chdir(bobr_repo)
        result = runner.invoke(app, ["spec", "show", "nonexistent"])
        assert result.exit_code == 1
        assert "not found" in result.output
