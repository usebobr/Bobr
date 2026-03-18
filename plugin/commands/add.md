---
name: bobr-add
description: Add a new backlog item
argument-hint: <title> [--type TYPE] [--priority P] [--area AREAS]
allowed-tools:
  - Bash
---

Add a new item to the backlog.

If $ARGUMENTS is provided:
  Run: `uv run bobr backlog add $ARGUMENTS -o json`

If no arguments:
  Ask the user for:
  - Title (required)
  - Type: feature / bug / idea / improvement (default: feature)
  - Priority: 0-4 (default: 2)
  - Area (optional)
  Then run the command with the provided values.
