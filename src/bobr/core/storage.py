from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import frontmatter

from bobr.core.ids import slug
from bobr.core.models import BacklogItem


def item_path(backlog_dir: Path, item: BacklogItem) -> Path:
    """Return the file path for a backlog item: backlog/{type}-{slug}.md"""
    s = slug(item.title)
    return backlog_dir / f"{item.type.value}-{s}.md"


def resolve_item_path(backlog_dir: Path, item: BacklogItem) -> Path:
    """Return item path, handling filename collisions by appending the ID."""
    path = item_path(backlog_dir, item)
    if path.exists():
        existing = read_item(path)
        if existing.id != item.id:
            # Collision: different item with same slug — append ID
            s = slug(item.title)
            return backlog_dir / f"{item.type.value}-{s}-{item.id.lower()}.md"
    return path


def read_item(path: Path) -> BacklogItem:
    """Read a backlog item from a markdown file with YAML frontmatter."""
    post = frontmatter.load(str(path))
    return BacklogItem.from_frontmatter(dict(post.metadata), post.content)


def write_item(path: Path, item: BacklogItem) -> None:
    """Write a backlog item to a markdown file with YAML frontmatter."""
    item.updated = datetime.now(timezone.utc)
    post = frontmatter.Post(item.body, **item.to_frontmatter())
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(frontmatter.dumps(post))
        f.write("\n")


def list_item_files(backlog_dir: Path) -> list[Path]:
    """List all backlog item markdown files (excluding epics subdirectory)."""
    if not backlog_dir.exists():
        return []
    return [
        p
        for p in sorted(backlog_dir.glob("*.md"))
        if p.is_file()
    ]


def find_item_file(backlog_dir: Path, item_id: str) -> Path | None:
    """Find the file for a given item ID by scanning frontmatter."""
    for path in list_item_files(backlog_dir):
        try:
            post = frontmatter.load(str(path))
            if post.metadata.get("id") == item_id:
                return path
        except Exception:
            continue
    return None
