---
area:
- workflow
- plugin
- agents
created: '2026-03-18T16:09:31.859131+00:00'
id: BL-71cd
priority: 0
status: done
title: 'Feature Development Workflow: 11-фазный guided workflow для реализации фич'
type: feature
updated: '2026-03-18T17:01:05.058881+00:00'
---

## Описание

Bobr должен предоставлять команду `/bobr:feature` (slash command + skill), которая проводит разработку фичи через 11 фаз. Аналог feature-dev из Claude Code official plugins, но встроенный в Bobr с интеграцией в бэклог и спеки.

## Workflow: 11 фаз

### 1. Discovery
- Уточнение задачи из бэклога
- Создание todo-листа по всем фазам
- Если задача нечёткая — уточняющие вопросы

### 2. Codebase Exploration
- Запуск 2-3 code-explorer агентов параллельно
- Каждый агент исследует свой аспект (похожие фичи, архитектура, паттерны)
- Агенты возвращают 5-10 ключевых файлов
- Основной агент читает все найденные файлы

### 3. Clarifying Questions
- Выявление неоднозначностей, edge cases, scope boundaries
- Презентация вопросов пользователю
- **Ожидание ответов перед продолжением**

### 4. Architecture Design
- Запуск 2-3 code-architect агентов с разными фокусами:
  - Minimal changes (максимум reuse)
  - Clean architecture (maintainability)
  - Pragmatic balance (speed + quality)
- Сравнение подходов, рекомендация
- **Ожидание выбора пользователя**

### 5. Register Spec Change
- Создание change в `.bobr/specs/` (или аналог openspec)
- Генерация артефактов: proposal, specs, design, tasks
- Фиксация выбранной архитектуры

### 6. Implementation
- Реализация по задачам из change
- Следование выбранной архитектуре и паттернам кодовой базы
- Обновление прогресса по задачам

### 7. Quality Review
- Запуск 3 code-reviewer агентов параллельно:
  - Simplicity / DRY / Elegance
  - Bugs / Functional correctness
  - Project conventions / Abstractions
- Презентация находок пользователю
- Исправление по решению пользователя

### 8. Update Documentation
- Обновление спеков, README, комментариев
- Документирование ключевых решений

### 9. Change Archive
- Архивация завершённого change
- Синхронизация delta specs → main specs

### 10. Close Tasks
- Закрытие задач в бэклоге (`bobr backlog edit <ID> --status done`)
- Обновление связанных задач

### 11. Create PR
- Создание PR через `gh pr create`
- Описание: что сделано, ключевые решения, файлы

## Реализация в Bobr

### Plugin command
```
plugin/commands/feature.md    # /bobr:feature slash command
```

### Специализированные агенты
```
plugin/agents/
├── bobr-explorer.md          # Phase 2: исследование кодовой базы
├── bobr-architect.md         # Phase 4: проектирование архитектуры
└── bobr-reviewer.md          # Phase 7: ревью кода
```

### Интеграция с бэклогом
- `/bobr:feature BL-xxxx` — запуск workflow для конкретной задачи
- Автоматическое claim задачи при старте
- Автоматическое закрытие при завершении Phase 10

### Интеграция со спеками
- Phase 5 создаёт change в `.bobr/specs/changes/`
- Phase 9 архивирует change и синхронизирует спеки

## Зависимости

- Требует работающий spec management (BL-874b ✅)
- Требует change workflow (BL-99cf ✅)
- Требует Claude Code plugin (BL-fe07 ✅)

## Ссылки

- Прототип: feature-dev official plugin (`~/.claude/plugins/.../feature-dev/`)
- Исследование: `.bobr/knowledge/research-feature-dev-skill.md`
