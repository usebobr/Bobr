from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Annotated

import typer

import bobr
from bobr.core.cache import Cache
from bobr.core.models import BacklogItem, Status
from bobr.core.repo import BobrNotFound, find_root, get_paths
from bobr.core.storage import list_item_files, read_item

from .backlog import app as backlog_app
from .dep import app as dep_app
from .output import render_status

app = typer.Typer(
    name="bobr",
    help="Git-native backlog management for AI-assisted teams",
    no_args_is_help=True,
)
app.add_typer(backlog_app)
app.add_typer(dep_app)

OutputFmt = Annotated[str, typer.Option("--output", "-o", help="Output format: table or json")]


@app.command()
def version() -> None:
    """Show bobr version."""
    typer.echo(f"bobr {bobr.__version__}")


@app.command()
def init(
    path: Annotated[Path, typer.Argument(help="Project root directory")] = Path("."),
) -> None:
    """Initialize .bobr/ structure in a project."""
    root = path.resolve()
    bobr_dir = root / ".bobr"

    dirs = [
        bobr_dir / "backlog" / "epics",
        bobr_dir / "requirements",
        bobr_dir / "specs" / "changes",
        bobr_dir / "knowledge",
        bobr_dir / ".cache",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    config = bobr_dir / "config.yaml"
    if not config.exists():
        config.write_text("schema: bobr\nversion: \"0.1\"\n")

    typer.echo(f"Initialized .bobr/ in {root}")


@app.command()
def validate(
    output: OutputFmt = "table",
) -> None:
    """Validate .bobr/ structure and backlog items."""
    root = find_root()
    paths = get_paths(root)
    errors: list[str] = []
    warnings: list[str] = []

    # Check directory structure
    for d in [paths.backlog, paths.epics]:
        if not d.exists():
            errors.append(f"Missing directory: {d.relative_to(root)}")

    # Validate each item — two-pass: collect IDs first, then check deps
    known_ids: set[str] = set()
    parsed_items: list[tuple[Path, BacklogItem]] = []
    files = list_item_files(paths.backlog)
    for f in files:
        try:
            item = read_item(f)
        except Exception as e:
            errors.append(f"{f.name}: failed to parse — {e}")
            continue

        if item.id in known_ids:
            errors.append(f"{f.name}: duplicate ID {item.id}")
        known_ids.add(item.id)
        parsed_items.append((f, item))

    # Second pass: check dependency references against all known IDs
    for _, item in parsed_items:
        for dep_id in item.depends_on:
            if dep_id not in known_ids:
                warnings.append(f"{item.id}: depends_on {dep_id} — not found in backlog")

    if output == "json":
        import json

        typer.echo(json.dumps({"errors": errors, "warnings": warnings}, indent=2))
    else:
        if errors:
            for e in errors:
                typer.echo(f"  ERROR: {e}", err=True)
        if warnings:
            for w in warnings:
                typer.echo(f"  WARN:  {w}", err=True)
        if not errors and not warnings:
            typer.echo(f"Valid. {len(files)} item(s) checked.")
        else:
            typer.echo(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")

    if errors:
        raise typer.Exit(1)


@app.command()
def status(
    output: OutputFmt = "table",
) -> None:
    """Show project status overview."""
    root = find_root()
    paths = get_paths(root)
    cache = Cache(paths.cache_db)
    cache.sync(paths.backlog)

    all_items = cache.query()
    by_status = Counter(item.status.value for item in all_items)

    data = {
        "total": len(all_items),
        "by_status": {s.value: by_status.get(s.value, 0) for s in Status},
    }

    ready_count = len(cache.get_ready_items())
    data["ready"] = ready_count

    cache.close()
    render_status(data, output)


@app.callback()
def main_callback() -> None:
    """Bobr — git-native backlog management for AI-assisted teams."""


def entry() -> None:
    try:
        app()
    except BobrNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1) from None
