# Vision & Scope: Ревизия после Phase 0

> Date: 2026-03-19 | Status: DRAFT | Author: Artem + Claude Code

---

## 1. Что показала Phase 0

Phase 0 реализовала `.bobr/` формат + CLI для бэклога с зависимостями. Технически — всё работает. Но я не понимаю, зачем мне это нужно.

### Настоящий инсайт

**Я пытался воссоздать свой workflow из Expecto как отдельный инструмент, хотя на самом деле мне нужно упаковать ВЕСЬ свой workflow — данные, процесс и интерфейс — в воспроизводимый, переносимый формат.**

На Expecto у меня было:
- `/backlog` — slash-команды для управления задачами
- `/openspec` — slash-команды для spec-driven development
- Requirements management — через взаимодействие с Claude Code
- Это всё жило в `.claude/` конфигурациях, в плагинах, в моей голове

Это работало, но **не переносилось** между проектами и людьми.

**Phase 0 ошибка: я начал строить CLI (инструмент), тогда как мне нужно было строить workflow (процесс + данные + интерфейс).**

### Что PRD v0.8 делал не так

1. **Путал инструмент и workflow** — CLI это деталь реализации, а не продукт. Продукт — это воспроизводимый процесс разработки.
2. **Не определил интерфейс для человека** — CLI неудобен для обзора и управления. Нужен и терминал (для работы с агентом), и web (для обзора картины).
3. **Слишком много концепций** — requirements (Вигерс), specs (OpenSpec), changes, knowledge base, consumer interfaces, Runner — каждая сама по себе продукт.

---

## 2. Пересмотренное видение

### 2.1 Одно предложение

**Bobr — воспроизводимый workflow для структурированной разработки с AI-агентами, включающий данные (`.bobr/`), процесс (skills + agents), и два интерфейса: терминал (Claude Code) для работы и web dashboard для обзора.**

### 2.2 Три слоя Bobr

