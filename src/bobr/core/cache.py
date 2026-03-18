from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from bobr.core.models import BacklogItem, ItemType, Status
from bobr.core.storage import list_item_files, read_item

SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
    path     TEXT PRIMARY KEY,
    mtime    REAL NOT NULL,
    size     INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id          TEXT PRIMARY KEY,
    path        TEXT NOT NULL,
    title       TEXT NOT NULL,
    type        TEXT NOT NULL,
    status      TEXT NOT NULL,
    priority    INTEGER NOT NULL,
    area        TEXT NOT NULL,
    epic        TEXT,
    assignee    TEXT,
    created     TEXT NOT NULL,
    updated     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dependencies (
    item_id     TEXT NOT NULL,
    depends_on  TEXT NOT NULL,
    PRIMARY KEY (item_id, depends_on)
);

CREATE INDEX IF NOT EXISTS idx_items_status   ON items(status);
CREATE INDEX IF NOT EXISTS idx_items_priority ON items(priority);
CREATE INDEX IF NOT EXISTS idx_items_epic     ON items(epic);
CREATE INDEX IF NOT EXISTS idx_items_type     ON items(type);
CREATE INDEX IF NOT EXISTS idx_deps_depends   ON dependencies(depends_on);
"""

READY_QUERY = """
SELECT i.* FROM items i
WHERE i.status = 'open'
  AND NOT EXISTS (
    SELECT 1 FROM dependencies d
    LEFT JOIN items dep ON dep.id = d.depends_on
    WHERE d.item_id = i.id
      AND (dep.id IS NULL OR dep.status NOT IN ('done', 'dropped'))
  )
