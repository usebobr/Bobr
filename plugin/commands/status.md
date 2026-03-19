---
name: bobr-status
description: Show full Bobr project status — backlog, requirements, knowledge, and overall health
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Project Status

Provide a comprehensive overview of the project state.

## Gather data

Run these commands and read these locations in parallel:

1. `uv run bobr status` — project overview
2. `uv run bobr backlog ready -o json` — items ready for work
3. `uv run bobr backlog list --status in-progress -o json` — items in progress
4. `uv run bobr backlog blocked -o json` — blocked items
5. List files in `.bobr/requirements/` — requirements documents
6. List files in `.bobr/knowledge/` — knowledge base entries

## Present summary

```
# Project Status

## Backlog
  Ready:       N items (highest priority: [title])
  In-progress: N items
  Blocked:     N items
  Done:        N items
  Total:       N items

## In Progress Right Now
  - BL-xxxx [P1] Title (assignee)

## Ready for Work (top 5)
  - BL-yyyy [P0] Title
  - BL-zzzz [P2] Title

## Blocked
  - BL-aaaa — blocked by BL-bbbb

## Requirements (N documents)
  - PRD.md
  - PRFAQ.md

## Knowledge Base (N documents)
  - research-xxx.md
  - decision-yyy.md

## Suggested Next Action
  [Based on project state, suggest what to do next:
   - If items are ready: "Pick a task with /bobr:backlog"
   - If nothing is ready but things are blocked: "Unblock BL-xxxx first"
   - If backlog is empty: "Add tasks with /bobr:backlog add or break down a feature"
   - If no requirements: "Define requirements with /bobr:requirements"]
```

Keep it concise. This is a dashboard view — give the user the big picture in one glance.
