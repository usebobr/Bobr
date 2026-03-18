"""Bobr MCP Server — L3 agent interface.

Exposes backlog management tools via Model Context Protocol,
allowing AI agents (Claude Code, Cursor, Copilot) to interact
with the bobr project directly.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from bobr.core.cache import Cache
from bobr.core.models import BacklogItem, Status
from bobr.core.repo import find_root, get_paths
from bobr.core.storage import find_item_file, read_item, write_item

mcp = FastMCP("Bobr", json_response=True)


def _item_to_dict(item: BacklogItem) -> dict:
    """Convert a BacklogItem to a JSON-serializable dict."""
    d = item.to_frontmatter()
    if item.body:
        d["body"] = item.body
    return d


def _get_cache() -> tuple:
    """Locate bobr project and return synced (paths, cache)."""
    root = find_root()
    paths = get_paths(root)
    cache = Cache(paths.cache_db)
    cache.sync(paths.backlog)
    return paths, cache


@mcp.tool()
def read_backlog(
    status: str | None = None,
    priority: int | None = None,
    item_type: str | None = None,
    epic: str | None = None,
) -> list[dict]:
    """List backlog items with optional filters.

    Args:
        status: Filter by status (open, in-progress, in-review, done, blocked, dropped).
        priority: Filter by priority (0=highest, 4=lowest).
        item_type: Filter by type (feature, bug, idea, improvement).
        epic: Filter by epic slug.

    Returns:
        List of backlog items matching the filters.
    """
    _, cache = _get_cache()
    items = cache.query(
        status=status,
        priority=priority,
        item_type=item_type,
        epic=epic,
    )
    cache.close()
    return [_item_to_dict(item) for item in items]


@mcp.tool()
def get_ready_items() -> list[dict]:
    """Get backlog items ready for work.

    Returns items with status=open that have no unresolved blocking
    dependencies. These are the items an agent can pick up immediately.

    Returns:
        List of ready backlog items, ordered by priority.
    """
    _, cache = _get_cache()
    items = cache.get_ready_items()
    cache.close()
    return [_item_to_dict(item) for item in items]


@mcp.tool()
def claim_item(item_id: str, assignee: str = "mcp-agent") -> dict:
    """Atomically claim a backlog item for work.

    Sets the item's status to in-progress and assigns it to the given
    assignee. Only items with status open or in-review can be claimed.

    Args:
        item_id: The item ID (e.g. BL-a3f1).
        assignee: Who is claiming the item (default: mcp-agent).

    Returns:
        The updated backlog item.

    Raises:
        ValueError: If item is not found or cannot be claimed.
    """
    paths, cache = _get_cache()

    path = find_item_file(paths.backlog, item_id)
    if not path:
        raise ValueError(f"Item {item_id} not found.")

    item = read_item(path)
    claimable = {Status.open, Status.in_review}
    if item.status not in claimable:
        raise ValueError(
            f"Item {item_id} is '{item.status.value}' and cannot be claimed. "
            f"Only items with status {', '.join(s.value for s in claimable)} can be claimed."
        )

    item.status = Status.in_progress
    item.assignee = assignee
    write_item(path, item)
    cache.upsert_item(item, path)
    cache.close()
    return _item_to_dict(item)


def main() -> None:
    """Entry point for the Bobr MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
