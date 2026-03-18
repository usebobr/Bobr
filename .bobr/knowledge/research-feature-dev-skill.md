# Research: Feature-Dev Skill (Claude Code Official Plugin)

**Дата**: 2026-03-18
**Источник**: `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/feature-dev/`
**Автор плагина**: Sid Bidasaria (Anthropic)

## Обзор

Feature-dev — официальный плагин Claude Code для структурированной разработки фич. Определяет 7-фазный (8 с OpenSpec) workflow с 3 специализированными агентами.

## Архитектура

### Структура файлов
```
feature-dev/
├── .claude-plugin/plugin.json
├── README.md
├── commands/
│   └── feature-dev.md          # Slash command /feature-dev
└── agents/
    ├── code-explorer.md        # Исследование кодовой базы
    ├── code-architect.md       # Проектирование архитектуры
    └── code-reviewer.md        # Ревью кода
```

### Формат команд
YAML frontmatter + Markdown:
```yaml
---
description: Guided feature development with codebase understanding and architecture focus
argument-hint: Optional feature description
---
```

## 8 фаз workflow

1. **Discovery** — уточнение задачи, создание todo
2. **Codebase Exploration** — 2-3 code-explorer агента параллельно, чтение ключевых файлов
3. **Clarifying Questions** — выявление неоднозначностей, ожидание ответов пользователя
4. **Architecture Design** — 2-3 code-architect агента с разными фокусами, рекомендация пользователю
5. **Register OpenSpec Change** — создание change через `openspec new change`, генерация артефактов
6. **Implementation** — реализация по задачам из OpenSpec
7. **Quality Review** — 3 code-reviewer агента параллельно (DRY/bugs/conventions)
8. **Summary** — документирование результатов

## 3 специализированных агента

### code-explorer
- Трассировка execution paths
- Маппинг архитектурных слоёв
- Возвращает 5-10 ключевых файлов для чтения

### code-architect
- Анализ паттернов кодовой базы
- Предлагает несколько подходов (minimal / clean / pragmatic)
- Blueprint с конкретными файлами для создания/модификации

### code-reviewer
- Фильтрация по confidence (≥80%)
- 3 фокуса: simplicity/DRY, bugs/correctness, conventions/abstractions
- Specific fixes с file:line references

## Ключевые паттерны

1. **Параллельные агенты** — 2-3 агента запускаются одновременно для разных аспектов
2. **Human-in-the-loop** — пользователь утверждает архитектуру перед реализацией
3. **Agents → Read files** — агенты возвращают списки файлов, основной агент их читает
4. **Интеграция с OpenSpec** — Phase 5 регистрирует change в openspec
5. **TodoWrite** — трекинг прогресса через все фазы

## Выводы для Bobr

- Модель "фаза → агенты параллельно → user approval → следующая фаза" хорошо работает
- Разделение exploration/architecture/review на специализированных агентов — отличный паттерн
- OpenSpec интеграция показывает: change management должен быть встроен в workflow
- Clarifying Questions как обязательная фаза предотвращает ошибки проектирования
