---
name: bobr-init
description: Initialize Bobr in a project — creates .bobr/ structure and configures Claude Code integration
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
---

# Initialize Bobr

Set up Bobr project management in the current repository.

## Steps

### 1. Create .bobr/ structure

Run: `uv run bobr init`

This creates the base directory structure:
- `.bobr/backlog/` — task files
- `.bobr/requirements/` — requirements documents
- `.bobr/knowledge/` — knowledge base
- `.bobr/config.yaml` — project configuration

### 2. Set up Claude Code integration

Check if `.claude/` directory exists. If not, guide the user through setup.

**CLAUDE.md**: Check if a project CLAUDE.md exists. If not, create one with Bobr conventions:
- Golden rule: use bobr CLI for tasks
- Link to available skills: `/bobr:feature`, `/bobr:backlog`, `/bobr:requirements`, `/bobr:knowledge`, `/bobr:status`
- Data structure overview
- Task lifecycle

**Plugin registration**: Check if the Bobr plugin is registered. Show the user how to add it if not:
```
claude plugin add /path/to/bobr/plugin
```

### 3. Create initial requirements document (optional)

Ask the user:
```
Would you like to create an initial requirements document?

  1. Yes — I'll describe the project and we'll draft a PRD
  2. No — I'll add requirements later
```

If yes, have a conversation to understand the project and create `.bobr/requirements/PRD.md`.

### 4. Summary

Present what was created:
- List of directories and files created
- Available skills they can now use
- Suggested next step: `/bobr:feature` to start building, or `/bobr:requirements` to define requirements first
