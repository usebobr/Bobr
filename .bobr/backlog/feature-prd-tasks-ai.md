---
area:
- ai
- backlog
- requirements
created: '2026-03-18T16:04:35.126961+00:00'
id: BL-e816
priority: 1
status: open
title: 'PRD → Tasks: AI-генерация задач из требований'
type: feature
updated: '2026-03-18T16:04:35.127081+00:00'
---

## Описание

Команда `bobr generate` читает PRD/требования из `.bobr/requirements/` и генерирует задачи в бэклоге с помощью AI (LLM).

Вдохновлено Taskmaster AI (`task-master parse-prd`), который является killer-feature продукта с 42k+ stars.

## Использование

```bash
# Из конкретного файла требований
bobr generate --from .bobr/requirements/prd.md

# Из всех requirements
bobr generate

# С фильтром по области
bobr generate --area api

# Добавить к существующим (не перезаписывать)
bobr generate --append
```

## Что генерируется для каждой задачи

- **title** — краткое название
- **description** — подробное описание с контекстом
- **type** — feature / bug / improvement
- **priority** — 0-4 на основе анализа требований
- **area** — области затрагиваемые задачей
- **dependencies** — зависимости между сгенерированными задачами
- **acceptance criteria** — критерии приёмки
- **test strategy** — стратегия тестирования (как в Taskmaster)

## Реализация

1. Читаем файлы из `.bobr/requirements/` (PRD, PRFAQ, specs)
2. Формируем промпт: контекст проекта + требования + текущий бэклог (чтобы не дублировать)
3. Вызываем LLM (Anthropic API) с structured output (JSON schema)
4. Валидируем результат
5. Создаём задачи через `bobr backlog add`
6. Показываем summary: сколько задач создано, граф зависимостей

## Дополнительно (Phase 2)

- **Complexity analysis** — AI оценивает сложность и рекомендует декомпозицию
- **Research mode** — использование web search для informed decisions
- **Incremental generation** — `--append` добавляет задачи из нового PRD без дублирования

## Ссылки

- Исследование: `.bobr/knowledge/research-taskmaster.md`
- Обобщение: `.bobr/knowledge/research-summary-ideas.md`
