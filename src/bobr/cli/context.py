from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer

from bobr.core.context import generate_context
from bobr.core.repo import find_root, get_paths

app = typer.Typer(name="context", help="Generate agent context files.", no_args_is_help=True)


@app.command()
def generate(
    task: Annotated[Optional[str], typer.Option("--task", "-t", help="Focus on specific task (BL-xxxx)")] = None,
    output_file: Annotated[Optional[Path], typer.Option("--file", "-f", help="Write to file (default: stdout)")] = None,
) -> None:
    """Generate context markdown for AI agents.

    Collects requirements, specs, active changes, and backlog status
    into a single context document suitable for CLAUDE.md or AGENTS.md.
    """
    root = find_root()
    paths = get_paths(root)

    content = generate_context(paths, task_id=task)

    if output_file:
        target = output_file if output_file.is_absolute() else root / output_file
        target.write_text(content + "\n")
        typer.echo(f"Context written to {target.relative_to(root)}")
    else:
        typer.echo(content)
