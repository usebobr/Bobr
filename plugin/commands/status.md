---
name: bobr-status
description: Show Bobr project status and backlog overview
allowed-tools:
  - Bash
  - Read
---

Show the project status using Bobr.

Run these commands and present the results to the user:

1. `uv run bobr status` — project overview
2. `uv run bobr backlog ready -o table` — items ready for work
3. `uv run bobr backlog blocked -o table` — blocked items (if any)

Present a concise summary.
