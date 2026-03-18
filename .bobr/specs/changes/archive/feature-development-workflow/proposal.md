---
created: '2026-03-18T16:45:47.137103+00:00'
id: CH-69ea
name: feature-development-workflow
promotes: BL-71cd
status: archived
title: Feature Development Workflow
updated: '2026-03-18T17:00:58.225394+00:00'
---

## Summary

Add `/bobr:feature` slash command — a 9-phase guided workflow for feature development,
with 3 specialized agents (bobr-explorer, bobr-architect, bobr-reviewer) and git worktree
isolation per feature.

## Motivation

Bobr manages backlog and specs but lacks a structured workflow for developing features.
The reference feature-dev plugin provides a good foundation, but Bobr needs its own
version with deeper integration: auto-claim, worktree isolation, change management,
interactive clarifying questions, and Bobr-aware agents.

## Scope

- Plugin command: `plugin/commands/feature.md`
- 3 agents: `plugin/agents/bobr-{explorer,architect,reviewer}.md`
- Worktree CLI: `bobr worktree create/clean/list`
- Core worktree model: `WorktreeRecord` dataclass
- Integration: BobrPaths extension, main.py registration
