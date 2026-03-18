# Capability: Feature Development Workflow

9-phase guided workflow for implementing features from backlog — orchestrated by `/bobr:feature` command with 3 specialized agents and worktree isolation.

## ADDED Requirements

### Requirement: 9-phase orchestration
The `/bobr:feature` command SHALL guide the developer through 9 sequential phases: Discovery, Codebase Exploration, Clarifying Questions, Architecture Design, Register Change (OpenSpec), Implementation, Quality Review, Finalize, Deliver. No phase SHALL be skipped.

#### Scenario: Full workflow
- **WHEN** `/bobr:feature BL-a3f1` is invoked
- **THEN** the workflow SHALL proceed through all 9 phases in order, waiting for user approval at marked checkpoints

---

### Requirement: Input resolution (Phase 1)
The command SHALL accept 3 input modes: BL-xxxx ID (show existing item), free text (create new backlog item), or empty (present menu of ready items). After resolving, it SHALL auto-claim the item.

#### Scenario: Empty input
- **WHEN** `/bobr:feature` is called with no arguments
- **THEN** it SHALL run `bobr backlog ready` and present a numbered menu

#### Scenario: Free text input
- **WHEN** `/bobr:feature "Add user authentication"` is called
- **THEN** it SHALL create a new backlog item via `bobr backlog add` and use it

---

### Requirement: Interactive clarifying questions (Phase 3)
Questions SHALL be presented one at a time with numbered menu options. The workflow SHALL NOT proceed to architecture design until all questions are answered.

#### Scenario: Question format
- **WHEN** there are 5 ambiguities to resolve
- **THEN** questions SHALL be shown as "Question 1 of 5: [text]" with numbered options

---

### Requirement: Parallel agent usage
Phase 2 SHALL launch 2-3 `bobr-explorer` agents in parallel. Phase 4 SHALL launch 2-3 `bobr-architect` agents in parallel. Phase 7 SHALL launch 3 `bobr-reviewer` agents in parallel.

#### Scenario: Architecture design agents
- **WHEN** Phase 4 begins
- **THEN** at least 2 architect agents SHALL be launched with different focuses (minimal changes, clean architecture, pragmatic balance)

---

### Requirement: OpenSpec change registration (Phase 5)
The workflow SHALL create an OpenSpec change via `openspec new change`, create all artifacts in dependency order using `openspec instructions`, and show final status via `openspec status`.

#### Scenario: Register change
- **WHEN** user approves architecture in Phase 4
- **THEN** Phase 5 SHALL create an OpenSpec change and fill all artifacts before proceeding to implementation

---

### Requirement: Worktree-isolated implementation (Phase 6)
Implementation SHALL happen in an isolated git worktree created via `bobr worktree create`. The agent SHALL switch context using the `EnterWorktree` tool.

#### Scenario: Implementation isolation
- **WHEN** Phase 6 begins
- **THEN** a worktree SHALL be created at `.bobr/.worktrees/{BL-id}/` and all code changes SHALL happen there

---

### Requirement: OpenSpec finalization (Phase 8)
The workflow SHALL verify the change via `openspec verify` and archive via `openspec archive`, syncing delta specs to main specs.

#### Scenario: Archive change
- **WHEN** all tasks are complete and review is done
- **THEN** the OpenSpec change SHALL be verified and archived

---

### Requirement: Optional PR delivery (Phase 9)
The workflow SHALL offer to create a GitHub PR via `gh pr create` and set the backlog item to in-review status.

#### Scenario: User declines PR
- **WHEN** user chooses "No — I'll create it manually later"
- **THEN** the workflow SHALL skip PR creation but still present the final summary

---

### Requirement: Three specialized agents
The system SHALL provide 3 Bobr-aware agents: `bobr-explorer` (sonnet, yellow — codebase analysis), `bobr-architect` (opus, green — architecture design), `bobr-reviewer` (sonnet, red — code review). Each agent SHALL have Bobr-specific context baked into its system prompt.

#### Scenario: Agent Bobr awareness
- **WHEN** `bobr-explorer` analyzes the codebase
- **THEN** it SHALL know about `.bobr/` layout, specs, requirements, and knowledge directories
