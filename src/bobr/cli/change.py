from __future__ import annotations

from typing import Annotated, Optional

import typer

from bobr.core.change import ARTIFACT_ORDER, ChangeStatus
from bobr.core.change_storage import (
    archive_change,
    change_dir,
    find_change,
    get_existing_artifacts,
    get_next_artifact,
    list_changes,
    parse_tasks,
    read_change,
    sync_delta_specs,
    write_artifact,
    write_change_meta,
)
from bobr.core.ids import make_id, slug
from bobr.core.repo import find_root, get_paths

from .output import render_change, render_changes

app = typer.Typer(name="change", help="Manage spec-driven changes.", no_args_is_help=True)

OutputFmt = Annotated[str, typer.Option("--output", "-o", help="Output format: table or json")]


@app.command()
def new(
    title: Annotated[str, typer.Argument(help="Change title")],
    promotes: Annotated[Optional[str], typer.Option("--promotes", "-p", help="Backlog item ID (BL-xxxx)")] = None,
    output: OutputFmt = "table",
) -> None:
    """Create a new change with proposal.md."""
    root = find_root()
    paths = get_paths(root)

    change_id = make_id(title, prefix="CH")
    name = slug(title)

    # Check for name collision
    cdir = change_dir(paths.bobr, name)
    if cdir.exists():
        typer.echo(f"Change '{name}' already exists.", err=True)
        raise typer.Exit(1)

    from bobr.core.change import Change

    change = Change(
        id=change_id,
        name=name,
        title=title,
        status=ChangeStatus.proposal,
        promotes=promotes,
    )

    write_change_meta(cdir, change)
    render_change(change, cdir, output)


@app.command("list")
def list_cmd(
    status: Annotated[Optional[str], typer.Option("--status", "-s", help="Filter by status")] = None,
    output: OutputFmt = "table",
) -> None:
    """List active changes."""
    root = find_root()
    paths = get_paths(root)
    all_changes = list_changes(paths.bobr)

    if status:
        all_changes = [c for c in all_changes if c.status.value == status]

    render_changes(all_changes, paths.bobr, output)


@app.command()
def show(
    name: Annotated[str, typer.Argument(help="Change name (directory slug)")],
    output: OutputFmt = "table",
) -> None:
    """Show details of a change."""
    root = find_root()
    paths = get_paths(root)

    cpath = find_change(paths.bobr, name)
    if not cpath:
        typer.echo(f"Change '{name}' not found.", err=True)
        raise typer.Exit(1)

    change = read_change(cpath)
    render_change(change, cpath, output)


@app.command("continue")
def continue_cmd(
    name: Annotated[str, typer.Argument(help="Change name")],
    output: OutputFmt = "table",
) -> None:
    """Create the next artifact for a change."""
    root = find_root()
    paths = get_paths(root)

    cpath = find_change(paths.bobr, name)
    if not cpath:
        typer.echo(f"Change '{name}' not found.", err=True)
        raise typer.Exit(1)

    change = read_change(cpath)
    if change.status == ChangeStatus.archived:
        typer.echo("Change is archived.", err=True)
        raise typer.Exit(1)

    next_art = get_next_artifact(cpath)
    if next_art is None:
        typer.echo("All artifacts already exist. Use 'bobr change verify' next.")
        return

    template = _artifact_template(next_art, change)
    write_artifact(cpath, next_art, template)

    # Update status to match the latest artifact
    change.status = ChangeStatus(next_art)
    write_change_meta(cpath, change)

    typer.echo(f"Created {next_art}.md")
    render_change(change, cpath, output)


@app.command()
def ff(
    name: Annotated[str, typer.Argument(help="Change name")],
    output: OutputFmt = "table",
) -> None:
    """Fast-forward: create all remaining artifacts at once."""
    root = find_root()
    paths = get_paths(root)

    cpath = find_change(paths.bobr, name)
    if not cpath:
        typer.echo(f"Change '{name}' not found.", err=True)
        raise typer.Exit(1)

    change = read_change(cpath)
    if change.status == ChangeStatus.archived:
        typer.echo("Change is archived.", err=True)
        raise typer.Exit(1)

    existing = get_existing_artifacts(cpath)
    created = []
    for art in ARTIFACT_ORDER:
        if art not in existing:
            template = _artifact_template(art, change)
            write_artifact(cpath, art, template)
            created.append(art)

    if not created:
        typer.echo("All artifacts already exist.")
    else:
        change.status = ChangeStatus.tasks
        write_change_meta(cpath, change)
        typer.echo(f"Created: {', '.join(a + '.md' for a in created)}")

    render_change(change, cpath, output)


