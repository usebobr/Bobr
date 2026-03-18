---
name: bobr-claim
description: Claim a backlog item and start working on it
argument-hint: <ITEM_ID>
allowed-tools:
  - Bash
---

Claim a backlog item for work.

If $ARGUMENTS is provided:
  Run: `uv run bobr backlog claim $ARGUMENTS -o json`

If no argument:
  1. Run `uv run bobr backlog ready -o json` to show available items
  2. Ask the user which item to claim
