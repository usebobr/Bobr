---
id: EPIC-01
title: "Native Spec Lifecycle: порт концепций OpenSpec в Bobr"
status: open
priority: 1
area:
  - specs
  - core
  - cli
---

## Цель

Bobr должен нативно поддерживать полный lifecycle спецификаций: delta specs в changes, intelligent merge при архивации, living main specs. Сейчас эту роль выполняет OpenSpec (внешняя зависимость). Цель эпика — портировать ключевые концепции OpenSpec в Bobr, убрав зависимость от внешнего Node.js пакета.

## Контекст

OpenSpec (github.com/Fission-AI/OpenSpec) реализует:
- **Delta specs** в changes: `ADDED / MODIFIED / REMOVED / RENAMED` секции
- **Main specs** как живые документы: `openspec/specs/<capability>/spec.md`
- **Intelligent merge**: парсинг markdown на уровне requirement blocks
- **Artifact instructions**: шаблоны + контекст для AI при создании артефактов
- **Schema-driven workflows**: разные пайплайны для разных типов changes
- **Zod-валидация** структуры спек

Bobr уже имеет `bobr change` с proposal/design/tasks артефактами, но:
- Нет понятия delta spec / main spec
- При архивации спеки не создаются (только перемещение в archive/)
- Нет intelligent merge — `sync_delta_specs` копирует файлы целиком

## Исследование

Подробный анализ OpenSpec: `.bobr/knowledge/research-openspec.md`
Репозиторий для изучения: `.research/openspec/`
Ключевые файлы реализации:
- `src/core/specs-apply.ts` — merge алгоритм
- `src/core/parsers/requirement-blocks.ts` — парсинг delta specs
- `src/core/archive.ts` — оркестрация archive + sync
- `schemas/spec-driven/schema.yaml` — workflow schema

## Фазы

### Phase 1: Delta Spec Format
Определить и реализовать формат delta spec для Bobr.

### Phase 2: Main Specs Storage
Реализовать хранение и чтение main specs в `.bobr/specs/<name>/spec.md`.

### Phase 3: Merge Algorithm
Портировать intelligent merge: парсинг ADDED/MODIFIED/REMOVED/RENAMED, применение к main spec.

### Phase 4: Integration with `bobr change`
Интегрировать delta specs в change workflow: создание, валидация, sync при архивации.

### Phase 5: Artifact Instructions
AI-инструкции для создания артефактов: шаблоны, контекст, правила.

### Phase 6: Migration & Cleanup
Миграция с OpenSpec гибрида на нативные спеки. Удаление зависимости.
