from __future__ import annotations

import json
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table

from bobr.core.change import Change
from bobr.core.models import BacklogItem

console = Console()


def _default_serializer(obj: object) -> str:
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def render_items(items: list[BacklogItem], fmt: str) -> None:
    """Render a list of backlog items as table or JSON."""
    if fmt == "json":
        data = [_item_to_dict(i) for i in items]
        typer.echo(json.dumps(data, default=_default_serializer, indent=2))
        return

    if not items:
        typer.echo("No items found.")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("P", justify="center", width=3)
    table.add_column("Type", width=11)
    table.add_column("Status", width=11)
    table.add_column("Title")
    table.add_column("Epic", style="dim")

    for item in items:
        status_style = _status_style(item.status.value)
        table.add_row(
            item.id,
            str(item.priority),
            item.type.value,
            f"[{status_style}]{item.status.value}[/]",
            item.title,
            item.epic or "",
        )

    console.print(table)
    typer.echo(f"\n{len(items)} item(s)")


def render_item(item: BacklogItem, fmt: str) -> None:
    """Render a single backlog item in detail."""
    if fmt == "json":
        typer.echo(json.dumps(_item_to_dict(item), default=_default_serializer, indent=2))
        return

    console.print(f"[bold cyan]{item.id}[/] {item.title}")
    console.print(f"  Type:     {item.type.value}")
    console.print(f"  Status:   [{_status_style(item.status.value)}]{item.status.value}[/]")
    console.print(f"  Priority: {item.priority}")
    if item.area:
        console.print(f"  Area:     {', '.join(item.area)}")
    if item.epic:
        console.print(f"  Epic:     {item.epic}")
    if item.assignee:
        console.print(f"  Assignee: {item.assignee}")
    if item.depends_on:
        console.print(f"  Depends:  {', '.join(item.depends_on)}")
    if item.blocks:
        console.print(f"  Blocks:   {', '.join(item.blocks)}")
    console.print(f"  Created:  {item.created.isoformat()}")
    console.print(f"  Updated:  {item.updated.isoformat()}")
    if item.body.strip():
        console.print()
        console.print(item.body.strip())


def render_status(data: dict, fmt: str) -> None:
    """Render project status overview."""
    if fmt == "json":
        typer.echo(json.dumps(data, default=_default_serializer, indent=2))
        return

    console.print(f"[bold]Project status[/]  ({data['total']} items)")
    console.print()
    for status, count in data["by_status"].items():
        console.print(f"  {status:12s} {count}")
    if "ready" in data:
        console.print()
        console.print(f"  [bold]ready[/]        {data['ready']}")


def _item_to_dict(item: BacklogItem) -> dict:
    d = item.to_frontmatter()
    if item.body.strip():
        d["body"] = item.body.strip()
    return d


def render_changes(changes: list[Change], bobr_dir, fmt: str) -> None:
    """Render a list of changes as table or JSON."""
    from pathlib import Path

    from bobr.core.change_storage import change_dir, get_existing_artifacts, parse_tasks

    if fmt == "json":
        data = []
        for c in changes:
            d = c.to_frontmatter()
            cpath = change_dir(bobr_dir, c.name)
            d["artifacts"] = get_existing_artifacts(cpath)
            d["tasks"] = parse_tasks(cpath)
            data.append(d)
        typer.echo(json.dumps(data, default=_default_serializer, indent=2))
        return

    if not changes:
        typer.echo("No changes found.")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", no_wrap=True)
    table.add_column("Status", width=14)
    table.add_column("Artifacts")
    table.add_column("Tasks")
    table.add_column("Promotes", style="dim")

    for c in changes:
        cpath = change_dir(bobr_dir, c.name)
        arts = get_existing_artifacts(cpath)
        tasks = parse_tasks(cpath)
        tasks_str = f"{tasks['done']}/{tasks['total']}" if tasks["total"] > 0 else "-"
        style = _change_status_style(c.status.value)
        table.add_row(
            c.id,
            c.name,
            f"[{style}]{c.status.value}[/]",
            ", ".join(arts) if arts else "-",
            tasks_str,
            c.promotes or "",
        )

    console.print(table)
    typer.echo(f"\n{len(changes)} change(s)")


def render_change(change: Change, change_path, fmt: str) -> None:
    """Render a single change in detail."""
    from pathlib import Path

    from bobr.core.change_storage import get_existing_artifacts, parse_tasks

    if fmt == "json":
        d = change.to_frontmatter()
        d["artifacts"] = get_existing_artifacts(change_path)
        d["tasks"] = parse_tasks(change_path)
        typer.echo(json.dumps(d, default=_default_serializer, indent=2))
        return

    style = _change_status_style(change.status.value)
    console.print(f"[bold cyan]{change.id}[/] {change.title}")
    console.print(f"  Name:     {change.name}")
    console.print(f"  Status:   [{style}]{change.status.value}[/]")
    if change.promotes:
        console.print(f"  Promotes: {change.promotes}")

    arts = get_existing_artifacts(change_path)
    console.print(f"  Artifacts: {', '.join(arts) if arts else 'none'}")

    tasks = parse_tasks(change_path)
    if tasks["total"] > 0:
        pct = tasks["done"] * 100 // tasks["total"]
        console.print(f"  Tasks:    {tasks['done']}/{tasks['total']} ({pct}%)")

    console.print(f"  Created:  {change.created.isoformat()}")
    console.print(f"  Updated:  {change.updated.isoformat()}")


def _change_status_style(status: str) -> str:
    return {
        "draft": "dim",
        "proposal": "white",
        "design": "white",
        "tasks": "yellow",
        "implementing": "yellow",
        "verifying": "blue",
        "done": "green",
        "archived": "dim",
    }.get(status, "white")


def _status_style(status: str) -> str:
    return {
        "open": "white",
        "in-progress": "yellow",
        "in-review": "blue",
        "done": "green",
        "blocked": "red",
        "dropped": "dim",
    }.get(status, "white")
