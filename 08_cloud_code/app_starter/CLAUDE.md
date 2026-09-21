# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup (uv-managed; Python >= 3.10)
uv venv && source .venv/bin/activate
uv pip install -e .          # editable install is required — tests/main.py import `tools.*` as a package

# Run the MCP server over stdio
uv run main.py

# Tests
uv run pytest
uv run pytest tests/test_document.py                                   # one file
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown     # one class
uv run pytest -k pdf                                                   # one test by name
```

There is no linter or formatter configured in this project.

## Architecture

An MCP server exposing document/utility tools. Three layers, deliberately kept separate:

1. **`tools/*.py` — plain Python functions.** No MCP imports, no server awareness. This is why they can be unit-tested directly (`tests/` imports `tools.document`, not the server).
2. **`main.py` — the server assembly.** Creates a single `FastMCP("docs")` instance and registers tools **explicitly, one line each**: `mcp.tool()(add)`. There is no decorator on the functions themselves and no auto-discovery of `tools/`, so a function in `tools/` is invisible to clients until it is imported and registered here. Currently only `tools.math.add` is wired up; `tools.document.binary_document_to_markdown` is implemented and tested but **not yet registered**.
3. **Client side** — this server is consumed by MCP clients (see `07_mcp/` in the parent repo), not run as a CLI.

### Adding a tool

Write the function in `tools/`, then add its import + `mcp.tool()(fn)` line to `main.py`. Both halves are needed.

### The function signature is the model-facing API contract

FastMCP derives the tool schema from the function itself, so signature and docstring are prompt text, not just documentation:

- Type hints become the JSON schema; pydantic `Field(description=...)` defaults become the per-parameter descriptions the model reads.
- The docstring becomes the tool description. Follow the established shape (see `tools/math.py`): one-line summary, then a detailed explanation, then a `When to use:` section (include when *not* to use), then `Examples:` with expected input/output.

### Document conversion

`binary_document_to_markdown` runs `markitdown` entirely in memory — bytes are wrapped in `BytesIO` and the format is declared via `StreamInfo(extension=file_type)`. No temp files are written. `file_type` is a bare extension string without a leading dot (`"docx"`, `"pdf"`).

## Constraints

- `mcp[cli]` is **pinned to 1.8.0** in `pyproject.toml` (everything else is a floor). Don't bump it incidentally — `FastMCP` lives at `mcp.server.fastmcp` and its API has moved across versions.
- This directory is one module of a larger course repo; the git root is `CloudAPI/`, two levels up, and the shared `.env` (`ANTHROPIC_API_KEY`) lives there. Commit from the repo root, but run and test from this directory.
