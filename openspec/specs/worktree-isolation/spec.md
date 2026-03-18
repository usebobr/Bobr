# Capability: Worktree Isolation

Git worktree management for feature development — each backlog item gets an isolated working copy with its own branch.

## ADDED Requirements

### Requirement: Worktree creation
The system SHALL create a git worktree at `.bobr/.worktrees/{BL-id}/` with branch `feature/{BL-id}-{slug}` when `bobr worktree create <BL-ID>` is called. The slug SHALL be derived from the backlog item's title. If the branch already exists, it SHALL be checked out; otherwise a new branch SHALL be created.

#### Scenario: Create new worktree
- **WHEN** `bobr worktree create BL-a3f1 -o json` is called for item "Fix login bug"
- **THEN** a worktree SHALL be created at `.bobr/.worktrees/BL-a3f1/` on branch `feature/BL-a3f1-fix-login-bug` and a `worktree.md` record SHALL be written

#### Scenario: Existing branch
- **WHEN** branch `feature/BL-a3f1-fix-login-bug` already exists in git
- **THEN** the worktree SHALL check out that existing branch instead of creating a new one

---

### Requirement: Idempotent creation
The system SHALL be idempotent: if a worktree already exists for the given item (worktree.md present), it SHALL return the existing record without error.

#### Scenario: Double create
- **WHEN** `bobr worktree create BL-a3f1` is called twice
- **THEN** the second call SHALL return the same branch and path as the first

---

### Requirement: Worktree record
Each worktree SHALL have a `worktree.md` file with YAML frontmatter containing: `item_id`, `branch`, `created` (ISO timestamp). This record SHALL be written atomically — if writing fails, the git worktree SHALL be rolled back (removed).

#### Scenario: Write failure rollback
- **WHEN** write_record fails after git worktree is created
- **THEN** the git worktree SHALL be removed via `git worktree remove --force`

---

### Requirement: Worktree cleanup
The system SHALL provide `bobr worktree clean <BL-ID>` to remove a worktree and its git worktree entry. It SHALL support `-o json` output.

#### Scenario: Clean existing worktree
- **WHEN** `bobr worktree clean BL-a3f1` is called
- **THEN** the worktree directory and git worktree registration SHALL be removed

---

### Requirement: Worktree listing
The system SHALL provide `bobr worktree list` to show all active worktrees with item_id, branch, and path. Corrupt worktree records SHALL be skipped with a warning. Supports `-o json`.

#### Scenario: List with corrupt record
- **WHEN** a worktree.md file is malformed
- **THEN** it SHALL be skipped with a stderr warning, not crash the listing
