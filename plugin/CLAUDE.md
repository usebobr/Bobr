# Bobr — Project Management for AI Agents

This project uses **Bobr** for backlog, requirements, and spec management.

## Golden Rule

**All tasks, requirements, and specs go through `bobr` CLI or MCP tools. Never create your own TODO files or invent custom formats.**

## When to Use Bobr

Bobr is available via MCP tools (preferred) and CLI. Use whichever is available.

### Via MCP Tools (L3)
- Need to know what to work on → `get_ready_items`
- Need to see all tasks → `read_backlog`
- Need filtered view → `read_backlog(status="open", priority=1)`
- Need to start working on a task → `claim_item(item_id="BL-xxxx")`

### Via CLI (L2)
- Need to know what to work on → `uv run bobr backlog ready -o json`
- Need to see all tasks → `uv run bobr backlog list -o json`
- Need to start working on a task → `uv run bobr backlog claim <ID>`
- Need to add a task → `uv run bobr backlog add "Title" -t feature -p 1 -a "area1,area2"`
- Need to update a task → `uv run bobr backlog edit <ID> --status done`
- Need project overview → `uv run bobr status`
- Need to check dependencies → `uv run bobr dep list <ID>`
- Need to see blocked items → `uv run bobr backlog blocked`

## Data Structure

Project data lives in `.bobr/`:
- `.bobr/backlog/` — tasks (markdown + YAML frontmatter)
- `.bobr/requirements/` — PRD, PRFAQ, requirements documents
- `.bobr/specs/` — specifications and changes
- `.bobr/knowledge/` — knowledge base (meetings, documents)

## CLI Reference

### Backlog
```
bobr backlog add TITLE [--type feature|bug|idea|improvement] [--priority 0-4] [--area AREAS] [--epic EPIC] [-o json]
bobr backlog list [--status STATUS] [--priority P] [--type TYPE] [--epic EPIC] [-o json]
bobr backlog show ITEM_ID [-o json]
bobr backlog edit ITEM_ID [--title T] [--status S] [--priority P] [--type T] [--area A] [--assignee A] [-o json]
bobr backlog drop ITEM_ID [-o json]
bobr backlog ready [-o json]
bobr backlog claim ITEM_ID [--assignee ASSIGNEE] [-o json]
bobr backlog blocked [-o json]
```

### Dependencies
```
bobr dep add FROM_ID TO_ID
bobr dep remove FROM_ID TO_ID
bobr dep list ITEM_ID [-o json]
```

### Project
```
bobr status [-o json]
bobr validate [-o json]
bobr init [PATH]
```

## MCP Tools Reference

| Tool | Args | Description |
|------|------|-------------|
| `read_backlog` | `status?`, `priority?`, `item_type?`, `epic?` | List backlog items with optional filters |
| `get_ready_items` | — | Items ready for work (open + no blockers) |
| `claim_item` | `item_id`, `assignee?` | Atomically claim an item (→ in-progress) |

## Task Lifecycle

1. **Pick a task** — `bobr backlog ready` to see what's available
2. **Claim it** — `bobr backlog claim <ID>` before starting work
3. **Do the work** — implement, test, verify
4. **Mark done** — `bobr backlog edit <ID> --status done`
5. **Deliver** — offer to commit, push, and/or create a PR. The task is not finished until code is in the repo.

Never stop after step 4. Always follow through to step 5.

## Conventions

- Priorities: 0 = critical, 1 = high, 2 = medium, 3 = low, 4 = someday
- Statuses: open → in-progress → in-review → done (or blocked / dropped)
- Always use `-o json` for programmatic parsing, `-o table` for user-facing display
