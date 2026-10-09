# Steering long Claude Code sessions

Идея: **сначала scope the work, потом steer while it runs.**

## 1. Plan mode (сначала план)

- Claude работает в read-only: читает код, решает что менять, отдаёт план.
- План надо реально прочитать, не пролистать.
- Чего-то не хватает — просит добавить в план. Итерировать план быстрее, чем чистить результат после запуска.

## 2. Compact (управление контекстом)

Сжимает разговор в summary, старые сообщения удаляются. Риск: важное потеряется и Claude "уплывёт".
Поэтому всегда добавляй инструкции:

```
/compact Focus on the --version flag implementation
```

Текст после команды определяет, что останется в summary.

## 3. Rewind (откат к чекпоинту)

Каждый твой prompt = checkpoint. Меню открывается так:

```
Esc Esc   (double tap escape on an empty prompt)
```

Опции в меню:

| Option | Что делает |
|---|---|
| Restore code and conversation | откат и кода, и чата |
| Restore conversation | откат только чата |
| Restore code | откат только файлов |
| Summarize from here | сжимает всё ПОСЛЕ чекпоинта (удобно после побочного разговора) |
| Summarize up to here | сжимает всё ДО чекпоинта (длинный setup, но реализацию оставить) |

## 4. Goal (автономный режим с условием "done")

Задаёшь условие завершения, Claude работает несколько ходов, пока быстрый evaluator не подтвердит, что условие выполнено.

```
/goal all tests in src/billing pass, and the type checker reports zero errors
/goal clear
```

- `/goal clear` — отменить.
- Evaluator читает только transcript, поэтому условие должно проверяться по выводу (например, результат запуска тестов).

## 5. Loop (повтор prompt по интервалу)

Запускает prompt между ходами, фиксированный или self-paced интервал. Для внешних вещей: CI run, deploy — и реагировать, когда состояние изменилось.

- Остановить: `Esc`

## 6. Worktrees (параллельная работа)

- Несколько агентов в одном репо без конфликтов: у каждой сессии свой независимый file tree.
- Когда сессия завершается, чистый worktree удаляется автоматически.
- Файл `.worktreeinclude` в корне репо: список git-ignored файлов, которые копируются в каждый worktree (например `.env`, локальный конфиг).

```
# .worktreeinclude (example)
.env
.env.local
```

## Cheat sheet

```
/compact <instructions>     # compact with focus
Esc Esc                     # rewind menu (on empty prompt)
/goal <completion condition>
/goal clear
Esc                         # stop a loop
.worktreeinclude            # git-ignored files to copy into each worktree
```

## Итог привычек

1. Scope first, then steer.
2. Направляй compaction, чтобы summary сохранил важное.
3. Rewind, когда Claude дрейфует.
4. `/goal`, когда "done" описать проще, чем шаги.
5. Параллельная работа — в worktrees.
