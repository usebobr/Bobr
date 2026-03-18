from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from bobr.core.repo import find_root, get_paths

app = typer.Typer(name="spec", help="Browse project specifications.", no_args_is_help=True)

OutputFmt = Annotated[str, typer.Option("--output", "-o", help="Output format: table or json")]


def _specs_dir(bobr_dir: Path) -> Path:
    return bobr_dir / "specs"


def _list_specs(bobr_dir: Path) -> list[dict]:
    """Scan .bobr/specs/ for spec directories (exclude changes/)."""
    sdir = _specs_dir(bobr_dir)
    if not sdir.exists():
        return []
    results = []
    for d in sorted(sdir.iterdir()):
        if not d.is_dir() or d.name == "changes":
            continue
        spec_file = d / "spec.md"
        if not spec_file.exists():
            continue
        text = spec_file.read_text()
        # Extract first non-empty line as title
        title = ""
        for line in text.splitlines():
            stripped = line.strip().lstrip("#").strip()
            if stripped:
                title = stripped
                break
        results.append({
            "name": d.name,
            "path": str(spec_file),
            "title": title,
            "size": len(text),
        })
    return results


@app.command("list")
def list_cmd(
    output: OutputFmt = "table",
) -> None:
    """List all project specifications."""
    root = find_root()
    paths = get_paths(root)
    specs = _list_specs(paths.bobr)

    if output == "json":
        import json

        typer.echo(json.dumps(specs, indent=2))
        return

    if not specs:
        typer.echo("No specs found.")
        return

    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(show_header=True, header_style="bold")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Title")
    table.add_column("Size", justify="right")

    for s in specs:
        table.add_row(s["name"], s["title"], f"{s['size']}b")

    console.print(table)
    typer.echo(f"\n{len(specs)} spec(s)")


@app.command()
def show(
    name: Annotated[str, typer.Argument(help="Spec name (directory name)")],
    output: OutputFmt = "table",
) -> None:
    """Show contents of a specification."""
    root = find_root()
    paths = get_paths(root)
    spec_file = _specs_dir(paths.bobr) / name / "spec.md"

    if not spec_file.exists():
        typer.echo(f"Spec '{name}' not found.", err=True)
        raise typer.Exit(1)

    text = spec_file.read_text()

    if output == "json":
        import json

        typer.echo(json.dumps({"name": name, "content": text}, indent=2))
        return

    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    console.print(f"[bold cyan]{name}[/]  ({spec_file.relative_to(root)})")
    console.print()
    console.print(Markdown(text))
