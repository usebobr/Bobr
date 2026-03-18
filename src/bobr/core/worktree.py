from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import frontmatter


@dataclass
class WorktreeRecord:
    item_id: str  # BL-xxxx
    branch: str  # feature/BL-xxxx-slug
    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_frontmatter(self) -> dict:
        """Convert to dict suitable for YAML frontmatter."""
        return {
            "item_id": self.item_id,
            "branch": self.branch,
            "created": self.created.isoformat(),
        }

    @classmethod
    def from_frontmatter(cls, metadata: dict) -> WorktreeRecord:
        """Create WorktreeRecord from parsed YAML frontmatter dict."""
        created = metadata.get("created", datetime.now(timezone.utc))
        if isinstance(created, str):
            created = datetime.fromisoformat(created)
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)

        return cls(
            item_id=metadata["item_id"],
            branch=metadata["branch"],
            created=created,
        )


def read_record(path: Path) -> WorktreeRecord:
    """Read a WorktreeRecord from worktree.md."""
    post = frontmatter.load(path)
    return WorktreeRecord.from_frontmatter(post.metadata)


def write_record(path: Path, record: WorktreeRecord) -> None:
    """Write a WorktreeRecord to worktree.md."""
    post = frontmatter.Post("")
    post.metadata = record.to_frontmatter()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frontmatter.dumps(post) + "\n")
