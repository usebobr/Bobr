# PRD: Bobr — AI Agent First платформа для разработки ПО

> Version: 0.5 | Date: 2026-03-18 | Author: Artem (с помощью Claude Code)

---

## 1. Проблема

### 1.1 Контекст рынка

AI-агенты стали полноценными участниками software development: Claude Code, Cursor, GitHub Copilot Agent, Codex, Devin, Jules — все умеют автономно брать задачу, писать код, создавать PR. **Рынок взорвался**: 25+ open-source проектов, 15+ SaaS с агентными возможностями, 5800+ MCP-серверов, 97M+ скачиваний SDK/месяц. Taskmaster AI набрал 15 500 звёзд за 9 недель. Cognition (Devin) оценена в $10.2B.

Но **разрыв между инструментами огромен**. Сформировались три модели, каждая с фатальным ограничением:

| Модель | Примеры | Сильная сторона | Фатальное ограничение |
|--------|---------|-----------------|----------------------|
| **Git-native markdown** | Taskmaster AI, Backlog.md, CCPM | Zero-config, максимальная совместимость, solo/small team | Не масштабируется на команды, нет enterprise-функций (permissions, audit) |
| **Agent-as-teammate в PM** | Linear for Agents, Jira/Rovo, Asana AI | Enterprise-ready, audit trail, зрелый PM | AI — надстройка над legacy архитектурой, не перепроектированной для агентов |
| **Full-stack agent platform** | Devin+Windsurf, Codex, Jules, Capy | Агент и планирует, и исполняет | Vendor lock-in, стоимость, ограниченная прозрачность |

**Ни одна модель не покрывает полный цикл**: requirements engineering → knowledge management → backlog → specs → agent execution → delivery → verification.

Height.app (наиболее "AI-first" PM) — **закрылся**: быть слишком далеко впереди рынка без пользовательской базы фатально. Но взрыв Taskmaster AI и оценка Devin сигнализируют: **рынок созрел**.

### 1.2 Что отсутствует на рынке (из Deep Research)

| Пробел | Детали |
|--------|--------|
| **Requirements + Agent orchestration** | Ни один инструмент не связывает формализованные требования (Vision, Use Cases) с контекстом для AI-агента |
| **Knowledge management + Delivery pipeline** | Протоколы встреч, письма, документы клиента не попадают в контекст агента автоматически |
| **Кросс-командная координация агентов** | Практически не решена — каждый агент работает изолированно |
| **Аналитика производительности агентов** | Какой тип агента лучше для какого типа задач — в зачаточном состоянии |
| **Bidirectional sync** | AI-native → existing PM и обратно порождает значительное трение |
| **Spec-driven development как продукт** | Kiro (Amazon) начал, но это IDE, не платформа для команды |

### 1.3 Боль пользователя

Продвинутая команда из 3–10 человек, использующая AI-агентов:

| Боль | Следствие |
|------|-----------|
| Нет единого места для требований, бэклога и кода | Контекст теряется между Notion, Slack, IDE и головой PM-а |
| AI-агент не знает "зачем" — только "что" | Агент пишет код без понимания бизнес-контекста, результат ревьюится дольше |
| Каждый настраивает свой workflow с Claude Code/Cursor | Нет воспроизводимого процесса; уход человека = потеря workflow |
| Нет прозрачности: кто что делает (человек или агент) | PM не видит статус, dev не видит context соседних задач |
| Knowledge silos: письма, совещания, документы разбросаны | Одни и те же вопросы задаются повторно; onboarding долгий |
| Token budgets не управляемы | AI costs растут непредсказуемо, нет capacity planning |

### 1.4 Личный опыт (proof of concept)

На проекте **Expecto** я выстроил полный цикл:

- **Requirements**: плагин по Вигерсу (Vision & Scope, Stakeholder Profiles, Use Cases, Requirements Review, Elicitation Planning)
- **Backlog**: OpenSpec-based система (9 slash-команд: add → explore → promote → implement → verify → archive), 68+ items, epics
- **Specs**: 117 спецификаций, 64 архивных changes, spec-driven development
- **Code**: 100% написан Claude Code (FastAPI + React + DuckDB, ~30K LOC)
- **Deploy**: PR → Render preview → merge → production
- **Knowledge**: проектный журнал (500+ строк), протоколы встреч, анализ документов клиента (FIBU-Lieferungen)

**Это работает, но это не масштабируется**: workflow живёт в `.claude/` директориях на моей машине, в плагинах, в моей голове. Это Модель 1 (git-native markdown) в чистом виде — с requirements management, которого нет ни у кого.

---

## 2. Видение продукта

### 2.1 Vision Statement

**Bobr** — платформа, где команда формулирует требования, управляет бэклогом и доставляет код, используя AI-агентов как основных (но не единственных) исполнителей.

> "CEO нажимает «Запустить» — AI-агент пишет код — CEO получает ссылку на Preview"

### 2.2 Стратегическое позиционирование

Bobr объединяет лучшие черты всех трёх моделей, добавляя то, чего нет ни у кого:

```
       Model 1                    Model 2                Model 3
   Git-native markdown      Agent-as-teammate        Full-stack agent
   (Taskmaster, Backlog.md)  (Linear, Jira)          (Devin, Codex, Jules)
          │                       │                        │
          ▼                       ▼                        ▼
   ┌─────────────┐        ┌─────────────┐         ┌──────────────┐
   │ Markdown +  │        │ Team collab  │         │ Agent        │
   │ YAML specs  │        │ Permissions  │         │ orchestration│
   │ in git repo │        │ Audit trail  │         │ Parallel exec│
   └──────┬──────┘        └──────┬──────┘         └──────┬───────┘
          │                      │                       │
          └──────────────────────┼───────────────────────┘
                                 ▼
                    ┌────────────────────────┐
                    │        BOBR         │
                    │                        │
                    │  + Requirements Mgmt   │  ◄── НЕТ НИ У КОГО
                    │  + Knowledge Base      │  ◄── НЕТ НИ У КОГО
                    │  + Spec-driven dev     │  ◄── Только Kiro (IDE)
                    │  + Full traceability   │  ◄── НЕТ НИ У КОГО
                    └────────────────────────┘
```

### 2.3 Ключевые принципы

1. **AI Agent First, but not only** — агент — полноправный участник команды (как Linear for Agents, но глубже), человек всегда может сделать то же самое
2. **Tool Provider, not AI Consumer** — Bobr не вызывает AI API. Bobr предоставляет данные и инструменты, с которыми работают AI-агенты (Claude Code, Cursor, Codex, Devin, Jules, Copilot). Три уровня интеграции: файлы (.bobr/), CLI (bobr commands), MCP (protocol). Zero AI dependency в ядре
3. **Context is King** — каждый агент получает полный контекст: requirements + decisions + constraints + knowledge base (паттерн "Structured data over natural language" из MetaGPT)
4. **Requirements-driven** — не "ticket → code", а "business need → requirements → specs → code → verify" (методология Вигерса + spec-driven development как у Kiro)
5. **Git-native + Cloud-synced** — артефакты в git (портабельность), метаданные в cloud (team collaboration)
6. **Propose-Review everywhere** — AI генерирует, человек ревьюит и решает (доминирующий паттерн даже в самых автономных системах)
7. **Token budget as capacity** — AI cost как метрика планирования вместо story points (паттерн из Scrum.org для AI-first)
8. **Convention over configuration** — разумные defaults, `.bobr/` структура, AGENTS.md как стандарт
9. **Dogfooding from Day 1** — Bobr разрабатывается с помощью Bobr. Каждая фаза roadmap заканчивается тем, что следующая фаза ведётся уже в самом продукте

### 2.4 Расширенное сравнение с конкурентами

| Capability | Bobr | Taskmaster AI | Backlog.md | Hamster | Linear+Agents | Jira+Rovo | Devin | Codex | Jules | Kiro |
|---|---|---|---|---|---|---|---|---|---|---|
| **Requirements mgmt** | ✅ Вигерс | ❌ | ❌ | ❌ Briefs | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ req.md |
| **Knowledge base** | ✅ Full | ❌ | ❌ | ❌ | ❌ | ⚠️ Confluence | ❌ | ❌ | ❌ | ❌ |
| **Spec-driven dev** | ✅ OpenSpec | ❌ | ⚠️ Basic | ❌ | ❌ | ❌ | ❌ | ⚠️ /plan | ❌ | ✅ 3-phase |
| **Git-native storage** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Multi-agent parallel** | ✅ Worktrees | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ MultiDevin | ✅ Sandbox | ✅ Batch | ❌ |
| **Agent monitoring** | ✅ Cost+logs | ❌ | ❌ | ❌ | ⚠️ Cycle time | ❌ | ✅ | ✅ | ⚠️ | ❌ |
| **Team collaboration** | ✅ | ❌ | ⚠️ Kanban | ✅ RT | ✅ | ✅ | ⚠️ | ⚠️ Slack | ❌ | ❌ |
| **MCP native** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Traceability** | ✅ Full | ❌ | ❌ | ❌ | ❌ | ⚠️ | ❌ | ❌ | ❌ | ⚠️ |
| **Open source** | ✅ Plan | ✅ MIT+CC | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Deploy preview** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Human execution** | ✅ Full parity | ⚠️ | ⚠️ | ⚠️ | ✅ | ✅ | ❌ Agent-only | ❌ | ❌ | ⚠️ |