ORDER BY i.priority ASC, i.updated DESC
"""

BLOCKED_QUERY = """
SELECT i.* FROM items i
WHERE i.status = 'blocked'
ORDER BY i.priority ASC, i.updated DESC
"""


class Cache:
    def __init__(self, db_path: Path) -> None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self) -> None:
        self.conn.close()

    def sync(self, backlog_dir: Path) -> None:
        """Incrementally sync cache with backlog files on disk."""
        disk_files = list_item_files(backlog_dir)
        disk_paths = {str(p) for p in disk_files}

        for path in disk_files:
            stat = path.stat()
            row = self.conn.execute(
                "SELECT mtime, size FROM files WHERE path = ?", (str(path),)
            ).fetchone()

            if row and row["mtime"] == stat.st_mtime and row["size"] == stat.st_size:
                continue  # cache hit

            try:
                item = read_item(path)
            except Exception:
                continue

            self._upsert_from_item(item, path)

        # Remove entries for deleted files
        existing = {
            r["path"]
            for r in self.conn.execute("SELECT path FROM files").fetchall()
        }
        deleted = existing - disk_paths
        for path in deleted:
            self.conn.execute("DELETE FROM items WHERE path = ?", (path,))
            self.conn.execute("DELETE FROM files WHERE path = ?", (path,))
        if deleted:
            # Clean up orphaned dependencies
            self.conn.execute(
                "DELETE FROM dependencies WHERE item_id NOT IN (SELECT id FROM items)"
            )
        self.conn.commit()

    def _upsert_from_item(self, item: BacklogItem, path: Path) -> None:
        """Insert or update an item in cache from parsed BacklogItem."""
        stat = path.stat()
        self.conn.execute(
            "INSERT OR REPLACE INTO files (path, mtime, size) VALUES (?, ?, ?)",
            (str(path), stat.st_mtime, stat.st_size),
        )
        self.conn.execute(
            """INSERT OR REPLACE INTO items
            (id, path, title, type, status, priority, area, epic, assignee, created, updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                item.id,
                str(path),
                item.title,
                item.type.value,
                item.status.value,
                item.priority,
                json.dumps(item.area),
                item.epic,
                item.assignee,
                item.created.isoformat(),
                item.updated.isoformat(),
            ),
        )
        # Sync dependencies
        self.conn.execute("DELETE FROM dependencies WHERE item_id = ?", (item.id,))
        for dep_id in item.depends_on:
            self.conn.execute(
                "INSERT OR IGNORE INTO dependencies (item_id, depends_on) VALUES (?, ?)",
                (item.id, dep_id),
            )

    def upsert_item(self, item: BacklogItem, path: Path) -> None:
        """Public method to upsert a single item into cache after a write."""
        self._upsert_from_item(item, path)
        self.conn.commit()

    def delete_item(self, item_id: str) -> None:
        """Remove an item from cache."""
        self.conn.execute("DELETE FROM dependencies WHERE item_id = ?", (item_id,))
        self.conn.execute("DELETE FROM dependencies WHERE depends_on = ?", (item_id,))
        row = self.conn.execute("SELECT path FROM items WHERE id = ?", (item_id,)).fetchone()
        if row:
            self.conn.execute("DELETE FROM files WHERE path = ?", (row["path"],))
        self.conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        self.conn.commit()

    def query(
        self,
        status: str | None = None,
        priority: int | None = None,
        item_type: str | None = None,
        epic: str | None = None,
    ) -> list[BacklogItem]:
        """Query items with optional filters."""
        clauses = []
        params: list = []
        if status:
            clauses.append("status = ?")
            params.append(status)
        if priority is not None:
            clauses.append("priority = ?")
            params.append(priority)
        if item_type:
            clauses.append("type = ?")
            params.append(item_type)
        if epic:
            clauses.append("epic = ?")
            params.append(epic)

        where = " AND ".join(clauses) if clauses else "1=1"
        sql = f"SELECT * FROM items WHERE {where} ORDER BY priority ASC, updated DESC"
        rows = self.conn.execute(sql, params).fetchall()
        return [self._row_to_item(r) for r in rows]

    def get(self, item_id: str) -> BacklogItem | None:
        """Get a single item by ID."""
        row = self.conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            return None
        return self._row_to_item(row)

    def get_ready_items(self) -> list[BacklogItem]:
        """Items with status=open and no unresolved blocking dependencies."""
        rows = self.conn.execute(READY_QUERY).fetchall()
        return [self._row_to_item(r) for r in rows]

    def get_blocked_items(self) -> list[BacklogItem]:
        """Items with status=blocked."""
        rows = self.conn.execute(BLOCKED_QUERY).fetchall()
        return [self._row_to_item(r) for r in rows]

    def get_blockers(self, item_id: str) -> list[str]:
        """Return IDs that block a given item (unresolved depends_on)."""
        rows = self.conn.execute(
            """SELECT d.depends_on FROM dependencies d
            JOIN items dep ON dep.id = d.depends_on
            WHERE d.item_id = ?
              AND dep.status NOT IN ('done', 'dropped')""",
            (item_id,),
        ).fetchall()
        return [r["depends_on"] for r in rows]

    def get_dependencies(self, item_id: str) -> dict[str, list[str]]:
        """Return depends_on and blocks lists for an item."""
        deps = self.conn.execute(
            "SELECT depends_on FROM dependencies WHERE item_id = ?", (item_id,)
        ).fetchall()
        blocks = self.conn.execute(
            "SELECT item_id FROM dependencies WHERE depends_on = ?", (item_id,)
        ).fetchall()
        return {
            "depends_on": [r["depends_on"] for r in deps],
            "blocks": [r["item_id"] for r in blocks],
        }

    def _row_to_item(self, row: sqlite3.Row) -> BacklogItem:
        """Convert a database row to BacklogItem (without body)."""
        return BacklogItem(
            id=row["id"],
            title=row["title"],
            type=ItemType(row["type"]),
            status=Status(row["status"]),
            priority=row["priority"],
            area=json.loads(row["area"]) if row["area"] else [],
            epic=row["epic"],
            assignee=row["assignee"],
            depends_on=[],  # not stored in items table, use get_dependencies()
            blocks=[],
            created=_parse_datetime(row["created"]),
            updated=_parse_datetime(row["updated"]),
        )


def _parse_datetime(s: str) -> datetime:
    from datetime import datetime

    return datetime.fromisoformat(s)
