# Research: Claude Code Project Manager (CCPM)

**Дата**: 2026-03-18
**Источник**: https://github.com/alhoseany/Claude-Code-Project-Manager
**Автор**: alhoseany

## Обзор

CCPM — фреймворк превращающий Claude Code в Project Manager. PM никогда не пишет код — только оркестрирует, документирует и делегирует субагентам. Философия: "THINK → DOCUMENT → DELEGATE → VERIFY → DOCUMENT → IMPROVE".

## Архитектура

### Не код, а методология
CCPM — это НЕ программный продукт. Это набор:
- Шаблон CLAUDE.md с правилами PM-оркестрации (~1000 строк)
- Шаблоны `.pm/` директории
- Python-скрипты автоматизации (pm-tools)
- Custom agents для Claude Code

### Memory System (`.pm/`)
```
.pm/
├── MEMORY.md          # Состояние проекта, архитектура
├── MISTAKES.md        # Паттерны ошибок и предотвращение
├── DECISIONS.md       # Архитектурные решения
├── PROGRESS.md        # Хронологический лог прогресса
├── IMPROVEMENTS.md    # Идеи улучшений
├── SUBAGENT-RULES.md  # Правила для субагентов
├── CRITICAL.md        # Credentials, URLs
├── INDEX.md           # Навигация
├── logs/
│   ├── sessions/      # Логи сессий
│   └── agents/        # Логи субагентов
├── debug/             # Артефакты отладки
├── tests/             # Тест-отчёты
├── reviews/           # Ретроспективы
└── plans/             # Планы реализации
```

### PM Tools (Python)
| Tool | Назначение |
|------|-----------|
| `pm-init` | Инициализация сессии |
| `pm-end` | Финализация сессии |
| `pm-check` | Health check |
| `pm-context` | Загрузка контекста |
| `pm-export-context` | Экспорт перед компактификацией |
| `pm-recover-context` | Восстановление после компактификации |
| `pm-audit` | Аудит качества PM работы (0-100) |
| `pm-agent-export` | Экспорт транскриптов субагентов |
| `pm-classify` | Управление sensitive data |

### Субагенты
| Агент | Модель | Назначение |
|-------|--------|-----------|
| Explore | haiku | Поиск файлов |
| python-pro | haiku | Python код |
| typescript-pro | haiku | TypeScript |
| backend-architect | opus | Системный дизайн |
| database-architect | opus | Схемы данных |
| security-auditor | opus | Аудит безопасности |
| debugger | opus | Расследование багов |
| qa-expert | opus | Тест-планирование |
| test-automator | haiku | Запуск тестов |

**Правило**: haiku для execution, opus для reasoning.

## Ключевые протоколы

### Loop Prevention
```
Attempt 1: Normal
Attempt 2: + MISTAKES.md patterns
Attempt 3: MANDATORY update MISTAKES.md
Attempt 4+: STOP, escalate to user
```

### Documentation Checkpoints
Обновлять `.pm/` при КАЖДОМ событии:
- После каждого агента
- Перед AskUserQuestion (пользователь может уйти)
- Перед long-running commands
- На любую ошибку
- При смене фазы

### Deployment Protocol
Deployment НЕ завершён пока local code ≠ deployed code.
Каждый fix на сервере → sync back to local.

### Context Preservation (Hooks)
```json
{
  "PreCompact": "pm-export-context",
  "SessionStart": "pm-recover-context",
  "SubagentStop": "pm-agent-export"
}
```

## Ключевые правила

### PM NEVER:
- Пишет/редактирует код
- Запускает build/test/git
- Создаёт файлы вне `.pm/`
- Пропускает чтение контекста
- Делегирует без проверки MISTAKES.md
- Принимает результат без верификации
- Продолжает после 3 неудач

### PM ALWAYS:
- Читает все `.pm/*.md` при старте
- Включает universal rules в каждую делегацию
- Верифицирует результат субагента
- Обновляет PROGRESS.md после КАЖДОГО агента

## Выводы для Bobr

- **MISTAKES.md** — анти-паттерны как первоклассные сущности. Проверка перед каждой делегацией
- **Loop Prevention** — счётчик попыток с эскалацией — защита от зацикливания
- **Documentation Checkpoints** — "if it's not in .pm/, it didn't happen"
- **Context preservation hooks** — PreCompact/SessionStart для выживания при компактификации
- **PM Quality Audit** — 5 измерений, скоринг 0-100
- **Subagent Rules** — субагенты НЕ наследуют CLAUDE.md, правила передаются явно
- **Model selection** — haiku для execution, opus для reasoning
- **Session protocol** — формализованные start/end с валидацией
- **Over-engineered для большинства проектов** — но идеи отличные
