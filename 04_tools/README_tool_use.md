# Building with the Claude API — Tool Use with Claude

Notes for the "Tool use with Claude" section — this is the core of building agents:
letting Claude decide which functions to call and use the results.

> Note: written from general Claude tool-use documentation/patterns — plug in your own
> notebook code and project specifics once you run through the lessons.

## The core loop

```
User message
   ↓
Claude decides it needs a tool → returns a "tool_use" content block (name + input)
   ↓
Your code executes the actual function
   ↓
You send the result back as a "tool_result" message
   ↓
Claude uses the result to write the final answer
```

This is the foundation every agent is built on.

## Topics

### 1. Introducing tool use

- Claude doesn't execute code itself — it only _requests_ that a tool be called, with structured
  arguments. Your application code is responsible for actually running the function.

### 2. Project overview

- Sets up the running example used through the section — a small app where Claude calls real
  functions (e.g. lookups against local data) instead of just generating text.

### 3. Tool functions

- Plain Python functions your code can call directly (e.g. `search_products(query)`,
  `get_product(product_id)`) — these are what actually get executed once Claude asks for them.

### 4. Tool schemas

- Each tool needs a JSON schema description so Claude knows it exists and how to call it:
  ```python
  tools = [
      {
          "name": "get_product",
          "description": "Look up a product by its ID",
          "input_schema": {
              "type": "object",
              "properties": {
                  "product_id": {"type": "string", "description": "The product ID"}
              },
              "required": ["product_id"]
          }
      }
  ]
  ```
- Passed to `client.messages.create(..., tools=tools)`

### 5. Handling message blocks

- A Claude response can contain multiple content blocks (`text` and `tool_use` mixed)
- Need to loop over `message.content` and check each block's `type` rather than assuming
  `content[0]` is always the answer

### 6. Sending tool results

- After running the requested function, send the result back as a `tool_result` block inside a
  new `user` message, referencing the original `tool_use_id`
- Claude then continues the conversation using that result

### 7. Multi-turn conversations with tools

- Tool calls live inside the same `messages` history as regular conversation — assistant
  `tool_use` blocks and user `tool_result` blocks just get appended like normal turns

### 8. Implementing multiple turns

- Practical loop: keep calling `messages.create()`, checking `stop_reason == "tool_use"`,
  executing tools, appending results, and repeating until Claude returns a final text answer
  with no more tool calls

### 9. Using multiple tools

- Claude can be given several tools at once and picks the right one (or several, in sequence)
  based on the user's request — this is what makes it "agent-like" rather than a single
  function call

### 10. Fine-grained tool calling

- More precise control over how/when tools are invoked (e.g. forcing a specific tool,
  restricting choice, streaming partial tool inputs) rather than leaving it fully up to the model

### 11. The text edit tool

- Anthropic's built-in tool for making targeted edits to text/files without regenerating
  full content from scratch

### 12. The web search tool

- Anthropic's built-in tool for letting Claude search the web as part of its tool-use loop,
  no custom implementation needed

## Why this section matters most for my roadmap

This is the direct foundation for:

- Adding `searchProducts()`, `getProduct()`, `checkAvailability()`, `recommendProducts()` to
  Nordic Shop
- Everything that comes after it (MCP, agents/workflows) is really "tool use" wrapped in more
  structure — MCP standardizes _how_ tools are exposed, agent architectures standardize
  _when/how many times_ tools get called in a loop
