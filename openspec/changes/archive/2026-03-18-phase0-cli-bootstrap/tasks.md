## 1. Package Skeleton

- [ ] 1.1 Create `pyproject.toml` (hatchling, typer+python-frontmatter+rich, entry point `bobr`)
- [ ] 1.2 Create `src/bobr/__init__.py` with version
- [ ] 1.3 Create all `__init__.py` stubs for `cli/` and `core/`
- [ ] 1.4 Create `.gitignore` entries (`.bobr/.cache/`, `*.egg-info`, etc.)
- [ ] 1.5 Verify `pip install -e .` and `bobr --help`

## 2. Core: Models and IDs

- [ ] 2.1 `core/models.py`: BacklogItem dataclass, ItemType/Status enums, to_dict/from_dict
- [ ] 2.2 `core/ids.py`: make_id(title), slug(title)
- [ ] 2.3 `core/repo.py`: find_root(), BobrPaths, get_paths()
- [ ] 2.4 `tests/test_ids.py`, `tests/test_models.py`

## 3. Core: Storage (Markdown I/O)

- [ ] 3.1 `core/storage.py`: read_item, write_item, item_path, list_item_files
- [ ] 3.2 `tests/test_storage.py`: round-trip read/write, frontmatter parsing

## 4. Core: SQLite Cache

- [ ] 4.1 `core/cache.py`: Cache class, schema init, sync(), query(), upsert_item, delete_item
- [ ] 4.2 `core/cache.py`: get_ready_items(), get_blocked_items(), get_dependencies()
- [ ] 4.3 `tests/test_cache.py`: sync, query, ready/blocked logic

## 5. CLI: Output and Init

- [ ] 5.1 `cli/output.py`: render_items, render_item, render_dict (table + JSON)
- [ ] 5.2 `cli/main.py`: root app, `bobr init`, `bobr validate`, `bobr status`
- [ ] 5.3 `tests/conftest.py`: bobr_repo fixture (tmp_path + init)

## 6. CLI: Backlog Commands

- [ ] 6.1 `cli/backlog.py`: `add` (create item with hash ID)
- [ ] 6.2 `cli/backlog.py`: `list` (with --status, --priority, --type, --epic filters)
- [ ] 6.3 `cli/backlog.py`: `show` (item details)
- [ ] 6.4 `cli/backlog.py`: `edit` (update fields)
- [ ] 6.5 `cli/backlog.py`: `drop` (mark as dropped)
- [ ] 6.6 `cli/backlog.py`: `ready` (unblocked items)
- [ ] 6.7 `cli/backlog.py`: `claim` (atomic assignee + in-progress)
- [ ] 6.8 `cli/backlog.py`: `blocked` (blocked items with reasons)
- [ ] 6.9 `tests/test_cli.py`: CliRunner tests for all commands

## 7. CLI: Dependency Commands

- [ ] 7.1 `cli/dep.py`: `add` (bidirectional write to both files)
- [ ] 7.2 `cli/dep.py`: `remove` (bidirectional removal)
- [ ] 7.3 `cli/dep.py`: `list` (show depends_on + blocks for item)
- [ ] 7.4 `tests/test_cli.py`: dep command tests
