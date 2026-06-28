# Scrappy DevLog 1 — Embedding Router

## Overview

This log documents the initial implementation of Scrappy’s embedding-based routing system.

I refactored the router to use a dedicated embedding and indexing pipeline to classify user queries and determine whether they should be handled locally or remotely.

The system currently uses OpenAI embeddings for testing, with a FAISS-based similarity index to compare queries against predefined routing examples.

---

## Architecture

client → main.py → router → embedder → index (FAISS) → route decision → local.py / remote.py → response

---

## Components

### main.py
CLI entry point and interactive loop for user queries.

### router.py *
Core decision layer. Uses embeddings + FAISS similarity search to determine whether a query should be routed locally or to a remote model.

### embed.py *
Converts input queries into vector embeddings (currently using OpenAI embeddings for testing).

### index.py *
Stores embedding vectors and performs similarity search using FAISS.

### local.py
Handles local model inference (toy implementation for now).

### remote.py
Handles remote/cloud model inference (toy implementation for now).

### documentation/
Development logs and system notes.

---

## Current Behavior

- Queries are converted into embeddings using the embedder.
- FAISS is used to find the closest matching routing example.
- The router selects either:
  - Local execution path
  - Remote execution path

Each route currently has only a small number of example queries (toy dataset).

---

## Known Limitations

- Routing accuracy is unstable due to a very small set of reference examples in the FAISS index.
- The system relies on sparse intent coverage, which makes similarity matching unreliable.
- OpenAI embeddings are used temporarily and will later be replaced with a fully offline model.

---

## Next Steps

- Expand routing dataset with more diverse query examples per intent (local vs remote).
- Improve FAISS stability by increasing coverage of edge-case queries.
- Add a confidence threshold for uncertain routing decisions.
- Replace OpenAI embeddings with a local embedding model.

---

## Thoughts

Initial experiments show that the routing logic works structurally, but performance is limited by the small number of example queries in the embedding index.

FAISS behaves correctly, but the decision boundary is too sparse to reliably distinguish between intents.