@app.command()
def verify(
    name: Annotated[str, typer.Argument(help="Change name")],
    output: OutputFmt = "table",
) -> None:
    """Verify that all tasks are complete."""
    root = find_root()
    paths = get_paths(root)

    cpath = find_change(paths.bobr, name)
    if not cpath:
        typer.echo(f"Change '{name}' not found.", err=True)
        raise typer.Exit(1)

    change = read_change(cpath)

    # Check all artifacts exist
    existing = get_existing_artifacts(cpath)
    missing = [a for a in ARTIFACT_ORDER if a not in existing]
    if missing:
        typer.echo(f"Missing artifacts: {', '.join(a + '.md' for a in missing)}", err=True)
        raise typer.Exit(1)

    # Check tasks completion
    tasks = parse_tasks(cpath)
    if tasks["total"] == 0:
        typer.echo("No tasks found in tasks.md.", err=True)
        raise typer.Exit(1)

    if tasks["done"] < tasks["total"]:
        typer.echo(
            f"Tasks incomplete: {tasks['done']}/{tasks['total']} done.",
            err=True,
        )
        raise typer.Exit(1)

    change.status = ChangeStatus.done
    write_change_meta(cpath, change)
    if output != "json":
        typer.echo(f"Verified: {tasks['done']}/{tasks['total']} tasks complete.")
    render_change(change, cpath, output)


@app.command("archive")
def archive_cmd(
    name: Annotated[str, typer.Argument(help="Change name")],
    force: Annotated[bool, typer.Option("--force", "-f", help="Archive without verify")] = False,
    output: OutputFmt = "table",
) -> None:
    """Archive a completed change and sync delta specs."""
    root = find_root()
    paths = get_paths(root)

    cpath = change_dir(paths.bobr, name)
    if not cpath.is_dir():
        typer.echo(f"Change '{name}' not found.", err=True)
        raise typer.Exit(1)

    change = read_change(cpath)

    if not force and change.status != ChangeStatus.done:
        typer.echo(
            f"Change status is '{change.status.value}', not 'done'. "
            "Run 'bobr change verify' first, or use --force.",
            err=True,
        )
        raise typer.Exit(1)

    # Sync delta specs before archiving
    synced = sync_delta_specs(paths.bobr, cpath)
    if synced and output != "json":
        typer.echo(f"Synced delta specs: {', '.join(synced)}")

    # Update status and archive
    change.status = ChangeStatus.archived
    write_change_meta(cpath, change)

    dest = archive_change(paths.bobr, cpath)
    if output != "json":
        typer.echo(f"Archived to {dest.relative_to(root)}")

    # Update promoted backlog item if linked
    if change.promotes:
        _mark_promoted_done(paths, change.promotes)

    render_change(change, dest, output)


def _mark_promoted_done(paths, item_id: str) -> None:
    """Set promoted backlog item status to done."""
    from bobr.core.cache import Cache
    from bobr.core.models import Status
    from bobr.core.storage import find_item_file, read_item, write_item

    item_path = find_item_file(paths.backlog, item_id)
    if not item_path:
        return
    item = read_item(item_path)
    item.status = Status.done
    write_item(item_path, item)
    cache = Cache(paths.cache_db)
    cache.upsert_item(item, item_path)
    cache.close()


def _artifact_template(artifact: str, change) -> str:
    """Generate a minimal template for an artifact."""
    if artifact == "proposal":
        return f"## Why\n\n\n\n## What Changes\n\n"
    elif artifact == "design":
        return (
            f"## Context\n\n{change.title}\n\n"
            f"## Goals / Non-Goals\n\n**Goals:**\n- \n\n**Non-Goals:**\n- \n\n"
            f"## Decisions\n\n"
        )
    elif artifact == "tasks":
        return f"## 1. TODO\n\n- [ ] 1.1 ...\n"
    return ""
