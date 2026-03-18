from __future__ import annotations

import pytest

from bobr.core.ids import make_id
from bobr.core.models import BacklogItem, ItemType, Status
from bobr.core.storage import resolve_item_path, write_item
from bobr.mcp.server import claim_item, get_ready_items, read_backlog


def _add_item(paths, title: str, **kwargs) -> BacklogItem:
    """Helper: create and write a backlog item, return it."""
    item_id = make_id(title)
    item = BacklogItem(id=item_id, title=title, **kwargs)
    path = resolve_item_path(paths.backlog, item)
    write_item(path, item)
    return item


class TestReadBacklog:
    def test_returns_all_items(self, bobr_paths):
        """GIVEN a backlog with two items
        WHEN read_backlog is called without filters
        THEN both items are returned.
        """
        _add_item(bobr_paths, "First feature", type=ItemType.feature)
        _add_item(bobr_paths, "Second bug", type=ItemType.bug)

        result = read_backlog()

        assert len(result) == 2
        titles = {item["title"] for item in result}
        assert titles == {"First feature", "Second bug"}

    def test_filter_by_status(self, bobr_paths):
        """GIVEN items with different statuses
        WHEN read_backlog is called with status filter
        THEN only matching items are returned.
        """
        _add_item(bobr_paths, "Open item", type=ItemType.feature, status=Status.open)
        _add_item(bobr_paths, "Done item", type=ItemType.feature, status=Status.done)

        result = read_backlog(status="open")

        assert len(result) == 1
        assert result[0]["title"] == "Open item"

    def test_filter_by_type(self, bobr_paths):
        """GIVEN items of different types
        WHEN read_backlog is called with item_type filter
        THEN only matching items are returned.
        """
        _add_item(bobr_paths, "A feature", type=ItemType.feature)
        _add_item(bobr_paths, "A bug", type=ItemType.bug)

        result = read_backlog(item_type="bug")

        assert len(result) == 1
        assert result[0]["title"] == "A bug"

    def test_empty_backlog(self, bobr_paths):
        """GIVEN an empty backlog
        WHEN read_backlog is called
        THEN an empty list is returned.
        """
        result = read_backlog()

        assert result == []


class TestGetReadyItems:
    def test_returns_open_items_without_blockers(self, bobr_paths):
        """GIVEN an open item with no dependencies
        WHEN get_ready_items is called
        THEN the item is returned.
        """
        _add_item(bobr_paths, "Ready task", type=ItemType.feature)

        result = get_ready_items()

        assert len(result) == 1
        assert result[0]["title"] == "Ready task"

    def test_excludes_in_progress_items(self, bobr_paths):
        """GIVEN an in-progress item
        WHEN get_ready_items is called
        THEN the item is not returned.
        """
        _add_item(
            bobr_paths,
            "Working on it",
            type=ItemType.feature,
            status=Status.in_progress,
        )

        result = get_ready_items()

        assert result == []

    def test_empty_backlog(self, bobr_paths):
        """GIVEN an empty backlog
        WHEN get_ready_items is called
        THEN an empty list is returned.
        """
        result = get_ready_items()

        assert result == []


class TestClaimItem:
    def test_claim_open_item(self, bobr_paths):
        """GIVEN an open backlog item
        WHEN claim_item is called with that item's ID
        THEN the item's status becomes in-progress and assignee is set.
        """
        item = _add_item(bobr_paths, "Claimable task", type=ItemType.feature)

        result = claim_item(item.id, assignee="test-agent")

        assert result["status"] == "in-progress"
        assert result["assignee"] == "test-agent"

    def test_claim_with_default_assignee(self, bobr_paths):
        """GIVEN an open backlog item
        WHEN claim_item is called without specifying assignee
        THEN the default assignee 'mcp-agent' is used.
        """
        item = _add_item(bobr_paths, "Default claim", type=ItemType.feature)

        result = claim_item(item.id)

        assert result["assignee"] == "mcp-agent"

    def test_claim_nonexistent_item_raises(self, bobr_paths):
        """GIVEN no item with the given ID
        WHEN claim_item is called
        THEN a ValueError is raised.
        """
        with pytest.raises(ValueError, match="not found"):
            claim_item("BL-0000")

    def test_claim_done_item_raises(self, bobr_paths):
        """GIVEN a done backlog item
        WHEN claim_item is called
        THEN a ValueError is raised because only open/in-review items can be claimed.
        """
        item = _add_item(
            bobr_paths, "Finished task", type=ItemType.feature, status=Status.done
        )

        with pytest.raises(ValueError, match="cannot be claimed"):
            claim_item(item.id)

    def test_claim_in_review_item(self, bobr_paths):
        """GIVEN an item with status in-review
        WHEN claim_item is called
        THEN the item is claimed successfully.
        """
        item = _add_item(
            bobr_paths,
            "Review task",
            type=ItemType.feature,
            status=Status.in_review,
        )

        result = claim_item(item.id)

        assert result["status"] == "in-progress"
