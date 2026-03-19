---
name: bobr-knowledge
description: Knowledge base management — record research, decisions, meeting notes, and search project knowledge
argument-hint: "[list | add <title> | show <name> | search <query>]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Knowledge Base Management

Manage the project knowledge base stored in `.bobr/knowledge/`.

## Routing

Parse `$ARGUMENTS` and route:

### No arguments → Overview

1. List all files in `.bobr/knowledge/`
2. Group by type prefix (research-, decision-, meeting-, etc.)
3. Present:

```
Knowledge Base: N documents

  Research (N):
    - research-backlog-md.md — [first line summary]
    - research-openspec.md — [first line summary]

  Decisions (N):
    - decision-xyz.md — [first line summary]

  Other (N):
    - ...

What would you like to do?

  1. Record new knowledge
  2. Search knowledge base
  3. View a document
```

### `list` → List all knowledge documents

List files in `.bobr/knowledge/` grouped by type with summaries.

### `add <title>` → Record new knowledge

1. Determine the type from context or ask:
```
What type of knowledge?

  1. Research — findings from investigation
  2. Decision — architectural or product decision (ADR-style)
  3. Meeting — meeting notes or discussion summary
  4. Convention — coding convention or project rule
  5. Other
```

2. Ask the user to describe the knowledge, or paste content
3. Structure it appropriately:

**Research format:**
```markdown
# Research: [Title]

**Date**: YYYY-MM-DD
**Source**: [URL or context]

## Summary
[key findings]

## Details
[full content]

## Implications for Bobr
[how this affects the project]
```

**Decision format (ADR):**
```markdown
# Decision: [Title]

**Date**: YYYY-MM-DD
**Status**: Accepted | Superseded | Deprecated

## Context
[what prompted this decision]

## Decision
[what we decided]

## Consequences
[positive and negative implications]
```

**Meeting format:**
```markdown
# Meeting: [Title]

**Date**: YYYY-MM-DD
**Participants**: [who]

## Summary
[key outcomes]

## Action Items
- [ ] [action] — [owner]
```

4. Write to `.bobr/knowledge/<type>-<kebab-case-title>.md`

### `show <name>` → View a document

Read and present `.bobr/knowledge/<name>.md`.

If ambiguous, show matching files and ask which one.

### `search <query>` → Search knowledge base

1. Search `.bobr/knowledge/` for the query using grep
2. Also search `.bobr/requirements/` as it may contain relevant context
3. Present matching documents with relevant excerpts
4. If no results, suggest broadening the search terms
