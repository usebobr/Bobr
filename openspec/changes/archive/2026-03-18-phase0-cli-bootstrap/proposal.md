## Why

Bobr has a PRD but no working software. To start dogfooding, we need a CLI that creates and manages `.bobr/` backlog items. This is the foundation — everything else (MCP, Cowork, Telegram) builds on top of structured data in `.bobr/backlog/`.

## What Changes

- New Python package `bobr` with Typer CLI
- `.bobr/` format specification (YAML frontmatter + Markdown)
- Hash-based IDs (`BL-xxxx`) for parallel-agent safety
- SQLite cache for fast queries without reading all files
- Dependency graph (`depends_on`/`blocks`) with `ready`/`claim`/`blocked` commands

## Capabilities

### New Capabilities

- `bobr-init`: Initialize `.bobr/` structure in a project
- `backlog-management`: CRUD for backlog items (add, list, show, edit, drop)
- `dependency-graph`: Dependency tracking between items with transitive resolution
- `agent-readiness`: `ready` (unblocked items), `claim` (atomic pickup), `blocked` (blocked items with reasons)
- `project-status`: Overview of project state and validation

## Impact

- **New files**: ~16 source files in `src/bobr/`, ~5 test files, `pyproject.toml`
- **Modified files**: `.gitignore` (add `.bobr/.cache/`)
- **Dependencies**: typer, python-frontmatter, rich (3 runtime deps)
- **No existing code affected** — greenfield