**Уникальная комбинация Bobr**: Requirements + Knowledge + Specs + Agent orchestration + Team + Git-native + Open source.

---

## 3. Целевая аудитория

### 3.1 Первичная (ICP — Ideal Customer Profile)

**Tech-lead / CTO малой продуктовой команды (3–15 человек)**, который:
- Уже использует AI-агентов для coding (Claude Code, Cursor, Copilot)
- Чувствует, что "магия" не масштабируется на команду
- Хочет дать AI-агентам контекст, а не просто промпты
- Ценит structured requirements, но не хочет тяжёлый процесс

**Пример**: Artem и команда Expecto — 5 человек, FastAPI + React, 100% AI-written code, нужна прозрачность и воспроизводимость.

**Пример**: Команда Apilize — 3 человека (CEO, CFO, CTO). Платформа финансового моделирования для оценки недвижимости (DCF, EWV, Acquimod). 3 параллельных продукта, 5 клиентов. CTO владеет кодовой базой и использует Claude Code. CEO и CFO — нетехнические, используют ChatGPT. Бэклог в Notion, документация в Obsidian vault (40+ фич, 3 ADR, 13 open questions). **Боль**: CEO не видит прогресс разработки, не может запустить задачу на исполнение, контекст разбросан между Notion, Obsidian и головой CTO.

### 3.2 Вторичная

- **Фаундеры-одиночки** (текущая аудитория Taskmaster AI) — хотят структуру без overhead, переросли Taskmaster
- **Консалтинговые / аутсорсинговые команды** — нужна прозрачность для клиентов + knowledge management по проектам
- **Enterprise product teams** — переход от Jira/Confluence к AI-native workflow, но с привычным уровнем governance

### 3.3 Персоны

| Персона | Роль | Потребность | Частота |
|---------|------|-------------|---------|
| **Костя (CEO)** | Определяет приоритеты, общается с клиентами | Видеть бэклог, запустить задачу, получить Preview link, дать feedback | Ежедневно |
| **Иван (CFO)** | Контролирует бюджет и AI costs | Видеть расходы на агентов, комментировать приоритеты | Еженедельно |
| **Артём (CTO)** | Владеет кодом, настраивает агентов | Полный контроль: specs, context, agent config, code review | Ежедневно |
| **AI Agent (Claude Code)** | Пишет код по спецификации | Structured context: spec + acceptance criteria + codebase knowledge | Непрерывно |
| **Клиент (WertXpert, INTREAL)** | Использует продукт, даёт feedback | Видеть preview, сообщать баги и запросы | По запросу |

---

## 4. Архитектурные паттерны

> На основе deep research ландшафта. 8 паттернов, из которых мы берём 7.

### 4.1 Паттерны, которые мы берём

#### P1: Structured data over natural language
**Источник**: MetaGPT (ICLR 2024), Backlog.md, AGENTS.md стандарт

Задачи, specs, requirements — как YAML + Markdown с метаданными, а не свободный текст. MetaGPT доказал: структурированные артефакты между агентами дают лучшие результаты, чем диалог (как в ChatDev).

**Реализация в Bobr**: `.bobr/` структура, YAML frontmatter во всех артефактах, AGENTS.md автогенерация.

#### P2: Propose-Review
**Источник**: ClickUp Super Agent, доминирует даже в самых автономных системах

AI генерирует — человек ревьюит и решает. Ключевая цитата: *"Агент не заменяет мой judgment — он делает административную инфраструктуру вокруг моего judgment."*

**Реализация в Bobr**: Каждый этап change workflow (proposal → design → tasks) проходит human review перед следующим шагом.

#### P3: Token budget as capacity planning
**Источник**: Scrum.org, AI-first Scrum адаптации

Story points неприменимы к AI-агентам. Вместо них — **токен-бюджеты и compute cost**. PBI для агентов переводятся в технические промпты с жёсткими границами.

**Реализация в Bobr**: Cost tracking per task/agent/project. Budget limits. Agent efficiency analytics (какой тип задачи стоит сколько).

#### P4: Isolated parallel execution
**Источник**: Claude Forge (39 фич, 9 батчей, 20 агентов, 0 конфликтов), CCPM (12+ параллельных агентов), Vibe Kanban

Анализ бэклога → выявление задач без file-конфликтов → группировка в волны → запуск агента в **изолированном git worktree**.

**Реализация в Bobr**: Wave planner определяет независимые задачи, каждый агент в своём worktree, автоматический merge.

#### P5: Event-driven feedback loops
**Источник**: GitHub Accessibility team (89% issues закрываются за 90 дней вместо 21%), Spotify Engineering

Каждое событие (создание issue, смена статуса, PR, merge) триггерит следующий шаг. Environment (тесты, CI, линтинг) важнее промпта на масштабе.

**Реализация в Bobr**: Все действия генерируют события. Hooks на статусы. Автоматический переход задач по pipeline.

#### P6: Code-to-ticket feedback
**Источник**: Nick Tune (2026)

Post-merge reflection: AI создаёт follow-up issues для code review findings. Feedback пропагируется назад к specs и планированию.

**Реализация в Bobr**: После merge агент анализирует diff, создаёт follow-up backlog items, обновляет specs.

#### P7: Context injection (AGENTS.md / CLAUDE.md)
**Источник**: De-facto стандарт (Codex, Claude Code, Backlog.md, Kiro)

Файл инструкций для агента, автоматически генерируемый из project context.

**Реализация в Bobr**: `bobr context generate` создаёт CLAUDE.md / AGENTS.md из requirements + specs + conventions + knowledge base. Агент читает его при старте.

#### P8: Tool Provider, not AI Consumer
**Источник**: Unix philosophy ("do one thing well"), MCP standard, Backlog.md

Система управления не должна содержать AI — она должна быть **инструментом для AI**. Агенты приходят и уходят (Claude → Codex → следующий), данные и процесс остаются.

**Реализация в Bobr**: Три уровня доступа для агентов:

| Уровень | Механизм | Что получает агент | Какие агенты |
|---------|----------|-------------------|--------------|
| **L1: Files** | Агент читает/пишет `.bobr/` напрямую | YAML+MD файлы, machine-readable | Все (любой агент умеющий читать файлы) |
| **L2: CLI** | Агент вызывает `bobr` команды | `--output json` на всех командах | Claude Code, Codex, Devin, Jules |
| **L3: MCP** | Агент подключает Bobr MCP Server | Structured tools: read_backlog, create_change, etc. | Claude Code, Cursor, Copilot |

Bobr **не вызывает Claude API / OpenAI / Google AI**. Zero AI dependency. AI-логика (explore, generate proposal, code review) — ответственность агента, который работает с Bobr.

### 4.2 Паттерн, который мы НЕ берём

#### ~~P8: Ролевая multi-agent simulation~~
**Источник**: MetaGPT (PM → Architect → Engineer → QA), BMAD (12 персон), ChatDev

Несколько AI "ролей" общаются друг с другом для имитации команды.

**Почему нет**: Overhead на inter-agent communication, hallucination amplification, трудно отлаживать. Bobr ориентирован на реальные команды людей + один агент на задачу, а не на симуляцию компании.

---

## 5. Функциональные требования

### 5.1 Module: Knowledge Base

> Единое хранилище контекста команды — то, что AI-агент "знает" о проекте.

#### 5.1.1 Document Management
- **FR-KB-01**: Загрузка документов (PDF, DOCX, XLSX, TXT, MD, images)
- **FR-KB-02**: AI-извлечение структурированной информации (ключевые факты, решения, контакты, даты)
- **FR-KB-03**: Полнотекстовый + семантический поиск по всем документам
- **FR-KB-04**: Версионирование документов
- **FR-KB-05**: Auto-linking: AI находит связи между документами и requirements/backlog items

#### 5.1.2 Meeting Intelligence
- **FR-KB-10**: Импорт записей / транскриптов совещаний (аудио, видео, текст)
- **FR-KB-11**: AI-саммаризация: решения, action items, открытые вопросы
- **FR-KB-12**: Автоматическая привязка action items к бэклогу (паттерн P6)
- **FR-KB-13**: Поиск по совещаниям ("Что решили по X?")

#### 5.1.3 Communication Archive
- **FR-KB-20**: Импорт email-цепочек (интеграция Gmail/Outlook)
- **FR-KB-21**: Импорт Slack-тредов
- **FR-KB-22**: AI-экстракция решений и обязательств из переписки
- **FR-KB-23**: Связывание коммуникаций с требованиями и задачами

#### 5.1.4 Project Journal
- **FR-KB-30**: Автоматический журнал проекта (хронология событий, решений, изменений) — как PROJECT_JOURNAL.md в Expecto, но автогенерируемый
- **FR-KB-31**: Ручные записи с AI-тегированием
- **FR-KB-32**: Timeline-визуализация истории проекта

### 5.2 Module: Requirements Management

> Формализация потребностей бизнеса — от Vision до Use Cases. Методология Вигерса.

