from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum


class ChangeStatus(StrEnum):
    draft = "draft"  # directory created, proposal not yet written
    proposal = "proposal"  # proposal.md written
    design = "design"  # design.md written
    tasks = "tasks"  # tasks.md written, ready for implementation
    implementing = "implementing"  # tasks being worked on
    verifying = "verifying"  # verification in progress
    done = "done"  # verified, ready to archive
    archived = "archived"  # moved to archive/


# Ordered list of artifacts in the change workflow
ARTIFACT_ORDER = ("proposal", "design", "tasks")
ARTIFACT_FILENAMES = {
    "proposal": "proposal.md",
    "design": "design.md",
    "tasks": "tasks.md",
}


@dataclass
class Change:
    id: str  # CH-xxxx
    name: str  # directory slug
    title: str
    status: ChangeStatus = ChangeStatus.draft
    promotes: str | None = None  # BL-xxxx link to backlog item
    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_frontmatter(self) -> dict:
        """Convert to dict suitable for YAML frontmatter in proposal.md."""
        d: dict = {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "status": self.status.value,
        }
        if self.promotes:
            d["promotes"] = self.promotes
        d["created"] = self.created.isoformat()
        d["updated"] = self.updated.isoformat()
        return d

    @classmethod
    def from_frontmatter(cls, metadata: dict) -> Change:
        """Create Change from parsed YAML frontmatter dict."""
        created = metadata.get("created", datetime.now(timezone.utc))
        if isinstance(created, str):
            created = datetime.fromisoformat(created)

        updated = metadata.get("updated", datetime.now(timezone.utc))
        if isinstance(updated, str):
            updated = datetime.fromisoformat(updated)

        return cls(
            id=metadata["id"],
            name=metadata["name"],
            title=metadata["title"],
            status=ChangeStatus(metadata.get("status", "draft")),
            promotes=metadata.get("promotes"),
            created=created,
            updated=updated,
        )
