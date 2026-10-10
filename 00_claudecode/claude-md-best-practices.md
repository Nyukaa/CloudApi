# CLAUDE.md that Claude actually follows

Главная мысль: **CLAUDE.md — это guidance, а не enforced config.** Каждая строка конкурирует с остальными за внимание Claude. Чем длиннее файл, тем хуже выполняется каждое отдельное правило. Цель: держать файл коротким.

## 1. Сначала спроси: нужен ли тут CLAUDE.md?

| Тип правила | Куда класть |
|---|---|
| Soft convention (стиль, структура, workflow) | `CLAUDE.md` |
| Hard rule, которое нельзя нарушать | **pre-tool-use hook** |

- Hook — это код, который запускается до действия Claude и может его заблокировать.
- Пример: "never push to main" в CLAUDE.md — это просьба, в hook — реальная защита.

## 2. Четыре места, где живёт CLAUDE.md

Все четыре загружаются вместе при запуске и складываются (ничего не отбрасывается).

| Level | Для чего |
|---|---|
| Managed policy | org-level файл от platform team, исключить нельзя |
| User | твои личные preferences для всех проектов на машине |
| Project | общий файл для команды, в репозитории |
| Local | в `.gitignore`, личные заметки только для этого репо |

Local удобен, когда в своей ветке нужно держать в голове архитектурные решения, которые не должны попасть в общий файл.

## 3. Разбивка большого файла через imports

```
@.claude/conventions/code-style.md
@.claude/conventions/testing.md
@.claude/conventions/workflow.md
```

- Imports раскрываются inline при запуске.
- Они помогают **организовать** файл, но **не уменьшают** контекст: всё грузится сразу.

## 4. Как формулировать правила

### Be specific and checkable

```
Vague:    Follow best practices for API routes.
Specific: Put new API routes in src/api/handlers, one per file.
```

Если нельзя проверить, выполнено ли правило, то Claude тоже не может.

### Name the replacement

```
Leaves it open: Don't use default exports.
Closes it:      Use named exports, not default exports.
```

### Emphasis is a budget

- `IMPORTANT` / `YOU MUST` повышают приоритет только относительно остальных правил.
- Если кричит каждое правило, то не выделяется ни одно.
- Трать emphasis на 2-3 правила, нарушение которых реально больно.

## 5. Keep the file under revision

- CLAUDE.md никогда не "закончен". Относись к нему как к живому коду.
- Claude сделал не так: считай это bug report на CLAUDE.md.
- Можно сказать прямо:

```
add that to the CLAUDE.md file
```

## Checklist

1. Hard rules → hooks, не CLAUDE.md.
2. Длинный файл → imports (помни: контекст не уменьшается).
3. Каждое правило specific и checkable, с названной заменой.
4. Emphasis только на самые важные правила.
5. Правь файл каждый раз, когда Claude ошибается.
6. Не можешь оправдать строку? Удали её.