#### 5.2.1 Vision & Scope
- **FR-RM-01**: Создание Vision & Scope документа (бизнес-требования, видение решения, границы, контекст)
- **FR-RM-02**: AI-ассистент для формулирования: пользователь описывает идею → AI задаёт уточняющие вопросы → генерирует структурированный документ
- **FR-RM-03**: Версионирование и diff между версиями
- **FR-RM-04**: Collaborative editing с комментариями

#### 5.2.2 Stakeholder Management
- **FR-RM-10**: Профили стейкхолдеров (роль, интересы, влияние, отношение)
- **FR-RM-11**: Impact x Interest матрица
- **FR-RM-12**: Генерация вопросов для интервью по профилю стейкхолдера

#### 5.2.3 Requirements Elicitation
- **FR-RM-20**: План элиситации (техники, участники, график)
- **FR-RM-21**: AI-ассистированные интервью: AI предлагает вопросы на основе контекста
- **FR-RM-22**: Автоматическое извлечение требований из протоколов встреч и документов Knowledge Base (P6: knowledge → requirements pipeline)

#### 5.2.4 Use Cases
- **FR-RM-30**: Создание Use Cases (brief / casual / fully-dressed по Cockburn)
- **FR-RM-31**: AI-генерация альтернативных и исключительных потоков
- **FR-RM-32**: Трассировка: Use Case → requirement → spec → код → тест

#### 5.2.5 Requirements Quality
- **FR-RM-40**: Автоматическая проверка качества по 8 критериям Вигерса (корректность, осуществимость, необходимость, приоритизация, однозначность, верифицируемость, полнота, непротиворечивость)
- **FR-RM-41**: AI-рецензент: находит ambiguity, gaps, contradictions
- **FR-RM-42**: Quality dashboard по набору требований

### 5.3 Module: Backlog & Specs

> Управление работой — от идеи до готовой спецификации.

#### 5.3.1 Backlog Management
- **FR-BL-01**: Quick capture: идея / баг / фича / улучшение — текстом, голосом, из Slack/email, от агента (P6: code-to-ticket feedback)
- **FR-BL-02**: AI-обогащение: автоматическое определение типа, приоритета, area, связей с существующими items (как Linear Triage Intelligence)
- **FR-BL-03**: Фильтрация и группировка: по типу, приоритету, area, epic, assignee (human или agent)
- **FR-BL-04**: Epics: группировка items, прогресс, зависимости
- **FR-BL-05**: Explore mode: AI-исследование feasibility без изменения кода (read-only анализ codebase)
- **FR-BL-06**: Приоритизация: ручная + AI-assisted scoring (формула вдохновлена ClickUp: `Priority Score = (User Impact x 3) + (Technical Risk x 2) + (Effort) + (Dependency Count)`)
- **FR-BL-07**: Duplicate detection (как Linear Triage)
- **FR-BL-08**: Wave planning: группировка независимых задач для параллельного запуска агентов (P4)

#### 5.3.2 Spec-Driven Development (OpenSpec)
- **FR-BL-10**: Change workflow: new → proposal → design → tasks → implement → verify → archive
- **FR-BL-11**: Артефакты change: proposal.md (что и зачем), design.md (как), tasks.md (декомпозиция) — аналог 3-фазного workflow Kiro (requirements.md → design.md → tasks.md)
- **FR-BL-12**: Delta specs: изменения к существующим спецификациям, с последующим sync в main specs
- **FR-BL-13**: Dependency tracking между changes
- **FR-BL-14**: AI-генерация артефактов (P2: propose-review): пользователь описывает intent → AI создаёт proposal → human review → AI создаёт design → human review → AI создаёт tasks
- **FR-BL-15**: Fast-forward mode: генерация всех артефактов за один шаг (для опытных пользователей)

#### 5.3.3 Traceability
- **FR-BL-20**: Полная цепочка: business need → requirement → spec → task → PR → deploy
- **FR-BL-21**: Impact analysis: "Если изменить требование X, что затронется?"
- **FR-BL-22**: Coverage: "Какие требования ещё не покрыты спецификациями/кодом?"
- **FR-BL-23**: Bi-directional links: изменение в коде пропагируется к specs (P6)

### 5.4 Module: Agent Interface (P8: Tool Provider)

> Bobr не запускает агентов — Bobr предоставляет данные и инструменты, с которыми агенты работают. Любой AI-агент (Claude Code, Cursor, Codex, Devin, Jules, Copilot) может использовать Bobr через файлы, CLI или MCP.

#### 5.4.1 L1: File-based Interface (.bobr/)
- **FR-AI-01**: `.bobr/` формат полностью документирован и machine-readable (YAML frontmatter + Markdown)
- **FR-AI-02**: Агент может читать/писать backlog items, specs, requirements, changes напрямую как файлы
- **FR-AI-03**: Формат валидируется: `bobr validate` проверяет корректность .bobr/ структуры после ручного или агентского редактирования
- **FR-AI-04**: `.bobr/AGENTS.md` — автогенерируемый файл-инструкция для агента, собирающий контекст из requirements + specs + conventions

#### 5.4.2 L2: CLI Interface
- **FR-AI-10**: Все CLI-команды поддерживают `--output json` для machine-readable output
- **FR-AI-11**: `bobr backlog add/list/edit/drop/promote` — управление бэклогом
- **FR-AI-12**: `bobr change new/continue/verify/archive` — управление changes
- **FR-AI-13**: `bobr context generate` — сборка контекста для агента (specs + requirements + knowledge → AGENTS.md / CLAUDE.md)
- **FR-AI-14**: `bobr status` — текущее состояние проекта (active changes, backlog summary, recent activity)
- **FR-AI-15**: Exit codes и structured errors для machine consumption

#### 5.4.3 L3: MCP Server
- **FR-AI-20**: Bobr MCP Server (Streamable HTTP) — AI-агенты подключают Bobr как MCP tool provider
- **FR-AI-21**: MCP tools: `read_backlog`, `add_backlog_item`, `get_change`, `create_change`, `read_spec`, `search_knowledge`, `get_project_status`
- **FR-AI-22**: Dynamic tool descriptions: MCP tools включают текущий project context в описаниях (агент знает что за проект)
- **FR-AI-23**: OAuth 2.1 авторизация для cloud-hosted MCP server (как Linear MCP)

#### 5.4.4 Context Generation (P7)
- **FR-AI-30**: `bobr context generate` собирает: relevant specs + requirements + active changes + conventions → один файл
- **FR-AI-31**: Smart context selection: включает только релевантные specs для конкретной задачи (по dependency graph)
- **FR-AI-32**: Negative constraints: секция "DO NOT" в сгенерированном контексте
- **FR-AI-33**: Per-agent format: `--format claude` (CLAUDE.md), `--format codex` (AGENTS.md), `--format cursor` (.cursorrules)

#### 5.4.5 Agent Activity Tracking
- **FR-AI-40**: Агент регистрирует свою работу: `bobr activity log --agent "claude-code" --task BL-42 --action "created PR #123"`
- **FR-AI-41**: Автоматический tracking через MCP (каждый tool call логируется)
- **FR-AI-42**: Cost tracking: агент (или wrapper) сообщает token usage через `bobr activity cost --tokens-in X --tokens-out Y`
- **FR-AI-43**: Agent efficiency dashboard (web UI, later phases): cycle time by agent type, success rate, cost per task

### 5.5 Module: Delivery Pipeline

> От PR до production. Event-driven (P5).

#### 5.5.1 PR Management
- **FR-DP-01**: Автоматическое создание PR из результата работы агента
- **FR-DP-02**: AI Code Review: автоматический review по conventions проекта (как "blind validation" в Zeroshot — reviewer не видит контекст implementer-а)
- **FR-DP-03**: Link PR → task → spec → requirement (traceability)
- **FR-DP-04**: Human review workflow: assign reviewer, approve/request changes

#### 5.5.2 Preview Deployments
- **FR-DP-10**: Автоматический deploy preview для каждого PR (Render, Vercel, Netlify)
- **FR-DP-11**: Preview URL в PR description и в dashboard
- **FR-DP-12**: Stakeholder review на preview: комментарии привязаны к PR и задаче

#### 5.5.3 Verification & Feedback
- **FR-DP-20**: Автоматическая верификация: acceptance criteria из spec → AI проверяет реализацию
- **FR-DP-21**: Test coverage check: новый код покрыт тестами
- **FR-DP-22**: Spec coherence check: реализация соответствует design.md
- **FR-DP-23**: Post-merge reflection (P6): AI анализирует diff, создаёт follow-up backlog items, обновляет specs

### 5.6 Module: Team Collaboration

> Прозрачность и alignment для всей команды.

#### 5.6.1 Activity Feed
- **FR-TC-01**: Единый feed: кто (человек/агент) что сделал, когда, в контексте какой задачи
- **FR-TC-02**: Фильтры: по проекту, участнику, типу активности
- **FR-TC-03**: @mentions и нотификации (human и agent — как Linear for Agents)

#### 5.6.2 Collaborative Editing
- **FR-TC-10**: Real-time collaborative editing требований, specs, briefs
- **FR-TC-11**: Комментарии и threads на любом артефакте
- **FR-TC-12**: Review & approval workflows (P2: propose-review)

#### 5.6.3 Team Dashboard
- **FR-TC-20**: Overview: active changes, backlog breakdown, agent utilization, delivery velocity, cost
- **FR-TC-21**: Per-person view: мои задачи, мои PR, мои reviews (включая "мои агенты")
- **FR-TC-22**: Project health: requirements coverage, spec freshness, test coverage, agent success rate

