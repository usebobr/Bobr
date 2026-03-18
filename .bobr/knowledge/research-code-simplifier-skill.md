# Research: Code-Simplifier Skill (Claude Code Official Plugin)

**Дата**: 2026-03-18
**Источник**: `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/code-simplifier/`

## Обзор

Code-simplifier — минималистичный официальный плагин. Состоит из одного агента, который упрощает недавно изменённый код.

## Архитектура

```
code-simplifier/
├── .claude-plugin/plugin.json
└── agents/
    └── code-simplifier.md
```

### Формат агента
```yaml
---
name: code-simplifier
description: Simplifies and refines code...
model: opus
---
```

## Принципы работы

1. **Preserve Functionality** — никогда не менять поведение, только структуру
2. **Apply Project Standards** — следовать CLAUDE.md проекта
3. **Enhance Clarity** — уменьшить сложность, убрать redundancy
4. **Maintain Balance** — не over-simplify, clarity > brevity
5. **Focus Scope** — только недавно изменённый код

## Процесс

1. Найти недавно изменённые файлы
2. Проанализировать возможности улучшения
3. Применить project-specific best practices
4. Убедиться что функциональность не изменилась
5. Задокументировать значимые изменения

## Выводы для Bobr

- Агент-only плагин (без команд) — легковесный подход
- Модель "автономный агент, запускаемый после изменений" — полезный паттерн
- `model: opus` — для задач требующих рассуждений используется сильная модель
- Минималистичная структура: один файл = один агент
