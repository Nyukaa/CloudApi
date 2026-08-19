# Building with the Claude API — Prompt Engineering & Evaluation

Notes and exercises for the prompt evaluation section.

## What I've done

### 1. Building an eval dataset
- Used Claude itself to generate a small evaluation dataset (`dataset.json`) of AWS-related tasks
- Each test case includes: `task` (description), `format` (`python` / `json` / `regex`), and ideally `solution_criteria` (task-specific grading criteria)
- Used the prefill + `stop_sequences` pattern to get clean JSON output when generating the dataset

### 2. Running the prompt under test
- `run_prompt(test_case)` sends the task to Claude and collects the raw output
- Key lesson: without prefill (`` ```code ``) + `stop_sequences=["```"]` and an explicit "respond only with code, no commentary" instruction, Claude returns markdown prose around the code instead of clean output — breaking any downstream parsing

### 3. Grading — two complementary methods
- **Syntax/structure grading** (`grade_syntax`) — deterministic, no LLM involved:
  - `validate_json` → `json.loads()`
  - `validate_python` → `ast.parse()`
  - `validate_regex` → `re.compile()`
  - Returns 10 or 0 depending on whether the output parses
- **Model-based grading** (`grade_by_model`) — Claude acts as an expert reviewer, given the task, the solution, and (when available) `solution_criteria`, and returns a structured JSON verdict: `strengths`, `weaknesses`, `reasoning`, `score` (1–10)
- Final score per test case = average of syntax score and model score

### 4. Running the full eval
- `run_eval(dataset)` loops over all test cases, runs + grades each, and prints the average score across the dataset
- This turns "does the prompt look good" into a repeatable, numeric signal you can track across prompt versions

## Key lesson learned (the hard way)
Forgetting prefill + `stop_sequences` on the **grader's** own output causes `JSONDecodeError` when parsing its verdict — the grader is just as prone to wrapping its JSON in prose/markdown as the model under test. The structured-output pattern must be applied at **every** step that expects machine-readable output, not just the main task.

## Next up
- Streaming responses
- Tool use with Claude