### 5.8 Module: Consumer Interfaces

> Bobr Core — tool provider. Consumers — интерфейсы, через которые люди и агенты взаимодействуют с Bobr. Стратегия: НЕ строить свой UI, пока существующие consumers закрывают потребность.

```
┌─────────────────────────────────────────────────────────────┐
│                    Consumers (интерфейсы)                     │
├────────────┬───────────────┬─────────────┬──────────────────┤
│ Claude Code│ Claude Cowork │ Telegram Bot│ Web UI           │
│ (CTO,devs) │ (CEO,CFO,PM)  │ (все,mobile)│ (dashboard)      │
│ Phase 0    │ Phase 1       │ Phase 1–2   │ Phase 3 (опц.)   │
├────────────┴───────────────┴─────────────┴──────────────────┤
│          L1: .bobr/ files  │  L2: CLI  │  L3: MCP Server    │
├─────────────────────────────────────────────────────────────┤
│                        Bobr Core                             │
└─────────────────────────────────────────────────────────────┘
```

#### 5.8.1 Claude Cowork как интерфейс для нетехнических пользователей (Phase 1)

Claude Cowork — агентный режим в Claude Desktop ("Claude Code для остальной работы"). Ключевые возможности для Bobr:

- **MCP поддержка**: Cowork подключает custom MCP серверы (local и remote, Streamable HTTP)
- **Файловая система**: Cowork читает/пишет файлы — работает с `.bobr/` напрямую (L1)
- **Shell commands**: Cowork может вызывать `bobr` CLI (L2)
- **Connectors**: Встроенные (Gmail, GitHub, Slack, Google Drive) + custom через MCP
- **Доступность**: macOS/Windows, платные планы (Pro, Max, Team, Enterprise)

**Сценарии для CEO/CFO через Cowork**:

| Что делает Костя (CEO) | Как Cowork обрабатывает |
|------------------------|------------------------|
| "Покажи бэклог Apilize" | MCP → `read_backlog` → таблица с приоритетами |
| "Добавь задачу: клиент просит экспорт в PDF" | MCP → `add_backlog_item` → подтверждение |
| "Какой статус задачи BL-15?" | MCP → `get_item` → статус, assignee, связанный PR |
| "Подготовь summary для встречи с клиентом" | MCP → `search_knowledge` + `read_backlog` → сводка |
| "Что изменилось за последнюю неделю?" | MCP → `get_project_status` → activity feed |

**Почему не свой Web UI сразу**: Claude Cowork уже есть, умеет MCP, визуализирует данные, отвечает на естественном языке. Bobr не тратит ресурсы на UI, а фокусируется на Core.

#### 5.8.2 Telegram Bot (Phase 1–2)

Тонкий адаптер над Bobr L2 (CLI) / L3 (MCP). Мобильный доступ для всех участников.

- **FR-TG-01**: Команды бота: `/status`, `/backlog`, `/task <id>`, `/add <title>`
- **FR-TG-02**: Уведомления: PR created, preview ready, review requested, task completed
- **FR-TG-03**: Inline-ответы: бот показывает preview link, статус задачи
- **FR-TG-04**: Natural language: "что нового?" → вызов `bobr status`
- **FR-TG-05**: Multi-project: бот привязан к нескольким проектам, переключение через `/project <name>`
- **FR-TG-06**: Permissions: read-only для viewers, write для members+

**Архитектура**: Telegram Bot → Bobr CLI (`--output json`) или MCP client → ответ пользователю.

#### 5.8.3 Web UI (Phase 3, опциональный)

Web UI становится **опциональным** — для пользователей, не использующих Claude Cowork, и для публичных dashboards.

- Dashboard: project overview, backlog kanban, activity feed
- Stakeholder view: read-only для клиентов (preview links, progress)
- Admin: project settings, agent config, cost controls
- Knowledge Browser: search, upload, browse documents

**Решение о приоритете Web UI принимается в Phase 2** — на основе feedback от Кости/Ивана: достаточно ли Cowork + Telegram?

### 5.9 Module: Bobr Runner (Phase 4+)

> Bobr Core — tool provider без AI. Bobr Runner — оркестратор внешних AI-агентов, аналогичный GitHub Actions runners. Runner запускает агентов, Core предоставляет им данные и инструменты.

#### 5.8.1 Концепция

Bobr Runner — **отдельный компонент**, который:
- Принимает команду "Запустить задачу" из Web UI или API
- Создаёт isolated environment (worktree, sandbox)
- Запускает внешнего AI-агента (Claude Code, Codex, Devin) с context injection
- Мониторит прогресс, cost, статус
- Собирает результат (PR, preview link)

**Ключевое различие**: Runner ≠ AI. Runner оркестрирует AI-агентов, как GitHub Actions оркестрирует CI/CD runners. Runner сам по себе не содержит LLM — он вызывает внешние агенты через их API/CLI.

#### 5.8.2 Функциональные требования
- **FR-RN-01**: Запуск задачи из Web UI: кнопка «Запустить» для любого backlog item или change
- **FR-RN-02**: Выбор агента: Claude Code, Codex, Devin, custom — пользователь или система выбирает подходящего
- **FR-RN-03**: Automatic context injection: Runner вызывает `bobr context generate` перед запуском агента
- **FR-RN-04**: Isolated execution: worktree + sandbox (Docker или аналог)
- **FR-RN-05**: Real-time monitoring: live logs, token usage, статус в Web UI
- **FR-RN-06**: Result collection: PR link, preview URL, agent report → привязка к task
- **FR-RN-07**: Cost controls: budget limit per task, per user, per project
- **FR-RN-08**: Queue management: приоритизация запусков, concurrency limits

#### 5.8.3 Архитектурная позиция

```
┌─────────────────────────────────────────────────────┐
│                 Web UI / API                         │
│            (человек нажимает «Запустить»)             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                  Bobr Runner                         │
│  (оркестрирует внешних агентов,                      │
│   аналог GitHub Actions runner)                      │
│  • Создаёт worktree                                  │
│  • Вызывает bobr context generate                    │
│  • Запускает агента (Claude Code CLI, Codex API)     │
│  • Мониторит прогресс, cost                          │
│  • Собирает результат (PR, preview)                  │
└──────────────────────┬──────────────────────────────┘
                       │ использует
                       ▼
┌─────────────────────────────────────────────────────┐
│                  Bobr Core                           │
│  (zero AI dependency — tool provider)                │
│  L1: .bobr/ files │ L2: CLI │ L3: MCP Server        │
└─────────────────────────────────────────────────────┘
```

### 5.7 Module: External Integrations

> Синхронизация с внешними системами и автоматизация.

#### 5.7.1 Bidirectional Sync
- **FR-IL-10**: Import из Jira/Linear/GitHub Issues → Bobr backlog
- **FR-IL-11**: Export из Bobr → Jira/Linear (для enterprise, где Jira — system of record)
- **FR-IL-12**: Continuous sync mode: изменения в обоих направлениях

#### 5.7.2 Automation Hooks
- **FR-IL-20**: Event-driven hooks (P5): on_task_created, on_pr_merged, on_review_approved
- **FR-IL-21**: Webhook integrations: Slack notifications, GitHub Actions triggers
- **FR-IL-22**: n8n / Zapier compatibility: HTTP webhooks для no-code automation

#### 5.7.3 Git & Deploy
- **FR-IL-30**: GitHub/GitLab integration: PR creation, status checks, webhooks
- **FR-IL-31**: Deploy preview: Render/Vercel/Netlify PR preview linking
- **FR-IL-32**: PR ↔ task ↔ spec linking (traceability через git metadata)

---

## 6. Нефункциональные требования

### 6.1 Архитектура

- **NFR-01**: Multi-tenant SaaS с возможностью self-hosted deployment
- **NFR-02**: API-first: все функции доступны через REST API
- **NFR-03**: CLI-first: основные операции доступны из терминала (для разработчиков и агентов)
- **NFR-04**: Git-native + Cloud-synced: артефакты в git, метаданные/embeddings/sessions в cloud
- **NFR-05**: Event-driven: все действия генерируют события (P5)
- **NFR-06**: Tool Provider: Bobr — инструмент для AI-агентов (L1: files, L2: CLI, L3: MCP), не AI consumer. Zero LLM dependency в ядре
- **NFR-07**: Agent-agnostic: работает с любым агентом, который умеет читать файлы, вызывать CLI или подключать MCP

### 6.2 Производительность

- **NFR-10**: Время запуска агента на задачу: < 30 секунд
- **NFR-11**: Real-time updates в dashboard: < 2 секунды задержки
- **NFR-12**: Семантический поиск по knowledge base: < 3 секунды
- **NFR-13**: Context injection assembly: < 5 секунд (relevance scoring + retrieval)

### 6.3 Безопасность

- **NFR-20**: SSO (Auth0 / OIDC) + API key authentication
- **NFR-21**: Role-based access: Owner, Admin, Member, Viewer, Agent (agent как first-class role)
- **NFR-22**: Audit log всех действий — человек и агент равноправны в audit trail
- **NFR-23**: Secrets management: API ключи агентов в vault, не в plaintext
- **NFR-24**: Изоляция tenant-ов на уровне данных

