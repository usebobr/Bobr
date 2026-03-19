---
name: bobr-requirements
description: Requirements management — create, review, analyze, and refine project requirements
argument-hint: "[list | add <title> | show <name> | review | gaps | refine <name>]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - TodoWrite
---

# Requirements Management

Manage project requirements stored in `.bobr/requirements/`.

## Routing

Parse `$ARGUMENTS` and route:

### No arguments → Overview + suggested action

1. List all files in `.bobr/requirements/`
2. Read each file's first few lines to extract title/summary
3. Present:

```
Requirements:
  - PRD.md — [title/summary]
  - PRFAQ.md — [title/summary]
  - ...

N documents, last updated [date]

What would you like to do?

  1. Review requirements for completeness
  2. Add a new requirement document
  3. Find gaps between requirements and backlog
  4. Refine a specific document
  5. View a document
```

### `list` → List all requirements

List files in `.bobr/requirements/` with titles and last-modified dates.

### `add <title>` → Create a new requirements document

Have a conversation with the user to understand what they want to document:

1. Ask what kind of document:
```
What type of requirements document?

  1. PRD — Product Requirements Document
  2. PRFAQ — PR/FAQ format (Amazon-style)
  3. User Stories — collection of user stories
  4. Technical Requirements — non-functional requirements
  5. Free-form — custom structure
```

2. Ask the user to describe the requirements in natural language
3. Draft the document using appropriate structure
4. Write to `.bobr/requirements/<kebab-case-title>.md`
5. Show the result and ask if they want to refine it

### `show <name>` → View a document

Read and present the contents of `.bobr/requirements/<name>.md`.

If the name is ambiguous, list matching files and ask which one.

### `review` → Analyze all requirements

Launch a `bobr-requirements` agent with the prompt:
"Analyze all requirements documents in .bobr/requirements/. Check for completeness, consistency, testability, and clarity. Provide a detailed analysis report."

Present the findings and offer to act on recommendations.

### `gaps` → Gap detection

Launch a `bobr-requirements` agent with the prompt:
"Build a traceability matrix between requirements (.bobr/requirements/), backlog tasks (.bobr/backlog/), and implementation (src/). Find: requirements without tasks, tasks without requirements, implemented features without requirements."

Present the traceability matrix and gaps found.

### `refine <name>` → Refine a specific document

1. Read `.bobr/requirements/<name>.md`
2. Launch a `bobr-requirements` agent with the prompt:
   "Analyze this requirements document for ambiguities, missing acceptance criteria, untestable requirements, and missing edge cases. For each issue, suggest specific improvements."
3. Present findings one at a time, asking the user how to resolve each:

```
Issue 1 of N: [description]

Current text: "[quote]"

Suggested improvement:
  "[improved text]"

  1. Accept suggestion
  2. Modify suggestion
  3. Skip this issue
```

4. Apply approved changes to the file.

### `trace <name>` → Traceability for one document

Read the document, find related backlog items and specs, present the mapping.
