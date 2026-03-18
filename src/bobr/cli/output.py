from __future__ import annotations

import json
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table

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


def _status_style(status: str) -> str:
    return {
        "open": "white",
        "in-progress": "yellow",
        "in-review": "blue",
        "done": "green",
        "blocked": "red",
        "dropped": "dim",
    }.get(status, "white")
