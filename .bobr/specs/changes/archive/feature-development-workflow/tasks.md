## 1. Core: Worktree model and paths

- [x] 1.1 Add `worktrees` path to `BobrPaths` in `src/bobr/core/repo.py`
- [x] 1.2 Create `WorktreeRecord` dataclass in `src/bobr/core/worktree.py`

## 2. CLI: Worktree commands

- [x] 2.1 Create `src/bobr/cli/worktree.py` with `create`, `clean`, `list` commands
- [x] 2.2 Register `worktree_app` in `src/bobr/cli/main.py`
- [x] 2.3 Add `Bash(uv run bobr worktree *)` to auto-permissions in `main.py`

## 3. Plugin: Agents

- [x] 3.1 Create `plugin/agents/bobr-explorer.md` (sonnet, yellow)
- [x] 3.2 Create `plugin/agents/bobr-architect.md` (opus, green)
- [x] 3.3 Create `plugin/agents/bobr-reviewer.md` (sonnet, red)

## 4. Plugin: Feature command

- [x] 4.1 Create `plugin/commands/feature.md` with 9-phase workflow

## 5. Integration

- [x] 5.1 Add `.bobr/.worktrees/` to `.gitignore`
- [x] 5.2 Update `plugin/CLAUDE.md` with feature workflow documentation

## 6. Tests

- [x] 6.1 Tests for `WorktreeRecord` YAML round-trip
- [x] 6.2 Tests for `bobr worktree create` (branch + directory creation)
- [x] 6.3 Tests for `bobr worktree clean` (removal)
- [x] 6.4 Tests for `bobr worktree list`
