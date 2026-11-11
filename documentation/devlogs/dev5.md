# Scrappy DevLog 5 — Router Testing and bge-small

## Overview

Expanded router testing: added offline unit tests, grew the seed examples from 6 to 15–16 per route, and grew the eval set from 36 to 225 labeled queries plus 40 vague ones. Based on the results, the default embedder switched from MiniLM to bge-small with a margin of 0.03.

---

## Architecture 

client → main.py → router → embedder (fastembed, bge-small, local) → cosine similarity (numpy) → margin check → route (code / talk / refine) → handler → response

---

## Components

### main.py
CLI entry point. Loads the seed examples, routes each query, prints the route with its reason, and calls that route's handler.

### router.py *
Core decision engine. Default `min_margin` is now 0.03, tuned for bge-small.

### examples.json *
Seed examples per route, now 15–16 each. Code was broadened the most (web, shell, git, Docker, CI, packages, APIs, performance, regex, threads).

### embed.py *
Converts queries into embeddings locally with fastembed. Default model is now `BAAI/bge-small-en-v1.5`.

### local.py
Placeholder handlers for code, talk, and refine.

### tests/test_router.py *
New. 17 offline unit tests with a fake embedder, plus an opt-in real-model accuracy floor.

### tests/eval_router.py *
Now reports where vague queries land, not just whether they fell back. `--margin` defaults to the Router's default.

### tests/route_cases.json *
75 labeled queries per route and 40 vague ones.

### requirements-dev.txt *
New. App requirements plus pytest, so normal installs stay small.

### documentation/
Stores development logs, experiments, and system design notes.

---

## Current Behavior

- bge-small at margin 0.03 routes 97% of the 225 labeled queries correctly, at about 4 ms per query.
- No query is sent confidently to the wrong route. Every misroute lands on talk, the cheap fallback.
- 39 of 40 vague queries land on talk.
- `python -m pytest` runs 17 unit tests offline in under a second. `SCRAPPY_SLOW=1 python -m pytest` also runs the real model.

---

## Known Limitations

- One vague query ("fix it") lands on refine instead of talk.
- The margin cutoff is model-specific: 0.03 for bge-small, 0.10 for MiniLM. Changing the embedder means re-running the eval and re-tuning.
- All seeds and test queries were written in one session from a single source, so they may share phrasing habits and not match how real users ask things.
- The handlers are placeholders. The eval measures routing, not answer quality.
- Refine can't be tested end to end until Cluster Milestones 4 and 6.

---

## Implementation Notes

### Testing methods

1. **Unit tests with a fake embedder.** The fake embedder looks up fixed vectors, so every score and margin is known ahead of time. The tests cover a clear winner, a near tie falling back with a reason, the default fallback being talk (never remote), the margin math, an empty router, a single-route router, `normalize`, an unknown backend, every route having a handler, refine running two steps, and the eval set not overlapping the seeds.
2. **Real-model floor.** An opt-in test fails if the real model drops below 80% accuracy or 80% of vague queries landing on talk.
3. **Eval script.** Runs every labeled query and reports accuracy per route, ms per query, margin spread, each misroute, and a margin sweep from 0.00 to 0.30.
4. **Held-out batches.** Test queries were added in batches, each written before the settings it was used to judge. This keeps the results honest, since queries written after seeing failures make the numbers look better than they are.
5. **Costly-misroute check.** Besides accuracy, each setting was checked for queries sent confidently to the wrong route, and for vague queries landing anywhere but talk. A misroute to refine wastes two model calls, so those count more than plain accuracy.
6. **Per-commit check.** The unit tests were run at each of the three commits on their own to make sure every commit works.

### Results

More seeds, measured with MiniLM at margin 0.10:

| | 6 seeds | 15 seeds |
|---|---|---|
| Original 90 queries | 87% | 94% |
| 60 queries written after the new seeds | — | 88% |
| Code route | 21/30 | 43/50 |

The 94% is partly inflated, since the seeds were written knowing which kinds of queries failed. The 88% on unseen queries is the honest number.

Embedder comparison on the newest 75 queries, written before either setting was picked:

| | MiniLM | bge-small |
|---|---|---|
| Best result | 96% (margin 0.06) | 98.7% (margin 0.02), all vague on talk |
| At margin 0.10 | 90.7% | 78.7% |

Choosing the margin on the full set (225 queries, 40 vague):

| | MiniLM @ 0.10 | bge-small @ 0.02 | bge-small @ 0.03 |
|---|---|---|---|
| Accuracy | 91.6% | 97.8% | 97.3% |
| Sent confidently to the wrong route | 0 | 1 | 0 |
| Vague not on talk | 0/40 | 1/40 | 1/40 |
| Speed | ~2 ms | ~4 ms | ~4 ms |

- 0.03 was picked over 0.02 because 0.02 sent "Who wrote Pride and Prejudice?" to refine, the most expensive route.
- At low margins (0.02–0.04), MiniLM sends 3–5 queries confidently to the wrong route, so its margin shouldn't be lowered.
- The eval used to count only vague queries that fell back. With the new "Hey there" seed, queries like "ok" and "hmm" matched talk directly, so that count dropped even though they still ended up on talk. The eval now counts where they land.

---

## Next Steps

- Open the PR into `dev`.
- Get test queries from other team members to check phrasing outside the current set.
- Decide whether "fix it" style follow-ups need conversation context (V3) or a seed.
- Save the seed embeddings to disk so they aren't re-embedded on every start.

---

## Thoughts

bge-small is the answer for now. It's slower than MiniLM, but at about 4 ms per query the router still won't be the slow part, and it routes more queries correctly without sending any to the expensive route by mistake.
