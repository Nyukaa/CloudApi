# Building with the Claude API — Features of Claude

Notes for the "Features of Claude" section — built-in API capabilities beyond plain text chat.

## Topics

### 1. Extended thinking
- Lets Claude reason through a problem in a visible "thinking" block before producing its final
  answer — useful for harder multi-step problems (math, complex logic, planning)
- Configured via a `thinking` parameter with a token budget; the thinking content is returned
  separately from the final answer

### 2. Image support
- Claude accepts images as input (base64-encoded or via URL) alongside text in the same message
- Useful for tasks like describing images, reading screenshots, analyzing charts/diagrams

### 3. PDF support
- Claude can accept PDF documents directly as input (as a `document` content block) and reason
  over both the text and visual layout of the file — no separate OCR/extraction step needed

### 4. Citations
- A feature for grounding answers in provided source documents — Claude can return responses
  with citations pointing back to the specific parts of the source content that support each
  claim, useful for RAG-style applications where traceability matters

### 5. Prompt caching
- Lets you cache a stable prefix of your prompt (system prompt, tool definitions, long context)
  so repeated requests don't re-process and re-charge for that content in full
- Cached reads are billed at a fraction of normal input token price, cache writes cost slightly
  more than normal input — net savings when the same prefix is reused across calls
- Default cache lifetime is short (a few minutes); an extended-TTL option exists for longer
  reuse windows

### 6. Rules of prompt caching
- Cache breakpoints are **positional/prefix-based** — content must be identical up to the
  breakpoint for a cache hit; changing anything earlier in the prompt invalidates it
- Order stable content (system prompt, tools, static context) **before** dynamic content
  (the actual user turn) so the stable part can be cached and reused
- There's a **minimum token count** below which a prompt won't be cached at all, even if marked
  — check current Anthropic docs for the exact number for the model you're using, since it can
  vary by model
- A limited number of cache breakpoints are available per request — use them for the highest-value
  stable sections

### 7. Prompt caching in action
- Hands-on: mark a cache breakpoint, make a first request (cache write, priced higher), then a
  second request reusing the same prefix (cache read, priced lower) — compare token usage in
  the response to confirm the cache actually hit
- Good habit: always check the cache-related token fields in the response rather than assuming
  caching worked just because you added `cache_control`

### 8. Code execution and the Files API
- Code execution lets Claude run code (e.g. Python) in a sandboxed environment as part of its
  response — useful for calculations, data analysis, or generating/verifying output rather than
  just guessing at it in text
- The Files API lets you upload files once and reference them across multiple requests by ID,
  instead of re-sending the same file content (e.g. a PDF or dataset) with every call

## Why this section matters for my roadmap
- **Prompt caching** is directly relevant to the cost/latency topic — a cheap way to cut token
  costs in an agent loop that repeats the same system prompt or tool schema on every turn
- **Citations** ties into RAG/evaluation — reduces hallucination risk and makes groundedness
  checkable
- **Code execution** is a useful pattern to know about even if Nordic Shop doesn't need it yet —
  relevant if evaluation scripts or data analysis features get added later

## Next up
- Model Context Protocol (MCP)
