---
name: bobr-feature
description: Guided feature development — 9 phases from backlog to PR with worktree isolation
argument-hint: "[BL-xxxx | feature description | (empty to see ready items)]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - TodoWrite
---

# Feature Development Workflow

You are guiding a developer through a complete feature development lifecycle using Bobr. Follow all 9 phases sequentially. Never skip phases. Wait for user approval at marked checkpoints.

## Core Principles

- **Interactive questions**: Always ask clarifying questions one at a time with numbered menu options. Never dump all questions at once.
- **Understand before acting**: Read and comprehend existing code patterns first.
- **Read files identified by agents**: After agents complete, read ALL files they list as essential.
- **Simple and elegant**: Prioritize readable, maintainable code.
- **Track progress**: Use TodoWrite throughout all phases.

---

## Phase 1: Discovery

**Goal**: Understand what needs to be built and set up tracking.

**Input resolution** — determine the backlog item:

If `$ARGUMENTS` is empty:
  1. Run `uv run bobr backlog ready -o json`
  2. Present a numbered menu of ready items: `1. BL-xxxx [P0] Title`
  3. Wait for user to pick one

If `$ARGUMENTS` matches `BL-` followed by 4 hex characters:
  1. Run `uv run bobr backlog show $ARGUMENTS -o json`
  2. Use this item

If `$ARGUMENTS` is free text:
  1. Run `uv run bobr backlog add "$ARGUMENTS" -t feature -o json`
  2. Use the newly created item

**After resolving the item:**
1. Auto-claim: `uv run bobr backlog claim <BL-ID> --assignee claude -o json`
2. Create TodoWrite list covering all 9 phases
3. Summarize: "I'll be working on: **[title]**. Here's what I understand: [summary from item body]. Confirm?"
4. Wait for user confirmation before proceeding

---

## Phase 2: Codebase Exploration

**Goal**: Understand relevant existing code and patterns at both high and low levels.

**Actions**:
1. Launch 2-3 `bobr-explorer` agents in parallel. Each agent should:
   - Trace through the code comprehensively
   - Target a different aspect of the codebase
   - Include a list of 5-10 key files to read

   Tailor prompts to the specific feature. Example prompts:
   - "Find features similar to [feature] and trace through their implementation comprehensively"
   - "Map the architecture and abstractions for [feature area], tracing through the code comprehensively"
   - "Analyze the current implementation of [existing feature/area], tracing through the code comprehensively"

2. After all agents return, read ALL files they identified as essential
3. Present a comprehensive summary of findings and patterns discovered

---

## Phase 3: Clarifying Questions

**Goal**: Fill in gaps and resolve all ambiguities before designing.

**CRITICAL**: This is one of the most important phases. DO NOT SKIP.

**Actions**:
1. Review the codebase findings and original feature request
2. Identify underspecified aspects: edge cases, error handling, integration points, scope boundaries, design preferences, backward compatibility, performance needs
3. Present questions one at a time with numbered options:

```
Question 1 of N: [question text]

  1. [Option A]
  2. [Option B]
  3. Something else (describe)

Your choice:
```

4. Wait for the user's answer before presenting the next question
5. The user can always ask to discuss a question in more detail before choosing
6. If the user says "your call" or "whatever you think is best", state your recommendation with reasoning and get explicit confirmation

**Do NOT proceed to Phase 4 until all questions are answered.**

---

## Phase 4: Architecture Design

**Goal**: Design multiple implementation approaches with different trade-offs.

**Actions**:
1. Launch 2-3 `bobr-architect` agents in parallel with different focuses:
   - Agent 1: "Minimal changes — smallest diff, maximum reuse of existing patterns"
   - Agent 2: "Clean architecture — proper abstractions, maintainability, extensibility"
   - Agent 3 (optional, for complex features): "Pragmatic balance — speed of delivery + code quality"

2. After agents return, read all files they reference
3. Consolidate approaches into a comparison:
   - Brief summary of each approach
   - Trade-offs comparison table
   - **Your recommendation with reasoning**
   - Concrete implementation differences

4. Present to user as a numbered menu:

```
Which approach do you prefer?

  1. Minimal changes — [one-line summary]
  2. Clean architecture — [one-line summary]
  3. Pragmatic balance — [one-line summary]
  4. Something else (describe)

I recommend option N because [reasoning].
```

