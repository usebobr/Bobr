from bobr.core.ids import make_id, slug


class TestMakeId:
    def test_format(self):
        """GIVEN a title WHEN make_id is called THEN returns BL-xxxx format."""
        result = make_id("Fix login bug")
        assert result.startswith("BL-")
        assert len(result) == 7  # "BL-" + 4 hex chars

    def test_hex_chars(self):
        """GIVEN a title WHEN make_id is called THEN the hash part contains only hex chars."""
        result = make_id("Test item")
        hex_part = result[3:]
        assert all(c in "0123456789abcdef" for c in hex_part)

    def test_uniqueness(self):
        """GIVEN the same title WHEN make_id is called twice THEN returns different IDs."""
        id1 = make_id("Same title")
        id2 = make_id("Same title")
        assert id1 != id2  # timestamp makes them unique


class TestSlug:
    def test_basic(self):
        """GIVEN a title WHEN slug is called THEN returns kebab-case."""
        assert slug("Fix Login Bug") == "fix-login-bug"

    def test_special_chars(self):
        """GIVEN a title with special chars WHEN slug is called THEN strips them."""
        assert slug("Add OAuth 2.0 (GitHub)") == "add-oauth-2-0-github"

    def test_truncation(self):
        """GIVEN a very long title WHEN slug is called THEN truncates to 48 chars."""
        long_title = "a" * 100
        assert len(slug(long_title)) == 48

    def test_strips_edges(self):
        """GIVEN a title with leading/trailing spaces WHEN slug is called THEN strips them."""
        assert slug("  hello world  ") == "hello-world"
