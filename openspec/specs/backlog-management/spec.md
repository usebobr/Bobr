# Capability: Backlog Management

Core task tracking system for Bobr — CRUD operations on backlog items stored as YAML frontmatter markdown files with SQLite cache for fast queries.

## ADDED Requirements

### Requirement: Backlog item model
The system SHALL represent each backlog item as a markdown file with YAML frontmatter containing: `id` (BL-xxxx hash), `title`, `type` (feature/bug/idea/improvement), `status` (open/in-progress/in-review/done/blocked/dropped), `priority` (0-4, 0=highest), `area` (list), `epic` (optional slug), `depends_on` (list of BL-ids), `blocks` (list of BL-ids), `assignee` (optional), `created` and `updated` (ISO timestamps). The markdown body MAY contain free-text description.

#### Scenario: Create item with defaults
- **WHEN** `bobr backlog add "Fix login bug" -t bug` is called
- **THEN** a file SHALL be created at `.bobr/backlog/bug-fix-login-bug.md` with status=open, priority=2, and a BL-xxxx hash ID

#### Scenario: ID collision
- **WHEN** two items produce the same 4-hex hash
- **THEN** the system SHALL rehash with the ID appended until unique

---

### Requirement: Item CRUD via CLI
The system SHALL provide CLI commands: `add` (create), `show` (read with body and deps), `edit` (update any field), `drop` (set status=dropped), `list` (query with filters). All commands SHALL support `-o json` and `-o table` output formats.

#### Scenario: Edit multiple fields
- **WHEN** `bobr backlog edit BL-a3f1 --status done --priority 0` is called
- **THEN** both status and priority SHALL be updated atomically

#### Scenario: List with filters
- **WHEN** `bobr backlog list --status open --priority 1 -o json` is called
- **THEN** only items matching both filters SHALL be returned as JSON array

---

### Requirement: Claim workflow
The system SHALL provide a `claim` command that atomically sets status=in-progress and assigns the item. Only items with status `open` or `in-review` SHALL be claimable. Attempting to claim an item in any other status SHALL fail with an error.

#### Scenario: Claim open item
- **WHEN** `bobr backlog claim BL-a3f1 --assignee claude` is called on an open item
- **THEN** status SHALL become `in-progress` and assignee SHALL be `claude`

#### Scenario: Claim in-progress item fails
- **WHEN** `bobr backlog claim BL-a3f1` is called on an in-progress item
- **THEN** the command SHALL exit with error "cannot be claimed"

---

### Requirement: Ready items query
The system SHALL provide a `ready` command that returns items with status=open and no unresolved blocking dependencies (all items in `depends_on` must have status=done or dropped).

#### Scenario: Item blocked by open dependency
- **WHEN** BL-a depends on BL-b and BL-b is status=open
- **THEN** BL-a SHALL NOT appear in `bobr backlog ready` output

#### Scenario: Item with all deps done
- **WHEN** BL-a depends on BL-b and BL-b is status=done
- **THEN** BL-a SHALL appear in `bobr backlog ready` output

---

### Requirement: Blocked items query
The system SHALL provide a `blocked` command that returns items with unresolved blocking dependencies, showing which items block each one.

#### Scenario: Show blockers
- **WHEN** BL-a depends on open BL-b and BL-c
- **THEN** `bobr backlog blocked` SHALL show BL-a with blockers BL-b, BL-c

---

### Requirement: SQLite cache
The system SHALL maintain a SQLite cache at `.bobr/.cache/bobr.db` that mirrors backlog items for fast queries. The cache SHALL sync from markdown files on each command invocation. The cache is ephemeral and can be rebuilt from the markdown source of truth.

#### Scenario: Cache rebuild
- **WHEN** the cache database is deleted and any backlog command is run
- **THEN** the cache SHALL be rebuilt from `.bobr/backlog/` files transparently
