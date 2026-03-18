from bobr.core.models import BacklogItem, ItemType, Status
from bobr.core.storage import read_item, resolve_item_path, write_item


class TestRoundTrip:
    def test_write_and_read(self, bobr_paths):
        """GIVEN a BacklogItem WHEN written and read back THEN fields match."""
        item = BacklogItem(
            id="BL-test",
            title="Test feature",
            type=ItemType.feature,
            priority=1,
            area=["backend", "api"],
            epic="auth",
            body="## Description\n\nA test feature.\n",
        )
        path = resolve_item_path(bobr_paths.backlog, item)
        write_item(path, item)

        loaded = read_item(path)
        assert loaded.id == "BL-test"
        assert loaded.title == "Test feature"
        assert loaded.type == ItemType.feature
        assert loaded.status == Status.open
        assert loaded.priority == 1
        assert loaded.area == ["backend", "api"]
        assert loaded.epic == "auth"
        assert "test feature" in loaded.body.lower()

    def test_depends_on_roundtrip(self, bobr_paths):
        """GIVEN an item with depends_on WHEN written and read THEN dependencies preserved."""
        item = BacklogItem(
            id="BL-dep1",
            title="Depends on something",
            type=ItemType.bug,
            depends_on=["BL-aaaa", "BL-bbbb"],
            blocks=["BL-cccc"],
        )
        path = resolve_item_path(bobr_paths.backlog, item)
        write_item(path, item)

        loaded = read_item(path)
        assert loaded.depends_on == ["BL-aaaa", "BL-bbbb"]
        assert loaded.blocks == ["BL-cccc"]

    def test_collision_handling(self, bobr_paths):
        """GIVEN two items with same slug but different IDs WHEN resolved THEN different paths."""
        item1 = BacklogItem(id="BL-1111", title="Login fix", type=ItemType.bug)
        item2 = BacklogItem(id="BL-2222", title="Login fix", type=ItemType.bug)

        path1 = resolve_item_path(bobr_paths.backlog, item1)
        write_item(path1, item1)

        path2 = resolve_item_path(bobr_paths.backlog, item2)
        assert path1 != path2
        assert "bl-2222" in path2.name
