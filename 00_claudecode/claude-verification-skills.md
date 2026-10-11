# Verification skills

Если ты дважды написал одну и ту же multi-step инструкцию, это кандидат на skill. Первым стоит делать skill для **verification**.

## 1. Зачем verification skill

Без него проверка зависит от тебя: надо вспомнить попросить прогнать тесты или прочитать diff. Пропустил раз, и плохой код проходит.

С skill всё идёт само: Claude закончил refactor, изменение совпало с `description` у skill, skill срабатывает и:

1. Запускает test suite.
2. Читает diff.
3. Проверяет, что ни один тест не ослабили, лишь бы он проходил.
4. Репортит pass/fail с evidence.

Важно: "done" это не "код выглядит правильно", а **gates реально запущены, результаты наблюдались и названы явно**. Зелёные тесты не гарантия: тест могли тихо ослабить.

Тот же шаблон подходит для: release checklist, migration recipe, pre-PR check.

## 2. Структура skill folder

```
.claude/skills/verify/
├── SKILL.md        # lean: name, description, procedure
├── reference.md    # детали, Claude читает только когда нужно
└── check.sh        # скрипт, Claude его выполняет, не грузит в context
```

- `SKILL.md` держи коротким: что делать.
- `reference.md`: длинные объяснения, ссылка на него из `SKILL.md`.
- Скрипты (например `check.sh`, который гоняет все gates) выполняются, а не загружаются в контекст.
- В контекст изначально грузятся только descriptions, поэтому упаковывать повторяющиеся процедуры почти ничего не стоит.

## 3. Пример SKILL.md (illustrative)

Формат на основе описания в статье (name + description + procedure). Конкретные поля frontmatter сверь с документацией.

```markdown
---
name: verify-changes
description: Use after finishing a refactor or code change to verify the work. Runs tests, reviews the diff, and reports pass/fail with evidence.
---

# Verify changes

1. Run `./check.sh` (runs the full test suite and all gates).
2. Read the diff (`git diff`).
3. Confirm no test was weakened, skipped, or deleted just to pass.
4. Report PASS or FAIL with the actual command output as evidence.

For details on each gate, see [reference.md](reference.md).
```

## 4. Какая instruction surface за что отвечает

| Что | Куда |
|---|---|
| Conventions, которые действуют всегда (naming, где лежат файлы) | `CLAUDE.md` |
| Procedures и reference для конкретного типа задач | skill |
| Rule, который Claude **не имеет права** пропустить | **hook** |

`CLAUDE.md` и skills — это инструкции, которым Claude следует. Hook — код, который реально выполняется. Если пропуск правила недопустим, не оставляй его на instruction-following.

## 5. Итог

1. Skill = папка с `SKILL.md` (name, trigger description, procedure).
2. Начни с verification skill.
3. Держи `SKILL.md` lean, тяжёлое выноси в side files и scripts.
4. Положи в `.claude/skills` и закоммить: вся команда получает одну и ту же проверку автоматически.
