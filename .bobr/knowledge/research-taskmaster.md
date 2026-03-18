# Research: Taskmaster AI (claude-task-master)

**Дата**: 2026-03-18
**Источник**: https://github.com/eyaltoledano/claude-task-master
**Stars**: 42k+ (самый популярный инструмент в категории)

## Обзор

Taskmaster — система управления задачами для AI-driven разработки. Работает как MCP-сервер и CLI. Ключевая фича — генерация задач из PRD с помощью AI.

## Архитектура

### Tech Stack
- Node.js / JavaScript
- Zod для валидации схем
- MCP SDK (`@modelcontextprotocol/sdk`)
- Multi-provider AI (Anthropic, OpenAI, Google, Perplexity, xAI, OpenRouter, Azure, Ollama)

### Структура проекта
```
.taskmaster/
├── tasks/
│   ├── tasks.json          # Главная БД задач (JSON!)
│   ├── task-1.md           # Индивидуальные файлы задач
│   └── task-2.md
├── docs/
│   └── prd.md              # PRD для парсинга
├── reports/
│   └── task-complexity-report.json
├── templates/
│   └── example_prd.md
└── config.json             # Конфигурация AI моделей
```

### Модель данных задачи
```javascript
{
  id: number,           // 1, 2, 3...
  title: string,        // max 200 chars
  description: string,
  status: 'pending' | 'in-progress' | 'blocked' | 'done' | 'cancelled' | 'deferred',
  dependencies: number[],
  priority: 'low' | 'medium' | 'high' | 'critical' | null,
  details: string | null,
  testStrategy: string | null,
  subtasks: Subtask[]
}
```

ID подзадач: `1.1`, `1.2`, `2.1` (иерархия через точку).

## MCP Integration

### Tiered tool loading (оптимизация контекста!)
| Tier | Tools | Назначение |
|------|-------|------------|
| `core` | 7 | Минимальный ежедневный набор |
| `standard` | 14 | Стандартное управление |
| `all` | 42+ | Полный набор с research, autopilot |

Core tools: `get_tasks`, `next_task`, `get_task`, `set_task_status`, `update_subtask`, `parse_prd`, `expand_task`

### Claude Code Plugin
```
packages/claude-code-plugin/
assets/claude/
├── commands/     # 49 slash commands
└── agents/       # 3 агента (orchestrator, executor, checker)
```

## AI-Powered Features

- **parse-prd** — генерация задач из PRD документа
- **analyze-complexity** — анализ сложности задач с research
- **expand** — разбиение задачи на подзадачи
- **update** — обновление задач с AI context
- **add-task** — создание задач с AI assistance
- **Research mode** (`--research`) — использование Perplexity для глубокого исследования

## Workflow

```
PRD → parse-prd → tasks.json → analyze-complexity → expand → next → implement → done
```

Ежедневный цикл:
```bash
task-master next              # Следующая задача
task-master show <id>         # Детали
task-master update-subtask    # Логирование прогресса
task-master set-status --done # Завершение
```

## Ключевые паттерны

1. **JSON как хранилище** — tasks.json, не markdown
2. **Multi-provider AI** — поддержка 8+ провайдеров
3. **Tiered MCP tools** — core/standard/all для экономии контекста
4. **PRD-driven** — генерация задач из PRD
5. **Complexity analysis** — AI оценивает сложность для оптимального expand
6. **testStrategy** — каждая задача имеет стратегию тестирования
7. **Subtask hierarchy** — точечная нотация для вложенности (1.1.1)
8. **Individual task files** — .md файлы генерируются из tasks.json

## Выводы для Bobr

- **Tiered MCP tools** — отличная идея, экономит контекст агента
- **PRD → Tasks** — AI-генерация задач из требований — killer feature
- **Complexity analysis** — оценка сложности помогает планировать
- **JSON storage** — быстрее для программного доступа, но менее human-readable чем markdown
- **Research mode** — интеграция с web search для informed decisions
- **testStrategy per task** — полезно для quality-first подхода
- **49 slash commands** — возможно избыточно, но показывает глубину функционала
