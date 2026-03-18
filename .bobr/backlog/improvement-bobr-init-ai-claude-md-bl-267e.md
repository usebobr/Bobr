---
area:
- cli
- onboarding
assignee: human
created: '2026-03-18T18:08:39.832355+00:00'
id: BL-267e
priority: 1
status: done
title: 'bobr init: генерировать AI-инструкции в CLAUDE.md проекта'
type: improvement
updated: '2026-03-18T18:11:49.021961+00:00'
---

## Проблема

При инициализации проекта через `bobr init` не создаётся CLAUDE.md с инструкциями для AI-агентов. В результате агент, попадая в проект с bobr, не знает о его существовании и начинает вручную бродить по файлам `.bobr/` вместо использования CLI/MCP.

## Решение

`bobr init` должен генерировать CLAUDE.md (или дополнять существующий) с секцией инструкций для AI-агентов, аналогичной `plugin/CLAUDE.md`:
- Golden Rule: все задачи через `bobr` CLI или MCP
- Основные команды: status, backlog list/add/claim/edit, worktree
- Task lifecycle
- Conventions (приоритеты, статусы, форматы вывода)

## Acceptance Criteria

- [ ] `bobr init` создаёт CLAUDE.md в корне проекта, если его нет
- [ ] Если CLAUDE.md уже существует — добавляет секцию Bobr, не затирая существующий контент
- [ ] Сгенерированные инструкции содержат: Golden Rule, CLI reference, task lifecycle, conventions
- [ ] Инструкции адаптируются к контексту проекта (путь к bobr, наличие MCP)
- [ ] Существующие проекты могут обновить инструкции повторным запуском `bobr init`

## Контекст

Обнаружено при dogfooding: AI-агент разрабатывал Bobr, но не использовал bobr CLI для просмотра бэклога — пошёл через ls по файлам, потому что нигде не было инструкции использовать CLI.