```
┌─────────────────────────────────────────────────────────────┐
│                      ИНТЕРФЕЙСЫ                             │
│                                                             │
│   ┌──────────────────────┐    ┌──────────────────────────┐  │
│   │   Terminal            │    │   Web Dashboard          │  │
│   │   (Claude Code)       │    │   (обзор + управление)   │  │
│   │                       │    │                          │  │
│   │  /bobr:feature        │    │  Бэклог (kanban/list)    │  │
│   │  /bobr:backlog        │    │  Requirements (pages)    │  │
│   │  /bobr:requirements   │    │  Зависимости (граф)      │  │
│   │  /bobr:status         │    │  Статус проекта          │  │
│   │                       │    │                          │  │
│   │  → для РАБОТЫ         │    │  → для ОБЗОРА            │  │
│   └───────────┬───────────┘    └────────────┬─────────────┘  │
│               │                             │                │
│               └──────────┬──────────────────┘                │
│                          │                                   │
├──────────────────────────┼───────────────────────────────────┤
│                      ПРОЦЕСС                                │
│                          │                                   │
│   Skills (slash-commands) + Agents (sub-agents)              │
│                                                              │
│   /bobr:feature  = explore → design → implement → verify     │
│   /bobr:backlog  = add, ready, claim, done                   │
│   bobr-explorer  = исследование кодовой базы                 │
│   bobr-architect = проектирование решений                    │
│   bobr-reviewer  = code review                               │
│                                                              │
├──────────────────────────┼───────────────────────────────────┤
│                      ДАННЫЕ                                  │
│                          │                                   │
│   .bobr/  (git-native, YAML+MD, hash IDs)                   │
│                                                              │
│   .bobr/backlog/     — задачи                                │
│   .bobr/requirements/ — требования                           │
│   .bobr/knowledge/   — база знаний                           │
│   .bobr/specs/       — спецификации                          │
│   .bobr/config.yaml  — настройки проекта                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 2.3 Два интерфейса — одни данные

| | Terminal (Claude Code) | Web Dashboard |
|---|---|---|
| **Для чего** | Работа: создание, редактирование, выполнение задач | Обзор: статус проекта, приоритеты, зависимости |
| **Кто** | Разработчик + агент | Разработчик, PM, CEO |
| **Как** | Slash-команды, естественный язык | Браузер, визуальные компоненты |
| **Примеры** | `/bobr:feature "добавить авторизацию"` | Kanban-доска с задачами, граф зависимостей |
| **Аналог** | Как работал Expecto workflow | Как Notion/Linear для обзора |

**Ключевое**: терминал — для РАБОТЫ (агент делает), web — для ОБЗОРА (человек видит картину). Оба читают/пишут `.bobr/`.

### 2.4 Что такое Bobr

**Bobr = упакованный workflow:**

1. **Данные** — формат `.bobr/` (git-native YAML+MD). Source of truth в репозитории.

2. **Процесс** — skills и agents для Claude Code:
   - `/bobr:backlog` — управление задачами
   - `/bobr:feature` — полный цикл разработки фичи
   - `/bobr:requirements` — управление требованиями
   - `/bobr:knowledge` — база знаний
   - `bobr-explorer`, `bobr-architect`, `bobr-reviewer` — агенты-специалисты

3. **Интерфейс** — два входа в одни данные:
   - **Terminal** (Claude Code) — для работы через естественный язык и slash-команды
   - **Web dashboard** — для визуального обзора и управления (kanban, графы, страницы)

### 2.5 Чем Bobr НЕ является

- **Не просто CLI** — CLI может существовать как internal utility, но не это продукт
- **Не просто плагины** — плагины без web dashboard не дают обзора, а это критично
- **Не замена Claude Code** — расширение его возможностей + отдельный web для обзора
- **Не Jira/Linear** — web dashboard read-heavy (обзор), а не write-heavy (управление)

### 2.6 Куда девается то, что уже построено?

| Phase 0 артефакт | Судьба | Почему |
|---|---|---|
| `.bobr/` формат (YAML+MD, hash IDs) | **Сохраняется** | Data layer — основа всего |
| `bobr` CLI | **Internal utility** | Skills и web dashboard могут вызывать CLI, но это не интерфейс для человека |
| SQLite cache | **Сохраняется** | Web dashboard будет использовать для быстрых запросов |
| Worktree workflow | **Сохраняется** | Claude Code работает через worktrees |

---

## 3. Принципы

1. **Workflow-first** — Bobr это не инструмент, а упакованный воспроизводимый процесс разработки
2. **Two interfaces, one truth** — Terminal для работы, Web для обзора. Данные одни — `.bobr/`
3. **Agent does, human sees** — агент выполняет работу (через skills), человек видит картину (через web dashboard)
4. **Git-native storage** — `.bobr/` в репозитории, версионируется с кодом
5. **Portable workflow** — подключил Bobr к новому проекту = получил тот же процесс
6. **Convention over configuration** — `.bobr/` структура, разумные defaults, zero setup

---

## 4. Scope: что делать дальше

### Phase 0.5a: `/bobr:feature` skill (1-2 недели)

**Цель**: Начать вести разработку Bobr через `/bobr:feature`.

1. **`/bobr:feature` skill** — guided workflow: explore → design → implement → verify
   - Это порт Expecto workflow в формальный skill
   - Создаёт задачи в `.bobr/backlog/`, спеки в `.bobr/specs/`
   - Использует sub-agents (explorer, architect)
2. **`/bobr:init`** — bootstrap `.bobr/` структуры (нужен для feature)
3. **`/bobr:status`** — быстрый обзор проекта в терминале

**Dogfooding**: следующую фичу Bobr разрабатываем через `/bobr:feature`.

### Phase 0.5b: Web Dashboard MVP (параллельно или сразу после)

**Цель**: Видеть картину проекта в браузере.

**Стек**: Node.js server (Express) + REST API + React SPA

4. **`bobr web`** — поднимает локальный сервер на localhost:3000
5. **GET /api/tasks** — читает `.bobr/backlog/`, возвращает JSON
6. **GET /api/status** — сводка проекта
7. **Dashboard view** — список задач (table/kanban), статусы, приоритеты
8. **Auto-refresh** — file watcher на `.bobr/`, WebSocket push

```
bobr web
# → http://localhost:3000
#
# API:
#   GET /api/tasks        → список задач из .bobr/backlog/
#   GET /api/tasks/:id    → детали задачи
#   GET /api/status       → сводка проекта
#   GET /api/specs        → список спецификаций
#
# UI:
#   /                     → dashboard (статус + последние изменения)
#   /tasks                → список/kanban задач
#   /tasks/:id            → детали задачи
#
# Позже (Phase 1):
#   POST/PUT /api/tasks   → создание/редактирование через web
#   /requirements         → страницы требований
#   /graph                → граф зависимостей
```

**Read-only на старте** — пишем через терминал (skills), смотрим через web. Write-API добавим в Phase 1.

### Phase 1: Structured development

9. `/bobr:backlog` — полноценное управление задачами через skill
10. `/bobr:requirements` — управление требованиями
11. `/bobr:knowledge` — база знаний проекта
12. Web dashboard: write API, requirements pages, dependency graph
13. MCP Server — для Cursor, Copilot, других агентов

### Phase 2: Team

14. Multi-user web dashboard (auth, roles)
15. Cowork интерфейс для нетехнических пользователей
16. Multi-agent coordination

---

## 5. Решения и открытые вопросы

### Решено

1. ~~**Web dashboard технология**~~ → **Local server + REST API** (Express + React SPA). Начинаем read-only, write API в Phase 1.
2. ~~**Scope первого skill**~~ → **`/bobr:feature`**. Самый ценный, сразу dogfood'им на себе.

### Открыто

3. **Портабельность** — MCP Server как universal layer для не-Claude агентов? (Phase 1)
4. **Монорепо** — Skills, agents, CLI, web dashboard — в одном репо или разделить?
5. **Web dashboard deployment** — только localhost, или позже облачный вариант? (Phase 2)

---

## 6. Связь с текущим PRD

Этот документ **требует переписывания PRD v0.8**. Изменилась не деталь — изменилось понимание продукта:

| | PRD v0.8 | Ревизия |
|---|---|---|
| **Что это** | AI-native PM platform | Упакованный workflow (данные + процесс + интерфейс) |
| **Продукт** | Standalone CLI + Web UI + MCP | Skills + Agents + Web Dashboard |
| **Интерфейс для работы** | CLI | Terminal (Claude Code + skills) |
| **Интерфейс для обзора** | Web UI (когда-нибудь) | Web Dashboard (с самого начала) |
| **Конкуренты** | Taskmaster, Linear, Devin | Expecto workflow (свой же), Kiro hooks, CLAUDE.md conventions |
| **Dogfooding тест** | "Я веду бэклог в Bobr CLI" | "Я работаю через `/bobr:feature`, смотрю статус в web dashboard" |