### 6.4 Интеграции

- **NFR-30**: Git hosting: GitHub (primary), GitLab, Bitbucket
- **NFR-31**: Deploy: Render (primary), Vercel, Netlify, Fly.io
- **NFR-32**: Communication: Slack, email (Gmail/Outlook)
- **NFR-33**: AI Agents (через L1/L2/L3): Claude Code, Cursor, Codex, Copilot, Devin, Jules, custom — любой, без привязки
- **NFR-34**: PM Import: Jira, Linear, GitHub Issues, Notion
- **NFR-35**: Middleware: Composio (250+ tools), n8n

---

## 7. Информационная архитектура

### 7.1 Domain Model

```
Organization
├── Project
│   ├── Knowledge Base
│   │   ├── Document (PDF, DOCX, MD, ...)
│   │   ├── Meeting (transcript, summary, action items)
│   │   ├── Communication (email thread, Slack thread)
│   │   └── Journal Entry (auto/manual)
│   │
│   ├── Requirements
│   │   ├── Vision & Scope
│   │   ├── Stakeholder Profile
│   │   ├── Use Case
│   │   └── Requirement (functional / non-functional)
│   │
│   ├── Backlog
│   │   ├── Epic
│   │   │   └── Item (bug / feature / idea / improvement)
│   │   ├── Item (unassigned to epic)
│   │   └── Wave (group of independent items for parallel execution)
│   │
│   ├── Specs (OpenSpec)
│   │   ├── Spec (domain/feature specification)
│   │   └── Change
│   │       ├── Proposal
│   │       ├── Design
│   │       ├── Tasks
│   │       └── Delta Specs
│   │
│   ├── Delivery Pipeline
│   │   ├── Agent Session (running agent instance)
│   │   ├── Pull Request
│   │   ├── Preview Deployment
│   │   └── Post-Merge Reflection
│   │
│   └── Runner (Phase 4+)
│       ├── Run (agent execution instance)
│       ├── Run Log (real-time output)
│       └── Cost Record (tokens, time, $)
│
├── Member (human, with role)
├── Agent (AI agent identity, with provider + cost tracking)
└── Integration (MCP server / external PM sync)
```

### 7.2 Git-native структура (`.bobr/`)

```
project-repo/
├── .bobr/
│   ├── config.yaml              # Project settings, agent defaults
│   ├── AGENTS.md                # Auto-generated agent instructions
│   ├── knowledge/
│   │   ├── documents/           # Uploaded docs (or symlinks)
│   │   ├── meetings/            # Transcripts + summaries
│   │   └── journal.md           # Auto-generated project journal
│   ├── requirements/
│   │   ├── vision-and-scope.md
│   │   ├── stakeholders/
│   │   │   └── <name>.md
│   │   ├── use-cases/
│   │   │   └── <UC-id>.md
│   │   └── requirements.md      # Functional + non-functional
│   ├── backlog/
│   │   ├── INDEX.md             # Master table (ID, Type, Priority, Title, Area, Epic, Assignee)
│   │   ├── epics/
│   │   │   └── <slug>.md
│   │   ├── bug-*.md
│   │   ├── feature-*.md
│   │   ├── idea-*.md
│   │   └── improvement-*.md
│   └── specs/
│       ├── <spec-name>/
│       │   └── spec.md
│       └── changes/
│           ├── <change-name>/
│           │   ├── proposal.md
│           │   ├── design.md
│           │   └── tasks.md
│           └── archive/
├── src/
└── ...
```

### 7.3 Ключевые связи и feedback loops

```
                    ┌──────────────────────────────┐
                    │        Knowledge Base         │
                    │  (docs, meetings, emails)     │
                    └──────────┬───────────────────┘
                               │ extracts
                               ▼
┌──────────────┐    ┌──────────────────────┐    ┌──────────────────┐
│ Requirements │◄───│     Backlog Items     │───►│   Specs/Changes  │
│ (Vision, UC) │    │ (bug,feature,idea)   │    │ (proposal→tasks) │
└──────┬───────┘    └──────────┬───────────┘    └────────┬─────────┘
       │                       │                         │
       │ traces-to             │ promotes                │ implements
       ▼                       ▼                         ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Agent Orchestration                            │
│  context injection → isolated worktree → execute → PR            │
└──────────────────────────────┬───────────────────────────────────┘
                               │ produces
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Delivery Pipeline                              │
│  PR → AI review → human review → preview deploy → merge          │
└──────────────────────────────┬───────────────────────────────────┘
                               │ post-merge reflection (P6)
                               ▼
                    ┌──────────────────────┐
                    │  Follow-up items +   │──► Backlog (loop)
                    │  Spec updates        │──► Specs (loop)
                    └──────────────────────┘
```

---

## 8. User Flows

### 8.1 Flow: От идеи до production (happy path)

```
1. PM записывает идею (текст/голос/Slack/email) ──► Backlog Item создан
2. AI обогащает: тип, приоритет, area, дубликаты, связи ──► Item enriched
3. PM запускает /explore ──► AI анализирует codebase, оценивает feasibility (read-only)
4. PM дополняет контекст из Knowledge Base ──► Item обогащён
5. PM делает /promote ──► Создаётся Change
6. AI генерирует proposal.md ──► Human review (P2: propose-review)
7. AI генерирует design.md ──► Human review
8. AI генерирует tasks.md с acceptance criteria ──► Human review
9. Wave planner определяет: можно запустить параллельно? (P4)
10. Agent(s) берут задачи ──► Context injection (P7): spec + requirements + knowledge
11. Agent(s) пишут код в isolated worktrees (P4)
12. PR создан ──► Preview deploy (Render)
13. AI Code Review (P2: blind validation) ──► Auto-review
14. Human Review ──► Developer проверяет PR
15. /verify ──► AI проверяет acceptance criteria
16. Merge ──► Production deploy
17. Post-merge reflection (P6) ──► Follow-up items в backlog, specs updated
18. /archive ──► Change архивирован
```

### 8.2 Flow: Обработка встречи с клиентом

```
1. Загрузка транскрипта встречи ──► Knowledge Base
2. AI извлекает: решения, action items, открытые вопросы
3. Action items ──► автоматически создаются Backlog Items
4. Решения ──► обновляют Requirements / Project Journal
5. Открытые вопросы ──► создаются задачи для follow-up
```

### 8.3 Flow: Параллельная разработка (Wave)

```
1. PM/Lead отмечает 5 задач как ready
2. Wave planner анализирует file-зависимости ──► 3 задачи независимы, 2 конфликтуют
3. Wave 1: 3 агента запускаются параллельно в worktrees
4. Dashboard: real-time прогресс, cost, статус
5. 2 из 3 завершены ──► PR created, preview deployed
6. 1 stuck ──► Alert, human intervention или retry
7. Wave 2: оставшиеся 2 задачи (после merge Wave 1)
```

### 8.4 North Star Flow: Костя (CEO) запускает задачу

> Целевой сценарий — когда Bobr полностью реализован. Не Phase 0.

```
1. Костя открывает Web UI Bobr ──► видит бэклог, приоритеты, статусы
2. Костя выбирает задачу (или создаёт новую из разговора с клиентом)
3. Нажимает «Запустить» ──► Bobr Runner создаёт Change
4. Runner запускает внешнего AI-агента (Claude Code / Codex) в isolated worktree
   ► Агент получает context injection: spec + requirements + knowledge
   ► Bobr — tool provider (L1/L2/L3), агент — executor
5. Dashboard показывает real-time прогресс: код пишется, тесты проходят
6. PR создан ──► Preview deploy (Render) ──► Костя получает ссылку
7. Костя кликает Preview, смотрит результат, оставляет комментарий
8. Артём (CTO) делает code review ──► Merge ──► Production
```

**Фазирование**:
- **Phase 0**: Артём работает через Claude Code. Костя/Иван ещё не подключены
- **Phase 1**: Костя/Иван подключают Bobr MCP в Claude Cowork → видят бэклог, добавляют задачи, задают вопросы
- **Phase 2**: Telegram bot → Костя получает уведомления (PR ready, preview link) на телефон
- **Phase 4+**: Кнопка «Запустить» (Bobr Runner) → Костя запускает агентов без участия CTO

### 8.5 Flow: Новый член команды (onboarding)

```
1. Invite → Member присоединяется к Organization
2. AI-сгенерированный onboarding brief:
   - Vision & Scope (из requirements)
   - Ключевые архитектурные решения (из specs)
   - Текущий статус (из backlog + active changes)
   - Важные решения (из project journal)
3. Knowledge Base доступна для self-service Q&A
4. Первая задача: AI подбирает подходящий по сложности item из бэклога
```

---

## 9. Приоритизация (MoSCoW)

### Must Have (MVP)

