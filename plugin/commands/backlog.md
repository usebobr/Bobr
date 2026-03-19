---
name: bobr-backlog
description: Unified backlog management — list, add, claim, complete tasks, or groom the backlog
argument-hint: "[list | ready | add <title> | claim <ID> | done <ID> | show <ID> | groom | breakdown <description>]"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - TodoWrite
---

# Backlog Management

Unified entry point for all backlog operations. Routes to the appropriate action based on arguments.

## Routing

Parse `$ARGUMENTS` and route:

### No arguments → Interactive menu

Show a quick status and menu:

1. Run `uv run bobr backlog ready -o json` and `uv run bobr backlog list --status in-progress -o json`
2. Present:

```
Backlog Overview:
  Ready: N items | In-progress: N items | Total: N items

In-progress right now:
  - BL-xxxx [P1] Title (assignee)

Ready for work:
  - BL-yyyy [P0] Title
  - BL-zzzz [P2] Title

What would you like to do?

  1. Pick a task to work on
  2. Add a new task
  3. Mark a task as done
  4. Show task details
  5. Groom the backlog
  6. Break down a feature
```

### `list` → List all items

Run: `uv run bobr backlog list -o table`

If followed by filters (e.g., `list --status open --priority 1`), pass them through.

### `ready` → Show ready items

Run: `uv run bobr backlog ready -o table`

### `add <title>` → Add a new task

If just a title: `uv run bobr backlog add "<title>" -o json`

If additional flags provided, pass them through:
`uv run bobr backlog add "<title>" -t TYPE -p PRIORITY -a "areas" -o json`

If no title provided, ask interactively:
- Title (required)
- Type: feature / bug / idea / improvement (default: feature)
- Priority: 0-4 (default: 2)
- Area (optional)

### `claim <ID>` → Claim a task

Run: `uv run bobr backlog claim <ID> -o json`

If no ID, show ready items and let user pick.

### `done <ID>` → Mark task done

Run: `uv run bobr backlog edit <ID> --status done -o json`

If no ID, show in-progress items and let user pick.

### `show <ID>` → Show task details

Run: `uv run bobr backlog show <ID> -o json`

Also show dependencies: `uv run bobr dep list <ID> -o json`

### `blocked` → Show blocked items

Run: `uv run bobr backlog blocked -o table`

### `groom` → Backlog grooming

Launch a `bobr-backlog` agent with the prompt:
"Analyze the current backlog. Look for duplicates, stale items, missing dependencies, priority mismatches, and scope issues. Provide a grooming report with specific recommendations."

Present the agent's findings and ask the user which recommendations to apply. Execute approved changes via `bobr` CLI.

### `breakdown <description>` → Break down a feature

Launch a `bobr-backlog` agent with the prompt:
"Break down this feature into concrete, implementable tasks: <description>. Analyze the codebase to understand what exists and what needs to change. Define dependencies between tasks."

Present the breakdown and ask:
```
Create these tasks in the backlog?

  1. Yes — create all tasks with suggested priorities
  2. Let me adjust first — show me the list to edit
  3. No — just informational
```

If yes, run `uv run bobr backlog add "..." -t feature -p N -o json` for each task, then add dependencies with `uv run bobr dep add FROM TO`.

### `edit <ID> [flags]` → Edit a task

Run: `uv run bobr backlog edit <ID> $FLAGS -o json`

### `drop <ID>` → Drop a task

Confirm first: "Drop BL-xxxx '[title]'? This sets status to 'dropped'."

Run: `uv run bobr backlog edit <ID> --status dropped -o json`
