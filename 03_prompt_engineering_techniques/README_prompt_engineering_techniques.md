# Building with the Claude API — Prompt Engineering Techniques

Notes for the "Prompt engineering techniques" section (Being clear and direct → Being specific →
Structure with XML tags → Providing examples → Exercise on prompting).

> Note: written from general Claude prompting best practices — plug in your own eval scores /
> notebook details once you run the exercises, since I don't have the exact lesson content.

## The goal of this section
Take the naive baseline prompt from the previous lesson (meal-plan generator, ~2.3/10 score) and
apply techniques one at a time, re-running the eval pipeline after each change to measure impact.

## Techniques

### 1. Being clear and direct
- State exactly what you want, don't make Claude infer intent
- Spell out required output fields instead of asking an open-ended question
- Example fix for the meal-plan prompt: instead of "What should this person eat?", say
  "Generate a 1-day meal plan including daily caloric total, macronutrient breakdown, and
  meals with exact foods, portions, and timing."

### 2. Being specific
- Vague instructions get vague answers — specify format, units, length, edge cases
- Replace general adjectives ("healthy", "good") with concrete, checkable requirements
- Specify units (grams vs cups), number of meals, and how to handle missing/edge-case inputs

### 3. Structure with XML tags
- Separate distinct parts of the prompt (context, data, instructions, examples) with tags like
  `<task>`, `<athlete_data>`, `<requirements>`, `<output_format>`
- Makes long prompts easier for Claude to parse correctly and easier for you to maintain
- Also useful on the output side — asking Claude to wrap its answer in tags makes parsing easier

### 4. Providing examples (few-shot prompting)
- Show 1-3 example input → output pairs directly in the prompt
- Most effective technique for locking down a specific output *format* (e.g. matching your
  meal-plan structure exactly)
- Keep examples realistic and representative of the range of cases you expect

### 5. Exercise on prompting
- Apply the above techniques **one at a time** to the meal-plan prompt
- Re-run `evaluator.run_evaluation(...)` after each change
- Log the score progression, e.g.:
  - v1 (naive): 2.3
  - v2 (+ clear & direct output requirements): ~5
  - v3 (+ XML structure): ~6.5
  - v4 (+ few-shot example): ~8+
- Rule to follow: change one thing, re-evaluate, keep what works before stacking the next technique

## Key takeaway
Prompt engineering here isn't guesswork — it's the same iterative loop as before (write → eval →
apply technique → re-eval), just now with a specific toolbox of techniques to reach for in order:
clarity → specificity → structure → examples.

## Next up
- Streaming responses
- Tool use with Claude