| ID | Feature | Обоснование |
|----|---------|-------------|
| M1 | Backlog management (add, list, edit, explore, promote, drop, epics) | Ядро workflow, validated на Expecto (68+ items, 9 commands) |
| M2 | Change workflow (new → proposal → design → tasks → verify → archive) | Ядро spec-driven dev, validated (64 archived changes) |
| M3 | Agent execution: Claude Code на задачу в isolated worktree + context injection | Ключевая ценность; proven (CCPM: 12 parallel agents) |
| M4 | PR creation + deploy preview (Render) | Замыкает delivery loop |
| M5 | Knowledge Base: документы + семантический поиск | Критично для context quality |
| M6 | Team: invite, roles (incl. Agent role), activity feed | Без этого нет "team product" |
| M7 | CLI interface | Developers и агенты работают из терминала |
| M8 | MCP Server (stdio + Streamable HTTP) | Стандарт де-факто; агенты и Claude Cowork подключаются нативно |

### Should Have (v1.1)

| ID | Feature | Обоснование |
|----|---------|-------------|
| S1 | Requirements management (Vision & Scope, Use Cases) | Differentiator; validated через Wiegers plugin |
| S2 | Meeting intelligence (transcript → action items → backlog) | Сильно сокращает manual work; Knowledge → Backlog pipeline |
| S3 | Multi-agent parallel execution (Wave planning, P4) | Proven: Claude Forge 39 фич за сессию |
| S4 | AI Code Review (blind validation, P2) | Качество без human bottleneck |
| S5 | Traceability (requirement → spec → code → test) | Прозрачность для PM и stakeholders |
| S6 | Cost tracking + agent analytics (P3) | Token budget as capacity planning |
| S7 | Post-merge reflection (P6) | Feedback loop: code → backlog → specs |
| S8 | Telegram Bot (commands + notifications) | Мобильный доступ для всей команды; event-driven уведомления |

### Could Have (v1.2+)

| ID | Feature | Обоснование |
|----|---------|-------------|
| C1 | Stakeholder profiles + elicitation planning | Полный Wiegers workflow |
| C2 | Web UI (dashboard, kanban, knowledge browser) | Опционально — Claude Cowork + Telegram покрывают основные сценарии |
| C2a | Collaborative real-time editing | Удобство, но не блокер |
| C3 | Slack/email integration (communication archive) | Автоматизация capture |
| C4 | Multi-provider agents (Codex, Cursor, Copilot) | Расширение аудитории |
| C5 | Bidirectional Jira/Linear sync | Enterprise migration path |
| C6 | Self-hosted deployment | Enterprise requirement |
| C7 | Wave planner AI (file-conflict detection) | Оптимизация параллелизма |
| C8 | Agent Skills system (reusable instructions) | Как Codex Skills |

### Won't Have (сейчас)

- **Sprint planning / velocity tracking** — анти-паттерн для AI-first (Scrum.org)
- **Story points** — заменены token budgets (P3)
- **Gantt charts / Time tracking** — не релевантно для agent-first
- **Multi-agent role simulation** (MetaGPT style) — overhead, не нужно для реальных команд
- **IDE** — мы не конкурируем с Cursor/Kiro, мы оркестрируем их

---

## 10. Технический стек

### 10.1 Архитектура

Bobr — tool provider. AI-агенты работают с Bobr, а не наоборот.

```
┌─────────────────────────────────────────────────────────────────┐
│                  AGENTS (пишут код, external)                     │
│  Claude Code │ Cursor │ Codex │ Devin │ Jules │ Copilot │ ...   │
├─────────────────────────────────────────────────────────────────┤
│                  CONSUMERS (интерфейсы для людей)                 │
│  Claude Cowork (CEO/CFO) │ Telegram Bot (mobile) │ Web UI (опц.)│
├──────┬───────────────┬──────────────────────────────────────────┤
│      │               │                                          │
│  L1: Files       L2: CLI              L3: MCP Server            │
│  .bobr/* r/w     bobr --output json   Streamable HTTP           │
│      │               │                     │                    │
├──────┴───────────────┴─────────────────────┴────────────────────┤
│                        API (FastAPI)                               │
├───────────┬───────────┬───────────┬─────────────────────────────┤
│ Knowledge │ Require-  │ Backlog   │ External                    │
│ Base      │ ments     │ & Specs   │ Integrations                │
│ Service   │ Service   │ Service   │ (Jira, GitHub, Render, ..)  │
├───────────┴───────────┴───────────┴─────────────────────────────┤
│      PostgreSQL + pgvector  │  S3/MinIO   │  Redis (events/q)   │
├─────────────────────────────┴─────────────┴─────────────────────┤
│                .bobr/ (git-native file storage)                   │
└─────────────────────────────────────────────────────────────────┘
```

### 10.2 Выбор технологий

| Layer | Technology | Обоснование |
|-------|-----------|-------------|
| Backend API | Python / FastAPI | Опыт команды (Expecto), async, быстрый |
| Frontend | React + TypeScript + Tailwind | Опыт команды, зрелая экосистема |
| Database | PostgreSQL + pgvector | Multi-tenant, JSONB, vector search — один сервис вместо двух |
| File storage | S3 / MinIO | Документы, транскрипты, артефакты |
| Queue/Events | Redis + arq | Event bus (P5), async jobs |
| CLI | Python (Typer) | L2 agent interface; `--output json` на всех командах |
| MCP Server | Streamable HTTP (Python) | L3 agent interface; стандарт, OAuth 2.1 |
| Auth | Auth0 | Проверено на Expecto, SSO ready |
| Deploy | Render | Proven, PR preview из коробки |

**Намеренно отсутствует**: AI/LLM dependency. Bobr не вызывает Claude API, OpenAI или Google AI. Вся AI-логика — на стороне агентов, работающих с Bobr.

### 10.3 Двойное хранение (Git + Cloud)

| Что | Где | Почему |
|-----|-----|--------|
| Specs, requirements, backlog items | `.bobr/` в git | Версионируются с кодом; агент читает из FS; портабельность |
| Embeddings, search indices | PostgreSQL + pgvector | Быстрый семантический поиск |
| Agent sessions, logs, cost | PostgreSQL + S3 | Audit trail, analytics |
| User data, roles, permissions | PostgreSQL | Multi-tenant security |
| Event stream | Redis | Real-time updates, webhook triggers |
| Large files (docs, recordings) | S3 | Не засоряют git |

---

## 11. Метрики успеха

### 11.1 North Star Metric

**Количество задач, доставленных до production за неделю на команду.**

### 11.2 Ключевые метрики

| Метрика | Цель (6 месяцев) | Как измеряем |
|---------|------------------|-------------|
| Cycle time (idea → production) | < 4 часов для типовой фичи | Timestamps в workflow |
| Agent success rate | > 80% задач без human intervention | Agent session outcomes |
| Context quality score | > 4/5 | Developer feedback |
| Team adoption | 100% команды ежедневно | DAU / team size |
| Requirements coverage | > 90% specs traced to requirements | Traceability report |
| Agent cost per task | < $2 среднее | Token tracking |

### 11.3 Guardrail Metrics

| Метрика | Порог | Действие |
|---------|-------|----------|
| PR rejection rate | < 20% | Улучшение specs / context injection quality |
| Agent stuck rate | < 10% | Улучшение error recovery / task decomposition |
| Knowledge base staleness | < 30 дней avg | Auto-reminders |
| Spec-code drift | < 5% | Auto-detection + follow-up items (P6) |

---

## 12. Dogfooding Strategy

### 12.1 Принцип

**Bobr разрабатывается с помощью Bobr как можно раньше.** Это не просто идеологическое решение — это архитектурный constraint, определяющий порядок разработки и критерий готовности каждой фазы.

> *"Если мы сами не можем использовать свой инструмент для его же разработки, он не готов для пользователей."*

### 12.2 Bootstrapping Sequence

Проблема курицы и яйца: чтобы управлять бэклогом Bobr в Bobr, нужно сначала создать Bobr. Решение — **инкрементальный bootstrap**:

```
Phase 0 (сейчас):
  PRD — этот документ. Code пишет Claude Code.
  Claude Code читает PRD напрямую (L1: files) — AI на стороне агента.

Phase 0 done (Week 3):
  bobr init создаёт .bobr/ в репозитории Bobr
  bobr backlog add/list работает (L2: CLI)
  ► Claude Code использует bobr CLI + читает .bobr/ файлы

Phase 1 (Week 5–6):
  Change workflow + MCP server работают
  Claude Code подключает Bobr MCP Server (L3)
  ► Каждая фича Bobr — Change с proposal + design + tasks
  ► Костя/Иван подключают Bobr MCP в Claude Cowork
  ► Нетехнические пользователи работают с бэклогом через Cowork

Phase 2 (Week 9–10):
  bobr context generate + Telegram bot
  ► Claude Code получает CLAUDE.md из .bobr/specs/ + requirements
  ► PR creation + deploy preview через Bobr
  ► Костя получает preview links и уведомления в Telegram

Phase 3 (Week 13+):
  Knowledge Base + Team
  ► PRD, research docs — в Knowledge Base
  ► Команда (3 человека) работает в Bobr: Code + Cowork + Telegram
  ► Web UI — по результатам feedback (опционально)

Full loop (Week 15+):
  Requirement → Spec → Change → Agent (external) → PR → Preview → Verify → Archive
  ► Весь цикл. Bobr — tool provider, агенты и consumers — executors и interfaces.
```

### 12.3 Acceptance Criteria для каждой фазы

Каждая фаза считается завершённой только когда **Bobr начинает использовать результат этой фазы для собственной разработки**:

