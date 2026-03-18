# Research: OpenSpec (OPSX)

**Дата**: 2026-03-18
**Источник**: `~/.claude/commands/opsx/`, `~/.claude/commands/backlog/`
**Автор**: eyaltoledano (тот же автор что и claude-task-master)

## Обзор

OpenSpec — система управления изменениями (changes) через артефакты. Артефакт-ориентированный workflow: каждое изменение проходит через цепочку артефактов (proposal → specs → design → tasks), после чего реализуется.

## Структура данных

```
openspec/
├── backlog/
│   └── INDEX.md              # Таблица бэклог-элементов
├── changes/
│   └── <change-name>/
│       ├── proposal.md       # Предложение
│       ├── specs/            # Delta specs
│       ├── design.md         # Архитектура
│       └── tasks.md          # Чеклист задач
└── specs/                    # Main specs (синхронизируются из delta)
```

## Workflow (10 команд)

### Бэклог (9 команд в `~/.claude/commands/backlog/`)
- `add` — добавить элемент
- `list` — просмотр
- `edit` — редактирование
- `drop` — удаление
- `status` — обзор
- `explore` — глубокое исследование элемента
- `epic-add`, `epic-list` — управление эпиками
- `promote` — перевод из бэклога в change (запускает /feature-dev или /bug-fix)

### Changes (10 команд в `~/.claude/commands/opsx/`)
- `new` — создать change с выбором schema (workflow)
- `continue` — создать следующий артефакт
- `ff` (fast-forward) — создать все артефакты за раз
- `apply` — реализовать задачи из change
- `verify` — верификация (completeness/correctness/coherence)
- `archive` — архивировать завершённый change
- `bulk-archive` — массовая архивация
- `sync` — синхронизация delta specs → main specs
- `explore` — thinking partner для исследования
- `onboard` — guided onboarding

## Ключевые паттерны

### Schema-driven workflow
Changes поддерживают разные schemas (spec-driven и другие). Schema определяет:
- Какие артефакты нужны
- Порядок зависимостей
- `applyRequires` — что нужно для начала реализации

### Artifact instructions
`openspec instructions <artifact-id> --change <name> --json` возвращает:
- `context` — контекст проекта (не копировать в файл)
- `rules` — правила для артефакта (не копировать)
- `template` — структура файла
- `instruction` — гайдлайны
- `outputPath` — куда писать
- `dependencies` — завершённые артефакты для контекста

### Verify: 3 измерения
1. **Completeness** — все задачи/требования покрыты?
2. **Correctness** — реализация соответствует спекам?
3. **Coherence** — дизайн-решения соблюдены?

Приоритеты: CRITICAL → WARNING → SUGGESTION

### Promote: backlog → workflow
Элемент бэклога "промоутится" в полноценный workflow:
- `bug` → `/bug-fix`
- `feature/idea/improvement` → `/feature-dev`

## Выводы для Bobr

- **Артефакт-ориентированный workflow** — change состоит из типизированных артефактов, а не свободного текста
- **Schema/workflow вариативность** — разные типы changes имеют разные pipeline
- **Delta specs** — изменения фиксируются как delta, потом синхронизируются в main
- **CLI как backend** — все команды через `openspec` CLI, slash-команды — обёртки
- **Verify перед archive** — формальная верификация перед закрытием change
- **Backlog → Change promotion** — мост между бэклогом и разработкой
