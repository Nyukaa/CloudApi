# Building with the Claude API — Part 1: Accessing Claude with the API

Notes and exercises completed for the "Getting started with Claude" section.

## What I've done

### 1. Environment setup
- Installed dependencies: `anthropic`, `python-dotenv`
- Stored API key securely in a `.env` file (`ANTHROPIC_API_KEY`), excluded from git via `.gitignore`
- Created an authenticated client:
  ```python
  from dotenv import load_dotenv
  load_dotenv()
  from anthropic import Anthropic

  client = Anthropic()
  model = "claude-sonnet-4-6"
  ```

### 2. First API request
- Learned the required parameters for `client.messages.create()`: `model`, `max_tokens`, `messages`
- Extracted the generated text via `message.content[0].text`
- Understood `max_tokens` as a safety cap, not a generation target

### 3. Multi-turn conversations
- Learned that Claude is stateless — no memory between requests
- Built helper functions to manage conversation history manually:
  ```python
  def add_user_message(messages, text): ...
  def add_assistant_message(messages, text): ...
  def chat(messages, system=None, stop_sequences=[]): ...
  ```
- Practiced maintaining a `messages` list across multiple turns so follow-up questions ("Write another sentence") resolve correctly
- Built a simple CLI loop (`while True` + `input()`) to chat interactively while preserving context

### 4. System prompts
- Learned that `system` sets Claude's role/behavior and is separate from the `messages` history
- Compared the same user question under different `system` prompts (default / formal support agent / friendly e-commerce assistant) to see how tone and format change without changing the underlying question

### 5. Structured output generation (prefill + stop sequences)
- Learned the "assistant message prefill" pattern: seeding the assistant turn with an opening marker (e.g. `` ```json ``) so Claude continues directly into the content
- Used `stop_sequences=["```"]` to cut generation exactly at the closing marker, avoiding extra commentary
- Extended `chat()` to accept `stop_sequences` as a parameter, since it wasn't originally supported
- Practiced this pattern for generating clean JSON, bash commands, and Python dicts — output usable directly by code, with no parsing needed

## Next up
- Streaming responses
- Structured output generation (deeper dive)
- Prompt engineering & evaluation section