| Фаза | Acceptance Criteria (dogfooding) | Agent level |
|------|----------------------------------|-------------|
| Phase 0 | `.bobr/` структура в репозитории Bobr; backlog items через CLI; Claude Code читает `.bobr/` | L1 + L2 |
| Phase 1 | Каждая фича — Change; Claude Code подключает MCP; Костя/Иван работают через Claude Cowork + MCP | L1 + L2 + L3 |
| Phase 2 | Агенты получают контекст через `bobr context generate`; PR → preview; Telegram bot с уведомлениями | L1 + L2 + L3 + context + Telegram |
| Phase 3 | PRD и docs в Knowledge Base; команда 3+ человек в Bobr ежедневно (Code + Cowork + Telegram) | Full stack |
| Phase 4 | CEO запускает задачу через Web UI → получает Preview link. Multi-agent waves | Full stack + Runner |
| Full loop | 100% фич: backlog → change → agent (external) → PR → verify → archive | Full stack + Runner |

### 12.4 Почему это важно

1. **Fastest feedback loop**: Мы — самые мотивированные пользователи. Проблемы UX обнаруживаются мгновенно.
2. **Proof of concept**: Если Bobr может построить Bobr, он может построить что угодно.
3. **Determines priority**: Фичи, нужные для собственной разработки, автоматически оказываются наверху бэклога — это правильная приоритизация.
4. **Prevents over-engineering**: Если фича не нужна нам самим сейчас — она точно не нужна в MVP.
5. **Marketing story**: "Built with itself" — мощный social proof (как Rust compiler, написанный на Rust).

### 12.5 Практические следствия для архитектуры

| Следствие | Влияние на дизайн |
|-----------|-------------------|
| CLI должен работать раньше Web UI | Phase 0.5 — CLI only; Web UI — Phase 3 |
| `.bobr/` формат — первый артефакт | Специфицируется и реализуется до API/DB |
| Single-user mode должен работать без сервера | CLI + git-native = полностью локальный workflow; server — для team features |
| Миграция из OpenSpec должна быть автоматической | `bobr migrate --from openspec` — часть Phase 0.5 |
| Bobr не вызывает AI | Zero LLM dependency; агенты работают с Bobr, не наоборот |
| L1 (files) работает сразу, L2 (CLI) — Phase 0, L3 (MCP) — Phase 1 | Инкрементальное расширение agent interface |

---

## 13. Roadmap

> Roadmap переструктурирован вокруг dogfooding milestones. Каждая фаза заканчивается переключением собственной разработки на новую capability.

### Phase 0: Bootstrap (Weeks 1–3)

**Цель**: `.bobr/` формат + CLI для бэклога (L1 + L2). К концу фазы бэклог Bobr ведётся в Bobr.

**Dogfooding milestone**: Бэклог Bobr создан в `.bobr/`, все новые items через CLI.

**Agent interface level**: L1 (files) + L2 (CLI)

- [ ] `.bobr/` format specification (YAML frontmatter + Markdown)
- [ ] CLI scaffolding (Python/Typer): `bobr init`
- [ ] `bobr backlog add` / `list` / `edit` / `drop` (с `--output json`)
- [ ] `bobr validate` — проверка корректности .bobr/ структуры
- [ ] `bobr status` — текущее состояние проекта (machine-readable)
- [ ] INDEX.md auto-generation
- [ ] **Создать бэклог Bobr** — PRD items → `.bobr/backlog/`
- [ ] Git-native storage: все операции = file writes + git commits

**Не нужно для этой фазы**: API server, database, web UI, auth, AI/LLM.

**Как агенты работают с Bobr на этом этапе**: Claude Code читает `.bobr/` файлы напрямую (L1) и вызывает `bobr` CLI (L2). Никакой специальной интеграции не нужно — агент уже умеет читать файлы и запускать shell-команды.

### Phase 1: Spec-Driven Loop + MCP + Cowork (Weeks 4–6)

**Цель**: Change workflow + MCP server + подключение нетехнических пользователей. К концу фазы каждая фича Bobr оформляется как Change, Костя (CEO) видит бэклог через Claude Cowork.

**Dogfooding milestone**: Фичи Phase 2 спланированы как Changes. Claude Code подключает Bobr как MCP server. Костя и Иван подключают Bobr MCP в Claude Cowork и работают с бэклогом Apilize.

**Agent interface level**: L1 + L2 + L3 (MCP)

- [ ] `bobr change new` / `continue` / `ff` (fast-forward)
- [ ] Change артефакты: proposal.md → design.md → tasks.md
- [ ] `bobr change verify` / `archive`
- [ ] `bobr context generate` — сборка AGENTS.md / CLAUDE.md из specs + requirements
- [ ] Delta specs + sync to main specs
- [ ] Epics: `bobr backlog epic-add` / `epic-list`
- [ ] **MCP Server (stdio + Streamable HTTP)**: `read_backlog`, `add_item`, `get_change`, `get_status`
- [ ] **Claude Cowork integration**: Костя/Иван подключают Bobr MCP Server в Claude Cowork
- [ ] **Plan Phase 2 features as Changes** — собственные фичи проходят через workflow

### Phase 2: Delivery Loop + Telegram (Weeks 7–10)

**Цель**: Полный цикл task → context → PR → preview + Telegram bot. К концу фазы агенты выполняют задачи Bobr, Костя получает уведомления в Telegram.

**Dogfooding milestone**: Claude Code берёт задачу из `.bobr/`, получает context через `bobr context generate`, создаёт PR. Костя получает preview link в Telegram.

- [ ] `bobr context generate --task <id>` — контекст для конкретной задачи (relevant specs + requirements)
- [ ] `bobr context generate --format claude|codex|cursor` — per-agent format
- [ ] `bobr activity log` — агент регистрирует свою работу (CLI + MCP tool)
- [ ] `bobr activity cost` — tracking token usage
- [ ] GitHub integration: PR creation с link к task/change
- [ ] Render deploy preview integration
- [ ] MCP Server расширение: `create_change`, `log_activity`, `search_knowledge`
- [ ] Event hooks: on_task_created, on_pr_merged (shell scripts)
- [ ] **Telegram Bot**: `/status`, `/backlog`, `/task`, уведомления (PR ready, preview link)
- [ ] **Telegram notifications**: event hooks → Telegram (on_pr_created, on_preview_ready)
- [ ] **Агенты выполняют задачи Bobr** — Claude Code использует `bobr context generate` + MCP tools

### Phase 3: Knowledge & Team (Weeks 11–14)

**Цель**: Knowledge Base + Requirements + Team. К концу фазы команда работает в Bobr через Claude Code (CTO), Claude Cowork (CEO/CFO) и Telegram (все). Web UI — по результатам feedback.

**Dogfooding milestone**: PRD, deep research, meeting notes — в Knowledge Base. Команда Apilize (3 человека) работает в Bobr ежедневно: Артём через Claude Code, Костя/Иван через Claude Cowork + Telegram.

- [ ] Project scaffolding: FastAPI + PostgreSQL + pgvector + S3
- [ ] Auth (Auth0, multi-tenant, Agent role)
- [ ] Knowledge Base: upload, parse, index, semantic search
- [ ] Vision & Scope module (port Wiegers plugin)
- [ ] Use Cases module
- [ ] Requirements quality checker
- [ ] Web UI: dashboard, backlog kanban, knowledge browser, change viewer
- [ ] Web UI: stakeholder view (read-only dashboard для CEO/CFO: бэклог, прогресс, preview links)
- [ ] Activity feed (human + agent, unified)
- [ ] Invite, roles, permissions
- [ ] Traceability engine: requirement → spec → PR
- [ ] Post-merge reflection (P6): AI creates follow-up items
- [ ] **Import Bobr's own docs into Knowledge Base** — PRD, research, specs
- [ ] **Onboard Apilize team** (Костя, Иван) — CEO/CFO видят бэклог и прогресс в Web UI

### Phase 4: Runner, Scale & Polish (Weeks 15+)

**Цель**: Bobr Runner (кнопка «Запустить»), multi-agent, analytics, integrations. К концу фазы Костя (CEO) может запустить задачу и получить Preview link — без участия CTO.

**Dogfooding milestone**: 100% фич Bobr проходят полный цикл. Костя запускает задачи через Web UI. Multi-agent waves на собственных задачах.

- [ ] **Bobr Runner**: запуск внешних AI-агентов из Web UI (кнопка «Запустить»)
- [ ] Runner: isolated execution (worktree + sandbox)
- [ ] Runner: real-time monitoring (logs, cost, status в Web UI)
- [ ] Runner: cost controls (budget per task/user/project)
- [ ] Runner: result collection (PR link, preview URL)
- [ ] Wave planner: parallel agent execution (P4)
- [ ] Agent analytics dashboard (cost, success rate, cycle time)
- [ ] Multi-provider agents (Codex, Cursor background)
- [ ] Agent Skills system
- [ ] AI Code Review (blind validation)
- [ ] Bidirectional Jira/Linear sync
- [ ] Slack notifications
- [ ] Collaborative real-time editing
- [ ] Self-hosted deployment
- [ ] **Костя (CEO) запускает задачи Apilize через Web UI → Preview link**
- [ ] **Run multi-agent waves on Bobr's own backlog**
- [ ] Public launch / waitlist

---

## 14. Риски и митигации

