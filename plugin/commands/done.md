---
name: bobr-done
description: Mark a backlog item as done
argument-hint: <ITEM_ID>
allowed-tools:
  - Bash
---

Mark a backlog item as completed.

If $ARGUMENTS is provided:
  Run: `uv run bobr backlog edit $ARGUMENTS --status done -o json`

If no argument:
  1. Run `uv run bobr backlog list --status in-progress -o json` to show in-progress items
  2. Ask the user which item to mark as done
