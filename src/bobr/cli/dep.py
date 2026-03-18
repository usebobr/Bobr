from __future__ import annotations

from typing import Annotated

import typer

from bobr.core.cache import Cache
from bobr.core.repo import find_root, get_paths
from bobr.core.storage import find_item_file, read_item, write_item

app = typer.Typer(name="dep", help="Manage dependencies between items.", no_args_is_help=True)

OutputFmt = Annotated[str, typer.Option("--output", "-o", help="Output format: table or json")]


def _get_cache() -> tuple:
    root = find_root()
    paths = get_paths(root)
    cache = Cache(paths.cache_db)
    cache.sync(paths.backlog)
    return paths, cache


@app.command("add")
def add_dep(
    from_id: Annotated[str, typer.Argument(help="Item that depends (e.g. BL-a3f1)")],
    to_id: Annotated[str, typer.Argument(help="Item it depends on (e.g. BL-b2c3)")],
) -> None:
    """Add a dependency: FROM depends on TO. Writes to both files."""
    paths, cache = _get_cache()

    from_path = find_item_file(paths.backlog, from_id)
    to_path = find_item_file(paths.backlog, to_id)

    if not from_path:
        typer.echo(f"Item {from_id} not found.", err=True)
        raise typer.Exit(1)
    if not to_path:
        typer.echo(f"Item {to_id} not found.", err=True)
        raise typer.Exit(1)
    if from_id == to_id:
        typer.echo("Cannot depend on self.", err=True)
        raise typer.Exit(1)

    # Update FROM: add to depends_on
    from_item = read_item(from_path)
    if to_id not in from_item.depends_on:
        from_item.depends_on.append(to_id)
        write_item(from_path, from_item)
        cache.upsert_item(from_item, from_path)

    # Update TO: add to blocks
    to_item = read_item(to_path)
    if from_id not in to_item.blocks:
        to_item.blocks.append(from_id)
        write_item(to_path, to_item)
        cache.upsert_item(to_item, to_path)

    cache.close()
    typer.echo(f"{from_id} depends on {to_id}")


@app.command("remove")
def remove_dep(
    from_id: Annotated[str, typer.Argument(help="Item that depends")],
    to_id: Annotated[str, typer.Argument(help="Item it depends on")],
) -> None:
    """Remove a dependency. Updates both files."""
    paths, cache = _get_cache()

    from_path = find_item_file(paths.backlog, from_id)
    to_path = find_item_file(paths.backlog, to_id)

    if not from_path:
        typer.echo(f"Item {from_id} not found.", err=True)
        raise typer.Exit(1)
    if not to_path:
        typer.echo(f"Item {to_id} not found.", err=True)
        raise typer.Exit(1)

    # Update FROM: remove from depends_on
    from_item = read_item(from_path)
    if to_id in from_item.depends_on:
        from_item.depends_on.remove(to_id)
        write_item(from_path, from_item)
        cache.upsert_item(from_item, from_path)

    # Update TO: remove from blocks
    to_item = read_item(to_path)
    if from_id in to_item.blocks:
        to_item.blocks.remove(from_id)
        write_item(to_path, to_item)
        cache.upsert_item(to_item, to_path)

    cache.close()
    typer.echo(f"Removed: {from_id} no longer depends on {to_id}")


@app.command("list")
def list_deps(
    item_id: Annotated[str, typer.Argument(help="Item ID")],
    output: OutputFmt = "table",
) -> None:
    """Show dependencies for an item."""
    _, cache = _get_cache()
    deps = cache.get_dependencies(item_id)
    cache.close()

    if output == "json":
        import json

        typer.echo(json.dumps({"item": item_id, **deps}, indent=2))
        return

    typer.echo(f"Dependencies for {item_id}:")
    if deps["depends_on"]:
        typer.echo(f"  Depends on: {', '.join(deps['depends_on'])}")
    else:
        typer.echo("  Depends on: (none)")
    if deps["blocks"]:
        typer.echo(f"  Blocks:     {', '.join(deps['blocks'])}")
    else:
        typer.echo("  Blocks:     (none)")
