# Building with the Claude API — Agents and Workflows

Notes for the "Agents and workflows" section — the final piece that ties tool use + MCP together
into actual architecture patterns for autonomous/semi-autonomous systems.

## Core decision: Workflows vs. Agents

The choice comes down to **predictability vs. control**:

```
How well do you know the exact steps?
         │
   ┌─────┴─────┐
   ▼           ▼
Predictable  Dynamic /
             Unpredictable
   │           │
   ▼           ▼
Workflows    Agents
```

- **Workflows** — predetermined, step-by-step LLM calls wired together in code. Ideal for
  constrained, production UX tasks where you can enumerate the steps in advance.
- **Agents** — given a goal + a set of tools, and left to figure out the path dynamically.
  Ideal for open-ended, unpredictable tasks.

**Rule of thumb:** default to workflows. Only move to an agent when the task is genuinely too
unpredictable for a fixed pipeline.

| Metric         | Workflows               | Agents                               |
| -------------- | ----------------------- | ------------------------------------ |
| Predictability | High                    | Low                                  |
| Flexibility    | Low                     | High                                 |
| UX alignment   | Great for structured UI | Great for open-ended chat/automation |
| Best for       | Production reliability  | Creative problem solving             |

## Topics

### 1. Agents and workflows (intro)

- Frames the core decision matrix above — the first design question for any LLM-powered feature
  is "do I know the steps, or does the model need to figure them out?"

### 2. Evaluator-Optimizer pattern

- A feedback loop: a **producer** generates an artifact, a **grader** evaluates it against
  criteria, and if rejected, the producer retries with the grader's feedback folded into the
  prompt.
  ```python
  while not accepted:
      artifact = producer.generate(prompt)
      feedback, accepted = grader.evaluate(artifact)
      if not accepted:
          prompt = f"Improve this: {artifact}. Feedback: {feedback}"
  ```
- **When to use:** outputs must meet strict, checkable criteria — this is basically the same
  producer/grader shape as the Prompt Evaluation section, but run live in the app loop instead
  of offline in an eval script.

### 3. Parallelization workflows

- Break a decision into independent sub-evaluations run **at the same time**, then combine
  results.
- Example: send one piece of content to three simultaneous LLM calls — SEO check, grammar check,
  tone check — instead of one call trying to judge everything at once.
- **When to use:** evaluating multiple independent criteria, or comparing several distinct
  options.

### 4. Chaining workflows

- A sequential pipeline where each LLM call's output feeds the next call's input.
- Example: Draft Outline → Generate Content → Translate to Spanish → Format as Markdown.
- **When to use:** a single long prompt would cause Claude to drop instructions, or when
  intermediate output needs validation before the next step runs.

### 5. Routing workflows

- A first LLM call classifies the incoming request, then routes it to a specialized downstream
  prompt/workflow.
  ```
  Incoming Query ──> [Router LLM] ──┬──> Refund Request  ──> (Billing Prompt)
                                    └──> Technical Issue ──> (Tech Support Prompt)
  ```
- **When to use:** handling diverse request types (e.g. customer service) where each type needs
  different handling logic or a different specialized prompt.

### 6. Agents and tools

- Agents get a goal plus a set of **flexible, atomic tool primitives** rather than narrow,
  purpose-built tools.
- Example — Claude Code's tools are deliberately general: `bash` (run any command), `read` /
  `write` / `edit` (file manipulation), `glob` / `grep` (search) — rather than something like a
  single hardcoded `refactor_code()` tool.
- Why: flexible primitives let the agent combine them creatively for tasks you didn't
  specifically design for; an over-specialized tool only covers the one case you anticipated.

### 7. Environment inspection

- An agent must never operate blindly — for every tool execution, it needs a way to verify what
  actually happened.
- Tactics:
  - Read a file's contents before _and_ after modifying it
  - Capture UI screenshots after a frontend interaction
  - Explicitly check API response/payload status rather than assuming success

### 8. Workflows vs. agents (review)

- Wrap-up reinforcing the decision matrix and rule of thumb: workflows by default, agents when
  the task's unpredictability genuinely demands it.

## Why this section matters for my roadmap

This is the synthesis step for Nordic Shop AI Agent:

- Most of the app (search → filter → recommend) is probably a **workflow** (predictable steps),
  not a full agent — resist over-engineering it into an agent by default
- The evaluator-optimizer pattern reuses the same producer/grader shape already built in the
  Prompt Evaluation section — can be reused directly
- Environment inspection matters even outside coding agents: e.g. after a tool call updates
  stock/availability, verify the actual DB state rather than trusting the tool "said" it worked
