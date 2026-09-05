# Building with the Claude API — RAG and Agentic Search

Notes for the "RAG and Agentic Search" section — building a retrieval pipeline so Claude can
answer questions grounded in your own documents instead of just its training data.

> Note: written from general RAG best practices — plug in your own notebook code and results
> once you run through the lessons.

## Topics

### 1. Introducing Retrieval Augmented Generation

- The core problem: Claude has no knowledge of your private/internal documents, and stuffing
  everything into the prompt doesn't scale (context limits, cost, noise)
- RAG solves this by retrieving only the relevant pieces of text at query time and injecting
  them into the prompt as context before Claude answers

### 2. Text chunking strategies

- Documents need to be split into smaller pieces ("chunks") before they can be embedded/searched
- Common strategies: fixed-size chunks, chunking by section/heading, sentence-aware chunking,
  overlapping chunks (to avoid cutting relevant context at a boundary)
- Chunk size is a trade-off: too small loses context, too large dilutes relevance and wastes
  tokens

### 3. Text embeddings

- Each chunk gets converted into a vector (embedding) that captures its semantic meaning
- Similar meanings → similar vectors → similarity search (e.g. cosine similarity) finds
  conceptually related chunks even without exact keyword overlap

### 4. The full RAG flow

```
User question
   ↓
Embed the question
   ↓
Similarity search against chunk embeddings → top-k relevant chunks
   ↓
Insert chunks into prompt as context
   ↓
Claude generates an answer grounded in the retrieved context
```

### 5. Implementing the RAG flow

- Hands-on build of the above pipeline end-to-end: chunk → embed → store → retrieve → prompt →
  answer
- Also where you start noticing semantic search's blind spot: it can miss exact-term lookups
  (IDs, codes, specific names) — see BM25 lesson

### 6. BM25 lexical search

- Classic keyword-based search (term frequency + rarity weighting) as a complement to semantic
  search — critical for exact matches semantic search alone misses (e.g. `INC-2023-Q4-011`)
- Combining both = **hybrid search**: run semantic + BM25 in parallel, merge/re-rank results
- (See separate `BM25Index` notes — implemented on top of `rank_bm25`'s `BM25Okapi`)

### 7. A Multi-Index RAG pipeline

- Real-world document sets often aren't uniform (e.g. code docs vs. policy docs vs. support
  tickets) — a single index/chunking strategy doesn't fit all of them well
- Multi-index RAG: maintain separate indexes per document type/source, query the relevant
  index(es) based on the question, and merge results before passing to Claude
- Sets up the idea of **agentic search**: instead of always retrieving the same way, the agent
  can decide _which_ index(es) to query and _how_ (semantic, lexical, or both) based on the
  question

## Why this section matters for my roadmap

This directly upgrades Nordic Shop's existing from-scratch RAG (tokenization → TF-IDF → cosine
similarity). Concrete next steps for that project:

- Add BM25 alongside the existing TF-IDF/semantic search → hybrid search
- Revisit chunking strategy for product descriptions/reviews
- Consider a multi-index setup if product data, reviews, and FAQ/support content are indexed
  separately
