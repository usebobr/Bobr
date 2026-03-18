from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class BobrNotFound(Exception):
    """Raised when .bobr/ directory is not found in any parent."""


@dataclass
class BobrPaths:
    root: Path  # directory containing .bobr/
    bobr: Path  # .bobr/
    backlog: Path  # .bobr/backlog/
    epics: Path  # .bobr/backlog/epics/
    cache_dir: Path  # .bobr/.cache/
    cache_db: Path  # .bobr/.cache/bobr.db


def find_root(start: Path | None = None) -> Path:
    """Walk up from start until .bobr/ directory is found.

    Raises BobrNotFound if not found.
    """
    current = (start or Path.cwd()).resolve()
    while True:
        if (current / ".bobr").is_dir():
            return current
        parent = current.parent
        if parent == current:
            raise BobrNotFound(
                "Not a bobr project (no .bobr/ directory found). Run 'bobr init' first."
            )
        current = parent


def get_paths(root: Path) -> BobrPaths:
    """Return well-known paths for a bobr project."""
    bobr = root / ".bobr"
    return BobrPaths(
        root=root,
        bobr=bobr,
        backlog=bobr / "backlog",
        epics=bobr / "backlog" / "epics",
        cache_dir=bobr / ".cache",
        cache_db=bobr / ".cache" / "bobr.db",
    )
