from __future__ import annotations

import json
import subprocess
from typing import Annotated

import typer

from bobr.core.ids import slug
from bobr.core.repo import find_root, get_paths
from bobr.core.storage import find_item_file, read_item
from bobr.core.worktree import WorktreeRecord, read_record, write_record

app = typer.Typer(name="worktree", help="Manage git worktrees for feature development.", no_args_is_help=True)

OutputFmt = Annotated[str, typer.Option("--output", "-o", help="Output format: table or json")]


@app.command()
def create(
    item_id: Annotated[str, typer.Argument(help="Backlog item ID (e.g. BL-a3f1)")],
    output: OutputFmt = "table",
) -> None:
    """Create a git worktree for a backlog item."""
    root = find_root()
    paths = get_paths(root)

    # Resolve backlog item for title
    item_file = find_item_file(paths.backlog, item_id)
    if not item_file:
        typer.echo(f"Item {item_id} not found.", err=True)
        raise typer.Exit(1)

    item = read_item(item_file)
    title_slug = slug(item.title)
    branch = f"feature/{item_id}-{title_slug}"
    wt_path = paths.worktrees / item_id

    # Idempotent: if worktree already exists, return it
    record_file = wt_path / "worktree.md"
    if record_file.exists():
        record = read_record(record_file)
        _render(record, wt_path, output)
        return

    # Create worktree directory parent
    paths.worktrees.mkdir(parents=True, exist_ok=True)

    # Check if branch already exists
    result = subprocess.run(
        ["git", "-C", str(root), "branch", "--list", branch],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        typer.echo(f"git branch --list failed: {result.stderr.strip()}", err=True)
        raise typer.Exit(1)
    branch_exists = bool(result.stdout.strip())

    # Create worktree
    cmd = ["git", "-C", str(root), "worktree", "add", str(wt_path)]
    if branch_exists:
        cmd.append(branch)
    else:
        cmd.extend(["-b", branch])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        typer.echo(f"git worktree add failed: {result.stderr.strip()}", err=True)
        raise typer.Exit(1)

    # Write worktree record — rollback worktree on failure
    record = WorktreeRecord(item_id=item_id, branch=branch)
    try:
        write_record(record_file, record)
    except Exception as e:
        subprocess.run(
            ["git", "-C", str(root), "worktree", "remove", str(wt_path), "--force"],
            capture_output=True,
        )
        typer.echo(f"Failed to write worktree record: {e}", err=True)
        raise typer.Exit(1)

    _render(record, wt_path, output)


@app.command()
def clean(
    item_id: Annotated[str, typer.Argument(help="Backlog item ID (e.g. BL-a3f1)")],
    output: OutputFmt = "table",
) -> None:
    """Remove a git worktree for a backlog item."""
    root = find_root()
    paths = get_paths(root)
    wt_path = paths.worktrees / item_id

    if not wt_path.exists():
        typer.echo(f"No worktree found for {item_id}.", err=True)
        raise typer.Exit(1)

    result = subprocess.run(
        ["git", "-C", str(root), "worktree", "remove", str(wt_path), "--force"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        typer.echo(f"git worktree remove failed: {result.stderr.strip()}", err=True)
        raise typer.Exit(1)

    if output == "json":
        typer.echo(json.dumps({"item_id": item_id, "status": "removed"}))
    else:
        typer.echo(f"Removed worktree for {item_id}.")


@app.command("list")
def list_worktrees(
    output: OutputFmt = "table",
) -> None:
    """List active worktrees."""
    root = find_root()
    paths = get_paths(root)

    if not paths.worktrees.exists():
        if output == "json":
            typer.echo("[]")
        else:
            typer.echo("No worktrees.")
        return

    records = []
    for wt_dir in sorted(paths.worktrees.iterdir()):
        if not wt_dir.is_dir():
            continue
        record_file = wt_dir / "worktree.md"
        if record_file.exists():
            try:
                record = read_record(record_file)
                records.append((record, wt_dir))
            except Exception:
                typer.echo(f"  Warning: corrupt worktree record at {wt_dir}", err=True)

    if output == "json":
        data = [
            {**r.to_frontmatter(), "path": str(p)}
            for r, p in records
        ]
        typer.echo(json.dumps(data, indent=2))
    else:
        if not records:
            typer.echo("No worktrees.")
            return
        for record, wt_dir in records:
            typer.echo(f"  {record.item_id}  {record.branch}  {wt_dir}")
        typer.echo(f"\n{len(records)} worktree(s)")


def _render(record: WorktreeRecord, wt_path, output: str) -> None:
    """Render a worktree record."""
    if output == "json":
        data = record.to_frontmatter()
        data["path"] = str(wt_path)
        typer.echo(json.dumps(data, indent=2))
    else:
        typer.echo(f"  Item:     {record.item_id}")
        typer.echo(f"  Branch:   {record.branch}")
        typer.echo(f"  Path:     {wt_path}")
