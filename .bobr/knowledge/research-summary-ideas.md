# Обобщение исследований: Идеи для Bobr

**Дата**: 2026-03-18
**Источники**: feature-dev, code-simplifier, OpenSpec, Taskmaster, Backlog.md, CCPM

## Сравнительная таблица

| Аспект | Bobr | Taskmaster | Backlog.md | OpenSpec | CCPM |
|--------|------|-----------|------------|---------|------|
| Хранение | Markdown + YAML frontmatter | JSON (tasks.json) | Markdown файлы | Markdown артефакты | Markdown (.pm/) |
| CLI | Python (Click) | Node.js | Bun/TypeScript | Node.js | Python scripts |
| MCP | Да (3 tools) | Да (7-42 tools, tiered) | Да (full) | Нет (CLI only) | Нет |
| AI-генерация | Нет | PRD → tasks, complexity | Агент разбивает идеи | Artifact instructions | Делегация субагентам |
| Web UI | Нет | Нет | Да (React Kanban) | Нет | Нет |
| Deps | Да (граф) | Да (числовые) | Нет | Да (артефакты) | Нет |
| Workflow | Open → Done | Pending → Done | To Do → Done | New → Archive | Think → Document → Delegate |
| Плагин CC | Да (commands) | Да (commands + agents) | MCP + CLAUDE.md | Commands (opsx/) | CLAUDE.md template |

## Топ идеи для реализации в Bobr

### 1. Tiered MCP Tools (из Taskmaster)
**Приоритет: ВЫСОКИЙ**

Сейчас у Bobr 3 MCP tools. При росте — делать tiered loading:
- `core` (3-7) — ежедневный минимум
- `standard` (10-15) — полное управление
- `all` (20+) — research, automation, AI features

Конфигурируется через env: `BOBR_TOOLS=core|standard|all`

### 2. PRD → Tasks AI-генерация (из Taskmaster)
**Приоритет: ВЫСОКИЙ**

```bash
bobr generate-tasks --from requirements/prd.md
```
AI читает PRD/требования и создаёт задачи в бэклоге с:
- Описанием, приоритетом, зависимостями
- testStrategy для каждой задачи
- Complexity analysis

### 3. Structured Change Workflow (из OpenSpec)
**Приоритет: ВЫСОКИЙ**

Bobr уже имеет change workflow, но можно усилить:
- **Schema-driven** — разные pipelines для разных типов changes
- **Artifact instructions** — шаблоны и инструкции для каждого артефакта
- **Verify перед archive** — формальная верификация (completeness/correctness/coherence)
- **Delta specs** — изменения как delta, синхронизация в main specs

### 4. Claude Code Plugin с агентами (из feature-dev)
**Приоритет: ВЫСОКИЙ**

Расширить plugin Bobr специализированными агентами:
- **bobr-explorer** — исследование бэклога, зависимостей, контекста
- **bobr-planner** — декомпозиция фич на задачи
- **bobr-reviewer** — ревью реализации против спеков

Workflow `/bobr:feature`:
1. Discovery → 2. Explore → 3. Clarify → 4. Plan → 5. Implement → 6. Review → 7. Done

### 5. MISTAKES.md / Anti-patterns (из CCPM)
**Приоритет: СРЕДНИЙ**

```
.bobr/
└── mistakes.md    # Паттерны ошибок, проверяемые перед каждой задачей
```

Loop prevention: счётчик попыток, эскалация после 3 неудач.
Агент проверяет mistakes.md перед началом работы.

### 6. Terminal Kanban Board (из Backlog.md)
**Приоритет: СРЕДНИЙ**

```bash
bobr board
```
Визуализация бэклога как Kanban-доска в терминале.
Библиотеки: rich (Python), blessed (Node).

### 7. Context Preservation Hooks (из CCPM)
**Приоритет: СРЕДНИЙ**

Hooks для Claude Code:
- `PreCompact` — экспорт контекста проекта перед компактификацией
- `SessionStart` — восстановление контекста
- `SubagentStop` — логирование результатов субагентов

### 8. MCP Resources (из Backlog.md)
**Приоритет: СРЕДНИЙ**

Помимо MCP tools, добавить MCP resources:
- `bobr://workflow/overview` — гайд по workflow
- `bobr://backlog/ready` — задачи готовые к работе
- `bobr://status` — статус проекта

Resources загружаются агентом по необходимости, экономя контекст.

### 9. Web Interface (из Backlog.md)
**Приоритет: НИЗКИЙ**

```bash
bobr browser
```
React/Svelte Kanban board с:
- Drag-and-drop
- Редактирование задач
- Граф зависимостей
- Real-time sync с markdown файлами

### 10. Complexity Analysis (из Taskmaster)
**Приоритет: НИЗКИЙ**

```bash
bobr analyze-complexity [--from BL-xxxx] [--to BL-yyyy]
```
AI оценивает сложность задач, рекомендует декомпозицию.

## Архитектурные принципы (заимствованные)

### Из feature-dev
- Параллельные агенты для разных аспектов
- Human-in-the-loop на ключевых решениях
- Agents возвращают "файлы для чтения" → основной агент читает

### Из OpenSpec
- Артефакт-ориентированный workflow
- CLI как backend, slash-commands как frontend
- Verify → Archive lifecycle

### Из Taskmaster
- Tiered tool loading для экономии контекста
- AI-powered task generation
- testStrategy как first-class field

### Из Backlog.md
- Markdown-native storage (git-friendly)
- Agent instructions как отдельный модуль
- Spec-driven AI development: один PR = одна задача

### Из CCPM
- Documentation checkpoints: "if it's not written, it didn't happen"
- Loop prevention protocol
- Model selection: cheap model для execution, expensive для reasoning

## Что НЕ брать

- **JSON storage** (Taskmaster) — Bobr уже использует markdown + YAML frontmatter, это лучше для git diff
- **Over-documentation** (CCPM) — `.pm/` с 10+ файлами избыточно
- **49 slash commands** (Taskmaster) — лучше меньше, но осмысленнее
- **PM-only mode** (CCPM) — ограничение "PM никогда не пишет код" слишком жёсткое

## Приоритезированный план

### Phase 1 (Immediate value)
1. PRD → Tasks generation
2. Tiered MCP tools
3. Plugin с агентами (explorer, planner)

### Phase 2 (Workflow enhancement)
4. Structured change workflow (verify, delta specs)
5. Terminal Kanban board
6. Context preservation hooks

### Phase 3 (Polish)
7. MCP Resources
8. Complexity analysis
9. Web interface
10. MISTAKES.md / anti-patterns
