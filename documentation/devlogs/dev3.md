# Scrappy DevLog 3 — Router Testing

## Overview

Removed the FAISS index from the router and added an eval script to measure how accurate and how fast routing is. This builds on the earlier switch to local embeddings with fastembed, so routing now runs fully offline after the first model download.

---

## Architecture 

client → main.py → router → embedder (fastembed, local) → cosine similarity (numpy) → route decision → local.py / remote.py → response

---

## Components

### main.py
CLI entry point. Handles user input and runs the main interaction loop. Passes queries into the routing system.

### router.py *
Core decision engine. Keeps the example embeddings in a numpy array and picks the route of the closest example by cosine similarity. `decide()` returns the route, the score, the matched example, and the reason.

### embed.py *
Converts queries into embeddings locally with fastembed (all-MiniLM-L6-v2 by default). `make_embedder()` picks the backend and can take a model name, so other embedders can be tested.

### index.py *
Removed. FAISS was no longer needed for a small set of examples.

### tests/eval_router.py *
Runs labeled queries through the router and prints accuracy per route, ms per query, every misroute, and accuracy across thresholds.

### tests/route_cases.json *
Seed examples and labeled test queries for the code, talk, and refine routes, plus vague queries that should fall back.

### local.py
Handles execution of queries routed to local inference. Currently a placeholder implementation.

### remote.py
Handles execution of queries routed to cloud or API-based models. Currently a placeholder implementation.

### documentation/
Stores development logs, experiments, and system design notes.

---

## Current Behavior

- Routing runs fully local. No API key is needed.
- `python -m tests.eval_router` tests the router on 36 labeled queries (12 per route) and 5 vague ones.
- Results with 6 seed examples per route:

| | MiniLM | bge-small |
|---|---|---|
| Speed | 2.0 ms/query | 3.6 ms/query |
| Accuracy at threshold 0.6 | 36% | 86% |
| Best threshold | 0.25 → 81%, all vague queries fall back | 0.55 → 92%, no vague queries fall back |

- With no threshold, MiniLM's closest example has the right route 33/36 times.

---

## Known Limitations

- The 0.6 threshold is far too high for MiniLM. Its scores run low (right matches have a median of 0.31), so most correct matches get thrown away.
- Thresholds depend on the model. bge-small scores everything higher, including vague queries (0.62–0.73), so no threshold separates them from real ones.
- Only 6 seed examples per route. Code queries are the weakest.
- main.py still uses the old local/remote routes with a 0.6 threshold and a remote fallback, so live routing doesn't use these results yet.

---

## Implementation Notes

- Embeddings are normalized to length 1, so a plain dot product gives the cosine score. That made FAISS unnecessary.
- The eval script scores every query once, then applies each threshold afterward, so the threshold sweep is free.
- Uncertain queries fall back to talk in the eval, since it's the cheapest route. Refine runs twice (draft then refine), so sending a simple query there is the most expensive mistake.

---

## Next Steps

- Add more and better seed examples per route, especially code, then rerun the eval.
- Test more embedders with `--model`.
- Pick a threshold and fallback from the eval results.
- Switch main.py to the code / talk / refine routes.
- Add pytest unit tests with a fake embedder.

---

## Thoughts

The router doesn't need to be very accurate. General areas should be fine, and speed is the main thing. The router only runs on the main system that sets up routes, not on the nodes, and at a few ms per query it won't be the slow part next to model inference on old hardware. The real question is which mistakes waste the most compute.

We will remove the remote fallback for now. Uncertain queries should stay local, which fits the local-first goal, and remote can come back later as an optional expansion.
