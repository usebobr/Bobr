## Context

9-phase feature development workflow for Bobr with worktree isolation.

## Goals / Non-Goals

**Goals:**
- `/bobr:feature` command orchestrating 9 phases from discovery to PR
- 3 Bobr-aware agents (explorer/sonnet, architect/opus, reviewer/sonnet)
- Git worktree per feature at `.bobr/.worktrees/{BL-id}/`
- `bobr worktree create/clean/list` CLI commands
- Interactive clarifying questions (one at a time, numbered menu)
- Auto-claim on start, in-review on PR

**Non-Goals:**
- MCP tools for worktree operations (CLI sufficient)
- Modifying `Change` model (worktree path is deterministic)
- Parallel feature orchestration within one session

## Decisions

### Architecture: Layered plugin with CLI backend
- Command (markdown) owns orchestration and user interaction
- Agents (markdown) are analytical — read-only, no state mutations
- CLI (Python) handles worktree lifecycle — testable, reusable
- All state mutations via `bobr` CLI or `gh` CLI

### Worktree strategy
- Path: `.bobr/.worktrees/{BL-id}/` (inside project, gitignored)
- Branch: `feature/{BL-id}-{slug}` (git-flow style)
- Lifecycle: create on Phase 6, cleanup after merge or manual `bobr worktree clean`
- Agent switches context via `EnterWorktree` tool
- `.bobr/.worktrees/` added to `.gitignore`

### WorktreeRecord storage
- YAML frontmatter in `.bobr/.worktrees/{BL-id}/worktree.md` (consistent with Bobr patterns)
- Fields: item_id, branch, created
- Not JSON — everything in Bobr uses YAML frontmatter

### Agent design
- Own agents (`bobr-*`), not reusing `code-*` from feature-dev
- Bobr-specific context baked into system prompts
- bobr-explorer: knows `.bobr/` layout, specs, requirements
- bobr-architect: knows Typer conventions, BobrPaths, model patterns, outputs tasks.md format
- bobr-reviewer: knows CLAUDE.md golden rule, GIVEN/WHEN/THEN test docstrings

### 9 Phases
1. Discovery — resolve input (BL-id / text / empty → ready items menu)
2. Codebase Exploration — 2-3 bobr-explorer agents parallel
3. Clarifying Questions — interactive, one at a time with numbered options
4. Architecture Design — 2-3 bobr-architect agents parallel
5. Register Change — `bobr change new` + `bobr change ff` + fill artifacts
6. Implementation — `bobr worktree create`, EnterWorktree, implement
7. Quality Review — 3 bobr-reviewer agents parallel
8. Finalize — update CLAUDE.md, verify + archive change
9. Deliver — optional PR, set in-review

### Input resolution
- `BL-xxxx` → `bobr backlog show`, use existing item
- Free text → `bobr backlog add`, create new item
- Empty → `bobr backlog ready`, numbered menu to pick

### Spec registration uses Bobr change system
- `bobr change new "<title>" --promotes BL-xxxx`
- `bobr change ff <name>` to create all artifacts
- Fill proposal.md with rationale, tasks.md with implementation checklist
- `bobr change verify` + `bobr change archive` in Phase 8
