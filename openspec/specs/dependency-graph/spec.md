# Capability: Dependency Graph

Bidirectional dependency tracking between backlog items — stored in the items themselves, cached in SQLite for blocking/ready queries.

## ADDED Requirements

### Requirement: Bidirectional dependency storage
The system SHALL store dependencies in both directions: the dependent item's `depends_on` list and the dependency's `blocks` list. Adding a dependency SHALL update both files atomically.

#### Scenario: Add dependency
- **WHEN** `bobr dep add BL-a3f1 BL-b2c3` is called
- **THEN** BL-a3f1's `depends_on` SHALL include BL-b2c3 AND BL-b2c3's `blocks` SHALL include BL-a3f1

#### Scenario: Self-dependency rejected
- **WHEN** `bobr dep add BL-a3f1 BL-a3f1` is called
- **THEN** the command SHALL fail with "Cannot depend on self"

---

### Requirement: Dependency removal
The system SHALL provide `dep remove` to remove a dependency, updating both files (removing from `depends_on` and `blocks`).

#### Scenario: Remove dependency
- **WHEN** `bobr dep remove BL-a3f1 BL-b2c3` is called
- **THEN** BL-a3f1's `depends_on` SHALL no longer include BL-b2c3 AND BL-b2c3's `blocks` SHALL no longer include BL-a3f1

---

### Requirement: Dependency listing
The system SHALL provide `dep list` showing both `depends_on` and `blocks` for a given item, with `-o json` support.

#### Scenario: List deps JSON
- **WHEN** `bobr dep list BL-a3f1 -o json` is called
- **THEN** output SHALL be JSON with `depends_on` and `blocks` arrays
