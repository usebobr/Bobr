---
name: bobr-ready
description: Show backlog items ready for work (no blockers)
argument-hint: "[filter]"
allowed-tools:
  - Bash
---

Show items ready for work.

Run: `uv run bobr backlog ready -o table`

If $ARGUMENTS is provided, filter or search within the results.
