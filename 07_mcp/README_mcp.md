# Building with the Claude API — Model Context Protocol (MCP)

Notes for the "Model Context Protocol" section — the biggest ⭐ priority in my roadmap. Goal:
go from "I tried MCP" to "I built an MCP server exposing tools for an AI-powered application."

> Note: written from general MCP documentation/architecture — plug in your own notebook code
> and project specifics once you run through the lessons.

## Topics

### 1. Introducing MCP
- MCP is a standardized protocol for connecting an AI application (the "host"/client) to
  external tools, data sources, and prompt templates ("servers") — instead of every integration
  being custom-built, both sides speak the same protocol
- Three core primitives: **tools** (functions the model can call), **resources** (data the
  client can read), **prompts** (reusable prompt templates the server can expose)

### 2. MCP clients
- The client is the piece that connects to one or more MCP servers, discovers what they offer
  (tools/resources/prompts), and relays that to the model (e.g. Claude) during a conversation
- Claude Desktop, Claude Code, and custom apps can all act as MCP clients

### 3. Project setup
- Scaffolding a basic MCP server project — dependencies, folder structure, and the minimal
  server instance needed before defining any tools

### 4. Defining tools with MCP
- Same underlying idea as regular tool use (name, description, input schema) but exposed
  through the MCP server rather than passed directly in an API call
- Example: wrapping `search_products()`, `get_product()`, `check_availability()` as MCP tools
  instead of inline API `tools` parameters — this is the direct upgrade path for Nordic Shop

### 5. The server inspector
- Anthropic's MCP Inspector — a dev tool for testing an MCP server in isolation: list its tools/
  resources/prompts, call them manually, and see raw responses without needing a full client/LLM
  in the loop. Useful for debugging a server before wiring it into an actual app

### 6. Implementing a client
- Hands-on: write a minimal MCP client that connects to your server, lists available tools, and
  lets Claude call them as part of a conversation (same tool-use loop as before, but tools now
  come from the MCP server instead of being hardcoded)

### 7. Defining resources
- Resources expose readable data (files, records, documents) that the client can fetch and use
  as context — different from tools, since resources are about *providing data*, not *performing
  an action*

### 8. Accessing resources
- Client-side: how to list and read resources exposed by a server, and feed that content into
  the conversation as context (similar in spirit to RAG, but the data comes from a live server
  rather than a static vector store)

### 9. Defining prompts
- Servers can expose reusable prompt templates (with parameters) so clients don't need to
  hardcode prompt text — keeps prompt engineering centralized on the server side

### 10. Prompts in the client
- Client-side: discovering and invoking a server-defined prompt template, filling in its
  parameters, and using the resulting prompt in a conversation with Claude

### 11. MCP review
- Section wrap-up tying tools + resources + prompts together into the full picture of what an
  MCP server can expose and how a client consumes all three

## Why this section matters most for my roadmap
This is the direct path to the CV line:
> **Built an MCP server exposing tools for an AI-powered e-commerce application.**

Concrete plan for Nordic Shop:
1. Take the tool functions already built in the Tool Use section (`searchProducts`,
   `getProduct`, `checkAvailability`, `recommendProducts`)
2. Wrap them as MCP tools on a real MCP server
3. Test the server with the MCP Inspector before connecting anything else
4. Connect it to Claude Desktop/Code as a client to confirm it works outside the course notebook
5. Optionally expose product data as an MCP **resource** and a prompt template (e.g. "product
   recommendation" prompt) to show the full tools + resources + prompts picture

## Next up
- Claude Code & Computer Use
- Agents and workflows
