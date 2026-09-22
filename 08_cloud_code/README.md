# Claude Code: Fundamentals, Workflows and MCP

Notes from the "Anthropic apps - Claude Code and computer use" chapter (Claude Code in action + Enhancements with MCP servers).

## 1. Project setup: `/init` and `CLAUDE.md`

Running `/init` makes Claude scan the codebase (structure, dependencies, coding style, architecture) and summarize it in a `CLAUDE.md` file. That file is automatically included as context in every future conversation.

There can be several `CLAUDE.md` files with different scopes:

| Scope | Purpose |
|-------|---------|
| **Project** | Shared between all engineers on the project (checked into git) |
| **Local** | Your personal notes, not checked into git |
| **User** | Used across all your projects |

Tips:
- You can give `/init` extra directions about areas to focus on.
- The generated file includes build commands, coding guidelines and project-specific patterns.
- Add notes quickly with `#`, e.g. `# Always use descriptive variable names`. Claude asks whether to save it to project, local or user memory.
- Always review the generated `CLAUDE.md`: fix inaccuracies and remove noise.

## 2. Fundamental workflows for working with AI agents

The core principle: **the agent is an effort multiplier. The more context and structure you give, the better the result.**

### Way 1: Plan → Implement (classic approach)

1. **Feed context.** Point Claude at the files relevant to the feature and ask it to read and analyze them. This shows it your patterns and existing functionality.
2. **Plan, don't code.** Ask Claude to think through the problem and produce a plan. Explicitly say not to write code yet.
3. **Implement.** Once the plan looks solid, ask Claude to implement it.

```
> Read the math.py and document.py files

> Plan to implement document_path_to_markdown tool. Don't write code yet:
  1. Create a function that takes a file path, validates it, detects type
     by extension, reads binary data, reuses binary_document_to_markdown
  2. Add documentation
  3. Register the tool with the MCP server
  4. Add tests

> Implement the plan
```

- **Best for:** new features.
- **Why it works:** planning first means less rework and no wrong-direction code.

### Way 2: Tests → Plan → Code (Test-Driven Development / TDD)

1. **Feed context.** Same as above: show Claude the relevant files.
2. **Brainstorm test cases.** Ask Claude what tests would validate the new feature.
3. **Implement the tests.** Pick the most relevant cases and have Claude write them.
4. **Write code that passes the tests.** Claude iterates on the implementation until all tests pass.

- **Best for:** logic that must be reliable.
- **Why it works:** clear, checkable success criteria give the agent a concrete target.

### Way 3: Act → Verify → Fix (feedback loop)

Give the agent a way to check its own work (tests, linter, build, type checker) and let it run in a loop: write, run the check, read the error, fix, repeat until it passes.

```
> Fix the failing test in test_math.py. Run the tests after every change until all pass.
```

- **Best for:** bug fixing and refactoring.
- **Why it works:** with feedback the agent verifies instead of guessing. The more precise the success criterion, the better the result.

### Way 4: Separation of roles (multiple agents or sessions)

Assign different tasks to different agents: one writes code, another reviews it as a critic, a third explores the codebase and returns only a short summary. Each has its own clean context, so they don't pollute the main session.

```
> Use a subagent to investigate how authorization works in this project and return a short summary.
```

- **Best for:** large tasks, code review, parallel work on independent parts.
- **Why it works:** a fresh pair of eyes catches what the author missed.
- **Trade-off:** every agent consumes tokens with its own context, so this is more expensive.

### Which way to choose

| Way | Key question | Best for |
|-----|--------------|----------|
| 1. Plan → Implement | What and how do we build? | New features |
| 2. Tests → Plan → Code (TDD) | How will we know it's done? | Reliable logic |
| 3. Act → Verify → Fix | What is broken? | Bugs, refactoring |
| 4. Separation of roles | Who does what? | Large tasks, review |

The ways can be combined: plan (1), write tests (2), and let the agent run the verify loop (3) during implementation.

## 3. Useful commands

| Command | What it does |
|---------|--------------|
| `/init` | Scans the codebase and creates `CLAUDE.md` |
| `#` | Adds a note to `CLAUDE.md` |
| `/clear` | Clears conversation history and resets context (use between unrelated tasks) |
| `/cost` | Shows the cost of the current session |
| `/mcp` | Shows the status of connected MCP servers |

Claude Code can also stage and commit changes to git, run tests and manage dependencies, so you don't have to switch between editor and terminal.

## 4. Extending Claude Code with MCP servers

Claude Code has a built-in **MCP client** (Model Context Protocol). By connecting MCP servers you give Claude access to external services and tools.

A server can expose three kinds of components:

| Component | Purpose |
|-----------|---------|
| **Tools** | Take actions (create a ticket, send a message) |
| **Prompts** | Prompt templates |
| **Resources** | Access to data |

### Registering a server

```bash
claude mcp add [server-name] [command-to-start-server]

# example
claude mcp add documents uv run main.py
```

Registration is done **once**. After that, Claude Code starts the server and connects to it automatically on every launch, and Claude picks the right tool by itself based on your request.

### Example

With an MCP server exposing a `document_path_to_markdown` tool:

```
> Convert the tests/fixtures/mcp_docs.docx file to markdown
```

Claude automatically uses the custom tool to read the document and return markdown.

### Popular MCP servers

- **sentry-mcp**: discover and fix bugs logged in Sentry
- **playwright-mcp**: browser automation for testing and troubleshooting
- **figma-context-mcp**: exposes Figma designs to Claude
- **mcp-atlassian**: access to Confluence and Jira
- **firecrawl-mcp-server**: web scraping
- **slack-mcp**: post messages and reply to threads

### Building your own workflow

Combine servers to match your process, for example:

1. Sentry: fetch production error details
2. Jira: read ticket requirements
3. Slack: notify the team when the work is done
4. Custom servers for internal tools and APIs

Note: every connected server adds its tool descriptions to the context, which slightly increases token usage. Connect only what you need.

## 5. Key takeaways

- Run `/init` and keep `CLAUDE.md` accurate.
- Give context first, plan before coding, then implement.
- Use tests or a verify loop so the agent has clear success criteria.
- Use `/clear` between unrelated tasks to save tokens.
- Extend Claude with MCP servers: register once with `claude mcp add`.
