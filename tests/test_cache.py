from bobr.core.cache import Cache
from bobr.core.models import BacklogItem, ItemType, Status
from bobr.core.storage import resolve_item_path, write_item


def _make_item(id: str, title: str, status: Status = Status.open, priority: int = 2, **kw):
    return BacklogItem(id=id, title=title, type=ItemType.feature, status=status, priority=priority, **kw)


class TestCacheSync:
    def test_sync_picks_up_new_files(self, bobr_paths):
        """GIVEN a new item on disk WHEN cache syncs THEN item appears in query."""
        item = _make_item("BL-aa11", "New item")
        path = resolve_item_path(bobr_paths.backlog, item)
        write_item(path, item)

        cache = Cache(bobr_paths.cache_db)
        cache.sync(bobr_paths.backlog)
        result = cache.get("BL-aa11")
        cache.close()

        assert result is not None
        assert result.title == "New item"

    def test_sync_removes_deleted_files(self, bobr_paths):
        """GIVEN a cached item WHEN file deleted and cache syncs THEN item gone."""
        item = _make_item("BL-bb22", "To delete")
        path = resolve_item_path(bobr_paths.backlog, item)
        write_item(path, item)

        cache = Cache(bobr_paths.cache_db)
        cache.sync(bobr_paths.backlog)
        assert cache.get("BL-bb22") is not None

        path.unlink()
        cache.sync(bobr_paths.backlog)
        assert cache.get("BL-bb22") is None
        cache.close()


class TestReadyItems:
    def test_item_without_deps_is_ready(self, bobr_paths):
        """GIVEN an open item with no deps WHEN get_ready_items THEN it appears."""
        item = _make_item("BL-r001", "Ready task")
        path = resolve_item_path(bobr_paths.backlog, item)
        write_item(path, item)

        cache = Cache(bobr_paths.cache_db)
        cache.sync(bobr_paths.backlog)
        ready = cache.get_ready_items()
        cache.close()

        assert any(i.id == "BL-r001" for i in ready)

    def test_item_with_open_dep_not_ready(self, bobr_paths):
        """GIVEN item A depends on open item B WHEN get_ready_items THEN A not ready."""
        b = _make_item("BL-r002", "Blocker")
        a = _make_item("BL-r003", "Blocked", depends_on=["BL-r002"])

        write_item(resolve_item_path(bobr_paths.backlog, b), b)
        write_item(resolve_item_path(bobr_paths.backlog, a), a)

        cache = Cache(bobr_paths.cache_db)
        cache.sync(bobr_paths.backlog)
        ready = cache.get_ready_items()
        cache.close()

        ready_ids = [i.id for i in ready]
        assert "BL-r002" in ready_ids  # blocker is ready
        assert "BL-r003" not in ready_ids  # blocked is NOT ready

    def test_item_with_done_dep_is_ready(self, bobr_paths):
        """GIVEN item A depends on done item B WHEN get_ready_items THEN A is ready."""
        b = _make_item("BL-r004", "Done blocker", status=Status.done)
        a = _make_item("BL-r005", "Unblocked", depends_on=["BL-r004"])

        write_item(resolve_item_path(bobr_paths.backlog, b), b)
        write_item(resolve_item_path(bobr_paths.backlog, a), a)

        cache = Cache(bobr_paths.cache_db)
        cache.sync(bobr_paths.backlog)
        ready = cache.get_ready_items()
        cache.close()

        assert any(i.id == "BL-r005" for i in ready)
