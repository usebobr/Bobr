from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum


class ItemType(StrEnum):
    feature = "feature"
    bug = "bug"
    idea = "idea"
    improvement = "improvement"


class Status(StrEnum):
    open = "open"
    in_progress = "in-progress"
    in_review = "in-review"
    done = "done"
    blocked = "blocked"
    dropped = "dropped"


@dataclass
class BacklogItem:
    id: str
    title: str
    type: ItemType
    status: Status = Status.open
    priority: int = 2  # 0 = highest, 4 = lowest
    area: list[str] = field(default_factory=list)
    epic: str | None = None
    depends_on: list[str] = field(default_factory=list)
    blocks: list[str] = field(default_factory=list)
    assignee: str | None = None
    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    body: str = ""

    def to_frontmatter(self) -> dict:
        """Convert to dict suitable for YAML frontmatter."""
        d: dict = {
            "id": self.id,
            "title": self.title,
            "type": self.type.value,
            "status": self.status.value,
            "priority": self.priority,
        }
        if self.area:
            d["area"] = self.area
        if self.epic:
            d["epic"] = self.epic
        if self.depends_on:
            d["depends_on"] = self.depends_on
        if self.blocks:
            d["blocks"] = self.blocks
        if self.assignee:
            d["assignee"] = self.assignee
        d["created"] = self.created.isoformat()
        d["updated"] = self.updated.isoformat()
        return d

    @classmethod
    def from_frontmatter(cls, metadata: dict, body: str = "") -> BacklogItem:
        """Create BacklogItem from parsed YAML frontmatter dict."""
        area = metadata.get("area", [])
        if isinstance(area, str):
            area = [a.strip() for a in area.split(",")]

        depends_on = metadata.get("depends_on", [])
        if isinstance(depends_on, str):
            depends_on = [depends_on]

        blocks = metadata.get("blocks", [])
        if isinstance(blocks, str):
            blocks = [blocks]

        created = metadata.get("created", datetime.now(timezone.utc))
        if isinstance(created, str):
            created = datetime.fromisoformat(created)

        updated = metadata.get("updated", datetime.now(timezone.utc))
        if isinstance(updated, str):
            updated = datetime.fromisoformat(updated)

        return cls(
            id=metadata["id"],
            title=metadata["title"],
            type=ItemType(metadata["type"]),
            status=Status(metadata.get("status", "open")),
            priority=int(metadata.get("priority", 2)),
            area=area,
            epic=metadata.get("epic"),
            depends_on=depends_on,
            blocks=blocks,
            assignee=metadata.get("assignee"),
            created=created,
            updated=updated,
            body=body,
        )
