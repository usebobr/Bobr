## Context

Bobr Phase 0 — bootstrap the CLI and `.bobr/` format. No API server, no web UI, no auth, no AI/LLM. Just files + CLI + SQLite cache.

Key references:
- PRD v0.6: `.bobr/requirements/PRD.md`
- Beads (steveyegge/beads): hash IDs, dependency graph, ready/claim
- Expecto/OpenSpec: YAML frontmatter patterns, backlog structure

## Goals / Non-Goals

**Goals:**
- Working `bobr` CLI installable via `pip install -e .`
- `.bobr/backlog/` with YAML frontmatter items, hash-based IDs
- SQLite cache with incremental invalidation (mtime-based)
- Dependency graph with `ready`, `claim`, `blocked`
- `--output json` on all commands for agent consumption
- Tests from day one (pytest, GIVEN/WHEN/THEN docstrings)

**Non-Goals:**
- API server, database (PostgreSQL), web UI
- Authentication, multi-tenant
- MCP server (Phase 1)
- Change workflow (Phase 1) — only basic backlog CRUD
- AI/LLM integration of any kind

## Decisions

### 1. YAML frontmatter over bold-text metadata

Use standard YAML frontmatter (`---` delimiters) instead of Expecto's `**Type**: feature` pattern. Machine-parsable via `python-frontmatter` library. Round-trips cleanly.

### 2. Hash-based IDs (BL-xxxx)

4-char hex hash from `sha1(title + timestamp_ns)`. Safe for parallel agents — no sequential counter, no merge conflicts. Collision detection: if ID exists, re-hash with nonce.

### 3. SQLite cache, not INDEX.md

No INDEX.md file — single point of drift, merge conflict magnet. Instead: `.bobr/.cache/bobr.db` (gitignored). Source of truth = YAML frontmatter in each file. Cache rebuilt incrementally by comparing file mtime/size.

### 4. Bidirectional dependency writes

`bobr dep add BL-a1 BL-b2` writes `depends_on: [BL-b2]` into BL-a1's file AND `blocks: [BL-a1]` into BL-b2's file. Both files updated atomically. SQLite `dependencies` table stores only `(item_id, depends_on)` — `blocks` derived by reversing the query.

### 5. Dataclasses over Pydantic

Minimal dependencies. `BacklogItem` is a plain dataclass. Validation at CLI layer via Typer callbacks. No ORM, no SQLAlchemy.

### 6. Flat module structure

`src/bobr/cli/` (4 files) + `src/bobr/core/` (5 files). No deeper nesting. Easy to navigate.

### 7. hatchling build backend

Lighter than setuptools. Single `pyproject.toml`, no `setup.py`, no `setup.cfg`.

## Risks / Trade-offs

- **[4-char hash collisions]** — 65536 possibilities. For any realistic backlog (<1000 items), collision probability is negligible. Detection + nonce retry as safety net.
- **[mtime-based cache invalidation]** — Some filesystems have 1-second mtime granularity. Two writes within 1 second may not invalidate. Acceptable for CLI tool; write commands also explicitly upsert cache.
- **[No locking for concurrent access]** — Two `bobr` processes writing simultaneously could corrupt. Acceptable for Phase 0 single-user. SQLite WAL mode helps with concurrent reads.