5. **Wait for user choice before proceeding.**

---

## Phase 5: Register Change

**Goal**: Record the approved design as a Bobr change before implementation.

**DO NOT START WITHOUT USER APPROVAL OF THE ARCHITECTURE (Phase 4).**

**Actions**:
1. Create change linked to backlog item:
   ```bash
   uv run bobr change new "<item-title>" --promotes <BL-ID> -o json
   ```

2. Fast-forward to create all artifact stubs:
   ```bash
   uv run bobr change ff <CHANGE-NAME> -o json
   ```

3. Fill in the change artifacts with the chosen architecture:
   - Write `proposal.md` with the rationale and summary
   - Write `design.md` with the architecture decision, component design, and data flow
   - Write `tasks.md` with implementation checklist from the chosen architect's blueprint

4. Show summary: change ID, name, artifacts created

---

## Phase 6: Implementation

**Goal**: Build the feature in an isolated git worktree.

**DO NOT START WITHOUT USER APPROVAL.**

**Actions**:
1. Create worktree:
   ```bash
   uv run bobr worktree create <BL-ID> -o json
   ```

2. Switch to the worktree using the `EnterWorktree` tool with the worktree path from the command output

3. Read the tasks from the change's `tasks.md`

4. Implement following the chosen architecture:
   - Follow codebase conventions strictly
   - Write clean, well-documented code
   - Update TodoWrite as you progress
   - Check off tasks in `tasks.md` as they complete (`- [ ]` → `- [x]`)

5. Run tests after each logical unit:
   ```bash
   uv run pytest -x
   ```

6. Commit incrementally with descriptive messages

---

## Phase 7: Quality Review

**Goal**: Ensure code is simple, DRY, elegant, and functionally correct.

**Actions**:
1. Launch 3 `bobr-reviewer` agents in parallel with different focuses:
   - Agent 1: "Review for simplicity, DRY, and elegance — eliminate redundancy"
   - Agent 2: "Review for bugs, logic errors, edge cases, and error handling"
   - Agent 3: "Review for Bobr project conventions, CLAUDE.md rules, and test docstrings (GIVEN WHEN THEN)"

   Each agent should review `git diff main...HEAD`.

2. Consolidate findings by severity (Critical / Important)
3. Present to user:

```
Review findings:

Critical:
  - [issue description] (file:line)

Important:
  - [issue description] (file:line)

What would you like to do?

  1. Fix all issues now
  2. Fix only critical issues
  3. Proceed as-is
  4. See full details
```

4. Address issues based on user decision

---

## Phase 8: Finalize

**Goal**: Update documentation, verify and archive the change.

**Actions**:
1. Ask user: "Did this feature introduce any new conventions that should be documented in CLAUDE.md?"
   - If yes, update `plugin/CLAUDE.md` with the new conventions

2. Verify all tasks are complete:
   ```bash
   uv run bobr change verify <CHANGE-NAME> -o json
   ```

3. Archive the change (syncs delta specs to main specs):
   ```bash
   uv run bobr change archive <CHANGE-NAME> -o json
   ```

4. Mark all TodoWrite items complete

---

## Phase 9: Deliver

**Goal**: Push code and optionally create a PR.

**Actions**:
1. Push the feature branch:
   ```bash
   git push -u origin <BRANCH-NAME>
   ```

2. Set backlog item to in-review:
   ```bash
   uv run bobr backlog edit <BL-ID> --status in-review -o json
   ```

3. Offer to create a PR:

```
Create a pull request?

  1. Yes — create PR now
  2. No — I'll create it manually later
```

4. If yes:
   ```bash
   gh pr create --title "feat: <item-title> (BL-ID)" --body "$(cat <<'EOF'
   ## Summary
   <summary from proposal.md>

   ## Changes
   <list of key files changed>

   Promotes: BL-ID
   Change: CH-xxxx

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

5. Present final summary:
   - What was built
   - Key decisions made
   - Files changed
   - PR link (if created)
   - Branch name
   - Next steps: "After PR is merged, run `uv run bobr worktree clean <BL-ID>` to clean up the worktree and `uv run bobr backlog edit <BL-ID> --status done` to close the task."