| Риск | P | I | Митигация | Референс |
|------|---|---|-----------|----------|
| AI agent quality нестабильно | H | H | Propose-Review (P2) обязателен; acceptance criteria в specs; retry strategies | Zeroshot: blind validation |
| Слишком сложный workflow (как Height.app — закрылся) | H | H | Progressive disclosure: "just add a task" → specs → agents. CLI-first для zero-overhead entry | Height.app lesson |
| Context injection раздувает tokens | H | M | Smart context selection (relevance scoring); P3: token budget per task; prompt caching (90% reduction, Backlog Agents) | Backlog Agents plugin |
| Git-native storage конфликтует при parallel work | M | M | Worktree isolation (P4); proven: Claude Forge 39 фич, 0 конфликтов | Claude Forge |
| Зависимость от одного AI provider | M | H | Multi-provider architecture; abstract agent interface | Capy: 30+ models |
| Конкуренция с Hamster/Linear/Devin | H | H | Differentiation: requirements + knowledge + specs + traceability — ни у кого нет этой комбинации | Market gap analysis |
| Bidirectional sync с Jira/Linear сложен | H | M | Start with one-way import; bidirectional — later phase | Industry-wide problem |
| Market timing (слишком рано / поздно) | M | H | Dogfood на Expecto сразу; не идти в enterprise до product-market fit | Height.app (too early) vs Taskmaster (right time) |
| Dogfooding замедляет начальные фазы | M | M | Phase 0 спроектирована минимальной (CLI only, no server); overhead миграции — одноразовый | Rust bootstrap: 3 фазы компилятора |
| Собственный bias как единственный пользователь | H | M | Привлечь 2-го пользователя (команда Expecto) в Phase 3; внешние beta-testers в Phase 4 | Height.app: N=1 → generalize too early |

---

## 15. Уроки из ландшафта

### 14.1 Чему учиться

| Источник | Урок | Применение в Bobr |
|----------|------|----------------------|
| **Taskmaster AI** (15.5K за 9 недель) | PRD → structured tasks with dependencies — killer feature для solo/small team | Наш change workflow должен быть таким же простым для входа |
| **Backlog.md** | Git-native markdown — правильная архитектура для AI | `.bobr/` формат |
| **CCPM** | GitHub Issues как DB + 12 parallel worktrees = проверено | Worktree isolation для agents |
| **Linear for Agents** | Agent as first-class teammate с профилем и permissions | Agent role в нашей модели |
| **Kiro (Amazon)** | 3-phase spec workflow (req → design → tasks) = наш change workflow | Валидация нашего подхода крупным вендором |
| **Claude Forge** | 39 фич, 9 батчей, 0 конфликтов через wave planning | Wave planner в Phase 3 |
| **ClickUp Super Agent** | Weekly AI sprint proposal + "Cut This" recommendation | AI-assisted prioritization |
| **Backlog Agents plugin** | 90% token reduction через prompt caching | Aggressive caching strategy |

### 14.2 Чего избегать

| Анти-паттерн | Источник | Почему опасно |
|-------------|----------|--------------|
| "Слишком AI-first" без user base | Height.app (закрылся) | Рынок не готов к полной автономии; нужен human-in-the-loop |
| Multi-agent role simulation | MetaGPT, ChatDev | Overhead, hallucination amplification; мы для реальных команд |
| Vendor lock-in на один AI provider | Devin ($400/мес) | Costs + зависимость; нужна абстракция |
| Retrofit AI на legacy архитектуру | Jira + Rovo | AI остаётся надстройкой; мы проектируем с нуля |
| Sprint ceremonies для AI agents | Traditional Scrum | Story points неприменимы; нужны token budgets (P3) |

---

## 16. Открытые вопросы

1. **Naming**: "Bobr" — финальное название. Репозиторий: github.com/usebobr/Bobr
2. **Pricing model**: Per-seat? Per-agent-run? Token-based? Freemium с лимитом на агентские runs?
3. **Open source strategy**: Core open-source (как Plane, 46K stars) + hosted service? Или SaaS-first?
4. **Agent protocol**: MCP (стандарт) vs расширение MCP для spec-driven workflows?
5. **Spec format**: `.bobr/` как эволюция OpenSpec? Совместимость с Kiro's format?
6. **Relationship to Taskmaster AI**: Интеграция? Конкуренция? Taskmaster как agent внутри Bobr?
7. **Mobile**: Нужен ли мобильный доступ для PM/stakeholders? (Минимум: read-only dashboard)
8. **Hamster partnership**: Hamster добавил CLI для Claude Code + облачную синхронизацию. Партнёрство или конкуренция?
9. **Dogfooding scope**: Когда переключать Expecto на Bobr? Параллельно с Phase 2 (agent execution) или ждать Phase 3 (team)?
10. **Bootstrap tooling**: Использовать существующие Claude Code плагины (backlog, OpenSpec) как bridge до Phase 1, или сразу писать CLI?

---

## Appendix A: Glossary

| Термин | Определение |
|--------|-------------|
| **Agent** | AI coding agent (Claude Code, Codex, etc.), выполняющий задачу автономно |
| **Change** | Единица работы: от proposal до archive (как в OpenSpec и Kiro) |
| **Spec** | Спецификация домена или фичи в markdown формате |
| **Delta Spec** | Изменения к существующей spec в рамках change |
| **Worktree** | Изолированная копия git-репозитория для параллельной работы агента |
| **Context Injection** | Процесс сборки релевантного контекста для агента перед запуском |
| **Wave** | Группа независимых задач для параллельного запуска агентов |
| **Traceability** | Прослеживаемость связей: requirement → spec → code → test |
| **Elicitation** | Процесс выявления требований у стейкхолдеров |
| **MCP** | Model Context Protocol — стандарт связи AI-агентов с инструментами |
| **Token Budget** | Лимит AI-ресурсов на задачу (замена story points для agent-first) |
| **Propose-Review** | Паттерн: AI генерирует → человек ревьюит и решает |
| **Blind Validation** | AI review без контекста реализации (только spec + result) |
| **Bobr Core** | Ядро Bobr — tool provider, zero AI dependency. Данные + CLI + MCP |
| **Bobr Runner** | Оркестратор внешних AI-агентов (аналог GitHub Actions runner). Запускает агентов, мониторит, собирает результат |
| **North Star Flow** | Целевой сценарий: CEO нажимает «Запустить» → AI-агент пишет код → CEO получает Preview link |
| **Consumer** | Интерфейс для взаимодействия с Bobr Core: Claude Code, Claude Cowork, Telegram Bot, Web UI |
| **Claude Cowork** | Агентный режим в Claude Desktop — "Claude Code для остальной работы". Поддерживает MCP, файлы, shell commands |

## Appendix B: Референсы

### Прямые конкуренты и аналоги
- **Hamster** (tryhamster.com) — team briefs + AI agent execution, 25K+ GitHub stars
- **Taskmaster AI** (github.com/eyaltoledano/claude-task-master) — PRD → structured tasks, 25.7K stars, MIT+CC
- **Backlog.md** (github.com/MrLesk/Backlog.md) — git-native markdown backlog + MCP
- **CCPM** (Automaze) — GitHub Issues + 12 parallel Claude Code agents
- **Capy** (capy.ai) — parallel AI IDE, Captain+Build architecture, YC-backed
- **Linear for Agents** — agent-as-teammate, MCP, cycle time by agent
- **Jira + Rovo** — enterprise AI, work breakdown, $10.2B Atlassian
- **Devin** (Cognition Labs) — full-stack agent, $10.2B, MultiDevin, acquired Windsurf
- **Codex** (OpenAI) — cloud-native parallel execution, Skills, Automations
- **Jules** (Google) — "Delegate your backlog", GitHub Issues native, Gemini 2.5 Pro
- **Kiro** (Amazon) — spec-driven IDE, 3-phase workflow, Agent Hooks

### Open-source frameworks
- **MetaGPT** (59.6K stars) — multi-agent SOP, ICLR 2024
- **Plane** (46.3K stars) — AI-native open-source PM, MCP server
- **BMAD METHOD** v6 — 12 agent personas
- **Zeroshot** (covibes) — multi-agent pipeline, blind validation
- **Vibe Kanban** — parallel agent orchestration, 10+ worktrees
- **GitHub Spec Kit** — official spec-driven development tool

### Validated internal tools
- **Expecto project** — 117 specs, 64 changes, 68+ backlog items, full workflow
- **Wiegers Requirements Plugin** — Vision & Scope, Use Cases, Quality Review
- **OpenSpec** — spec-driven development convention
- **Backlog plugin** — 9 slash-commands, git-native storage

### Методологии
- Karl Wiegers, "Software Requirements, 3rd Edition"
- Alistair Cockburn, "Writing Effective Use Cases"
- Scrum.org — AI-first Scrum adaptations (token budgets)
- MetaGPT (arXiv) — structured artifacts > dialogue

### Академические работы
- "LLM-Based Multi-Agent Systems for Software Engineering" (arXiv 2404.04834)
- "Cognitive Agents for Agile Software PM" (arXiv 2508.16678)
- "ALMAS: Autonomous LLM-based Multi-Agent Software Engineer" (arXiv 2510.03463)
- 18 architectural patterns for LLM multi-agent systems (arXiv 2511.08475)
