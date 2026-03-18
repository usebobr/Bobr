# Research: Backlog.md

**Дата**: 2026-03-18
**Источник**: https://github.com/MrLesk/Backlog.md
**Автор**: Alex Gavrilescu (MrLesk)

## Обзор

Backlog.md — markdown-native task manager и Kanban-визуализатор для Git-репозиториев. Каждая задача — отдельный `.md` файл. Ориентирован на spec-driven AI development.

## Архитектура

### Tech Stack
- **Runtime**: Bun + TypeScript 5
- **Formatting**: Biome
- **UI**: React + Tailwind (web interface)
- **MCP SDK**: `@modelcontextprotocol/sdk`
- **Search**: fuse.js (fuzzy search)
- **Markdown**: gray-matter (frontmatter parsing)
- **TUI**: neo-bblessed (terminal Kanban board)
- **Distribution**: npm global package, Homebrew, Nix

### Структура задач
```
backlog/
├── task-10 - Add core search functionality.md
├── task-11 - Implement user auth.md
└── ...
```

Каждая задача — markdown файл с YAML frontmatter + описание + acceptance criteria.

### Структура исходников
```
src/
├── cli.ts              # Entry point
├── commands/           # CLI commands
├── core/               # Бизнес-логика
├── mcp/                # MCP server
├── server/             # Web server
├── web/                # React web UI
├── markdown/           # Markdown парсинг
├── git/                # Git интеграция
├── formatters/         # Форматирование вывода
├── board.ts            # Terminal Kanban
├── agent-instructions.ts  # Инструкции для агентов
└── types/              # TypeScript типы
```

## Ключевые фичи

1. **Terminal Kanban board** — `backlog board` рисует Kanban в терминале
2. **Web interface** — `backlog browser` запускает React UI с drag-and-drop
3. **Board export** — экспорт доски в markdown
4. **Fuzzy search** — `backlog search` по задачам, docs, decisions
5. **MCP server** — `backlog mcp start` для интеграции с AI
6. **Multi-AI support** — Claude Code, Gemini CLI, Codex, Kiro, Cursor
7. **Definition of Done** — переиспользуемые чеклисты для задач
8. **Acceptance criteria** — интерактивный редактор чеклистов

## AI Workflow (Spec-Driven)

Рекомендуемый flow:
1. Описать идею агенту → агент разбивает на задачи
2. Одна задача = одна сессия агента = один PR
3. Перед кодом: агент пишет implementation plan в задаче
4. Реализация + верификация
5. Review checkpoint после каждого шага

## MCP Integration

```bash
claude mcp add backlog --scope user -- backlog mcp start
```

MCP resources:
- `backlog://workflow/overview` — общий обзор workflow
- Workflow guides загружаются динамически

CLAUDE.md содержит `<CRITICAL_INSTRUCTION>` для принуждения агента читать workflow overview.

## CLAUDE.md паттерны

### Agent POV секция
> "Treat Backlog.md as a shipped CLI/MCP binary that may be used from other repositories where agents cannot inspect this source tree."

### Simplicity-first rules
- Prefer single implementation for similar concerns
- Keep APIs minimal (load + upsert > load/save/update)
- Avoid extra layers unless proven need
- Keep behavior consistent across similar stores

## Выводы для Bobr

- **Markdown-native** — каждая задача как файл — human-readable, git-friendly
- **Web + Terminal** — два интерфейса для визуализации (Kanban)
- **MCP resources** — динамические гайды через MCP resources (не только tools)
- **Spec-driven AI workflow** — один PR на задачу, plan → implement → verify
- **Agent instructions** — отдельный модуль для генерации инструкций AI-агентам
- **`<CRITICAL_INSTRUCTION>`** — принуждение агента читать documentation upfront
- **Bun + TypeScript** — современный стек, быстрая сборка, native binaries
- **Fuzzy search** — fuse.js для поиска по задачам
- **Version 1.35.7** — зрелый продукт с активной разработкой
