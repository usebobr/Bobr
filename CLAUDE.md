<!-- bobr:instructions -->
# Bobr — Project Management

This project uses **Bobr** for backlog and task management.

## Golden Rule

**All tasks go through `bobr` CLI. Never browse `.bobr/` files directly — always use the CLI.**

## CLI Quick Reference

```
bobr status                          # Project overview
bobr backlog list                    # All tasks
bobr backlog ready                   # Tasks ready for work
bobr backlog show <ID>               # Task details
bobr backlog add "Title" -t feature  # Add task
bobr backlog claim <ID>              # Start working on a task
bobr backlog edit <ID> --status done # Mark task done
bobr dep list <ID>                   # Check dependencies
bobr validate                        # Validate project structure
```

## Task Lifecycle

1. **Pick a task** — `bobr backlog ready`
2. **Claim it** — `bobr backlog claim <ID>`
3. **Do the work** — implement, test, verify
4. **Mark done** — `bobr backlog edit <ID> --status done`
5. **Deliver** — commit, push, and/or create a PR

## Conventions

- Priorities: 0 = critical, 1 = high, 2 = medium, 3 = low, 4 = someday
- Statuses: open → in-progress → in-review → done (or blocked / dropped)
- Use `-o json` for programmatic parsing, `-o table` for display
<!-- bobr:instructions -->
