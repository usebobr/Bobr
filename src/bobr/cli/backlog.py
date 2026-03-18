from __future__ import annotations

from typing import Annotated, Optional

import typer

from bobr.core.cache import Cache
from bobr.core.ids import make_id
from bobr.core.models import BacklogItem, ItemType, Status
from bobr.core.repo import find_root, get_paths
from bobr.core.storage import find_item_file, read_item, resolve_item_path, write_item

from .output import render_item, render_items

app = typer.Typer(name="backlog", help="Manage backlog items.", no_args_is_help=True)

OutputFmt = Annotated[str, typer.Option("--output", "-o", help="Output format: table or json")]


def _get_cache() -> tuple:
    root = find_root()
    paths = get_paths(root)
    cache = Cache(paths.cache_db)
    cache.sync(paths.backlog)
    return paths, cache


@app.command()
def add(
    title: Annotated[str, typer.Argument(help="Item title")],
    item_type: Annotated[str, typer.Option("--type", "-t", help="feature/bug/idea/improvement")] = "feature",
    priority: Annotated[int, typer.Option("--priority", "-p", help="Priority 0-4 (0=highest)")] = 2,
    area: Annotated[Optional[str], typer.Option("--area", "-a", help="Comma-separated areas")] = None,
    epic: Annotated[Optional[str], typer.Option("--epic", "-e", help="Epic slug")] = None,
    output: OutputFmt = "table",
) -> None:
    """Add a new backlog item."""
    paths, cache = _get_cache()

    item_id = make_id(title)
    # Collision check
    while cache.get(item_id):
        item_id = make_id(title + item_id)

    areas = [a.strip() for a in area.split(",")] if area else []
    item = BacklogItem(
        id=item_id,
        title=title,
        type=ItemType(item_type),
        priority=priority,
        area=areas,
        epic=epic,
    )

    path = resolve_item_path(paths.backlog, item)
    write_item(path, item)
    cache.upsert_item(item, path)
    cache.close()

    render_item(item, output)


@app.command("list")
def list_items(
    status: Annotated[Optional[str], typer.Option("--status", "-s", help="Filter by status")] = None,
    priority: Annotated[Optional[int], typer.Option("--priority", "-p", help="Filter by priority")] = None,
    item_type: Annotated[Optional[str], typer.Option("--type", "-t", help="Filter by type")] = None,
    epic: Annotated[Optional[str], typer.Option("--epic", "-e", help="Filter by epic")] = None,
    output: OutputFmt = "table",
) -> None:
    """List backlog items with optional filters."""
    _, cache = _get_cache()
    items = cache.query(status=status, priority=priority, item_type=item_type, epic=epic)
    cache.close()
    render_items(items, output)


@app.command()
def show(
    item_id: Annotated[str, typer.Argument(help="Item ID (e.g. BL-a3f1)")],
    output: OutputFmt = "table",
) -> None:
    """Show detailed info about a backlog item."""
    paths, cache = _get_cache()

    # Read full item from file (includes body)
    path = find_item_file(paths.backlog, item_id)
    if not path:
        typer.echo(f"Item {item_id} not found.", err=True)
        raise typer.Exit(1)

    item = read_item(path)
    deps = cache.get_dependencies(item_id)
    item.depends_on = deps["depends_on"]
    item.blocks = deps["blocks"]
    cache.close()
    render_item(item, output)


@app.command()
def edit(
    item_id: Annotated[str, typer.Argument(help="Item ID")],
    title: Annotated[Optional[str], typer.Option("--title")] = None,
    status: Annotated[Optional[str], typer.Option("--status", "-s")] = None,
    priority: Annotated[Optional[int], typer.Option("--priority", "-p")] = None,
    item_type: Annotated[Optional[str], typer.Option("--type", "-t")] = None,
    area: Annotated[Optional[str], typer.Option("--area", "-a")] = None,
    epic: Annotated[Optional[str], typer.Option("--epic", "-e")] = None,
    assignee: Annotated[Optional[str], typer.Option("--assignee")] = None,
    output: OutputFmt = "table",
) -> None:
    """Edit a backlog item's fields."""
    paths, cache = _get_cache()

    path = find_item_file(paths.backlog, item_id)
    if not path:
        typer.echo(f"Item {item_id} not found.", err=True)
        raise typer.Exit(1)

    item = read_item(path)
    if title is not None:
        item.title = title
    if status is not None:
        item.status = Status(status)
    if priority is not None:
        item.priority = priority
    if item_type is not None:
        item.type = ItemType(item_type)
    if area is not None:
        item.area = [a.strip() for a in area.split(",")] if area else []
    if epic is not None:
        item.epic = epic if epic else None
    if assignee is not None:
        item.assignee = assignee if assignee else None

    write_item(path, item)
    cache.upsert_item(item, path)
    cache.close()
    render_item(item, output)


@app.command()
def drop(
    item_id: Annotated[str, typer.Argument(help="Item ID")],
    output: OutputFmt = "table",
) -> None:
    """Mark a backlog item as dropped."""
    paths, cache = _get_cache()

    path = find_item_file(paths.backlog, item_id)
    if not path:
        typer.echo(f"Item {item_id} not found.", err=True)
        raise typer.Exit(1)

    item = read_item(path)
    item.status = Status.dropped
    write_item(path, item)
    cache.upsert_item(item, path)
    cache.close()
    render_item(item, output)


@app.command()
def ready(
    output: OutputFmt = "table",
) -> None:
    """Show items ready for work (no open blockers)."""
    _, cache = _get_cache()
    items = cache.get_ready_items()
    cache.close()
    render_items(items, output)


@app.command()
def claim(
    item_id: Annotated[str, typer.Argument(help="Item ID")],
    assignee: Annotated[str, typer.Option("--assignee", "-a", help="Who claims")] = "human",
    output: OutputFmt = "table",
) -> None:
    """Atomically claim an item (set assignee + status: in-progress)."""
    paths, cache = _get_cache()

    path = find_item_file(paths.backlog, item_id)
    if not path:
        typer.echo(f"Item {item_id} not found.", err=True)
        raise typer.Exit(1)

    item = read_item(path)
    claimable = {Status.open, Status.in_review}
    if item.status not in claimable:
        typer.echo(
            f"Item {item_id} is {item.status.value} and cannot be claimed.", err=True
        )
        raise typer.Exit(1)

    item.status = Status.in_progress
    item.assignee = assignee
    write_item(path, item)
    cache.upsert_item(item, path)
    cache.close()
    render_item(item, output)


@app.command()
def blocked(
    output: OutputFmt = "table",
) -> None:
    """Show blocked items with their blockers."""
    _, cache = _get_cache()
    items = cache.get_blocked_items()

    if output == "json":
        import json

        data = []
        for item in items:
            d = item.to_frontmatter()
            d["blocked_by"] = cache.get_blockers(item.id)
            data.append(d)
        typer.echo(json.dumps(data, indent=2))
    else:
        if not items:
            typer.echo("No blocked items.")
        else:
            for item in items:
                blockers = cache.get_blockers(item.id)
                blocker_str = ", ".join(blockers) if blockers else "manually blocked"
                typer.echo(f"  {item.id}  P{item.priority}  {item.title}  ← {blocker_str}")
            typer.echo(f"\n{len(items)} blocked item(s)")

    cache.close()
