# Capability: Project Bootstrap

Project initialization and status — `bobr init` scaffolds the `.bobr/` directory structure, `bobr status` shows project overview, `bobr validate` checks integrity.

## ADDED Requirements

### Requirement: Project initialization
`bobr init [PATH]` SHALL create the `.bobr/` directory structure with subdirectories: `backlog/`, `requirements/`, `specs/`, `knowledge/`, `.cache/`. It SHALL be idempotent — running on an existing project SHALL not destroy data.

#### Scenario: Init new project
- **WHEN** `bobr init /path/to/project` is called in a directory without `.bobr/`
- **THEN** the `.bobr/` structure SHALL be created with all required subdirectories

#### Scenario: Init existing project
- **WHEN** `bobr init` is called in a directory that already has `.bobr/`
- **THEN** existing data SHALL be preserved, missing subdirectories SHALL be created

---

### Requirement: Project root discovery
The system SHALL find the project root by walking up from the current directory looking for `.bobr/`. All CLI commands SHALL use this discovery mechanism.

#### Scenario: Nested directory
- **WHEN** a bobr command is run from `src/bobr/cli/`
- **THEN** it SHALL find the project root at the ancestor directory containing `.bobr/`

#### Scenario: No project found
- **WHEN** no `.bobr/` directory exists in any ancestor
- **THEN** the command SHALL fail with an appropriate error

---

### Requirement: Project status
`bobr status` SHALL display a summary of the project: total items by status, items by priority, recent activity. It SHALL support `-o json` output.

#### Scenario: Status overview
- **WHEN** `bobr status -o json` is called
- **THEN** output SHALL include counts grouped by status and priority

---

### Requirement: Project validation
`bobr validate` SHALL check project integrity: valid frontmatter in all items, valid dependency references (no dangling IDs), valid enum values for status/type/priority.

#### Scenario: Dangling dependency
- **WHEN** item BL-a references non-existent BL-z in depends_on
- **THEN** `bobr validate` SHALL report the dangling reference as an error
