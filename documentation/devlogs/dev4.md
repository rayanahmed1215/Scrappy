# Scrappy DevLog 4 — Margin Scoring and Code/Talk/Refine Routes

## Overview

Replaced the score threshold with a margin check, removed the remote fallback, and switched the CLI to the code, talk, and refine routes. Uncertain queries now fall back to talk, and no route reaches remote anymore.

---

## Architecture 

client → main.py → router → embedder (fastembed, local) → cosine similarity (numpy) → margin check → route (code / talk / refine) → handler → response

---

## Components

### main.py *
CLI entry point. Loads the seed examples, routes each query, prints the route with its reason, and calls that route's handler.

### router.py *
Core decision engine. Takes the best score in each route and compares the top two. If the winner is ahead by at least `min_margin` (0.10) it wins, otherwise the query falls back to talk. `load_examples()` reads the seed file.

### examples.json *
New. Seed example queries for each route. `main.py` and the eval read the same file, so the eval measures what the CLI does.

### embed.py
Converts queries into embeddings locally with fastembed (all-MiniLM-L6-v2 by default).

### local.py *
Placeholder handlers for code, talk, and refine, plus a `HANDLERS` map. Refine runs two steps: draft, then refine.

### remote.py *
Removed. Remote can come back later as an optional expansion.

### tests/eval_router.py *
Now measures the margin instead of the raw score: `--margin`, margin spread, and a margin sweep from 0.00 to 0.30.

### tests/route_cases.json *
Labeled test queries and vague queries only. The seeds moved to `examples.json`.

### documentation/
Stores development logs, experiments, and system design notes.

---

## Current Behavior

- The router picks a route only when it is clearly ahead of the runner-up. Near ties go to talk, with a reason like `near tie between talk and refine (margin 0.06 < 0.1), fell back to talk`.
- Eval on MiniLM, before and after:

| | Score ≥ 0.6 (before) | Margin ≥ 0.10 (after) |
|---|---|---|
| Accuracy | 36% (13/36) | 89% (32/36) |
| Vague queries caught | 5/5 | 5/5 |
| Speed | 2.4 ms/query | 2.2 ms/query |

- All 4 remaining misroutes have a margin of 0.05 or less, so they fall back to talk instead of guessing wrong.
- The CLI sends "Implement binary search in C" to code, "hello there" to talk, an essay request to refine, and "hmm" to talk.

---

## Known Limitations

- The margin cutoff depends on the model. bge-small gets 67% at 0.10 and does best near 0.08 (81%, 3/5 vague caught).
- The test set is small (36 labeled queries), so one query moves accuracy by about 3%.
- Only 6 seed examples per route. Code is still the weakest route.
- The handlers are placeholders. Refine can't be tested end to end until Cluster Milestones 4 and 6.

---

## Implementation Notes

- An audit showed the scores were computed correctly. MiniLM just scores short phrases low (right matches had a median of 0.31), so a fixed 0.6 cutoff threw away most correct matches.
- When the router picked the wrong route, the top two routes were almost always tied (median margin 0.00). That's why the margin works as a confidence signal.
- Talk is the fallback because it is one cheap local model call. Refine runs two models, so a wrong guess there wastes the most compute.

---

## Next Steps

- Add more seed examples, especially for code, then rerun the eval.
- Grow the test set to about 30 queries per route.
- Add pytest unit tests with a fake embedder.
- Open the PR into `dev`.

---

## Thoughts

The remote fallback is gone for now, and so is the remote handler. Uncertain queries stay local, which fits the local-first goal. Remote can come back later as an optional expansion, not a default.
