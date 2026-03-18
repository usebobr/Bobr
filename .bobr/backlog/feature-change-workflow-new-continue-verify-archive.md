---
area:
- cli
- core
assignee: claude-code
blocks:
- BL-0b36
- BL-874b
created: '2026-03-18T10:39:56.243595+00:00'
depends_on:
- BL-83e4
id: BL-99cf
priority: 1
status: done
title: 'Change workflow: new, continue, verify, archive + delta spec sync'
type: feature
updated: '2026-03-18T11:43:02.963710+00:00'
---

## Scope

Change lifecycle: `bobr change new` → `continue` → `ff` → `verify` → `archive`.

Archive должен мержить delta specs в основные спецификации (`specs/<name>/spec.md`).
Change ссылается на backlog item через `promotes: BL-xxxx`.
