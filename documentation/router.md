# Router

The router decides how a query should run. It is currently a working prototype with three routes: code, talk and refine.

## How it works

1. **Embed the examples.** When Scrappy starts, a set of example queries for each route is converted into embeddings in one batch and kept in a numpy array.
2. **Embed the query.** A new query is converted into an embedding with the same model (`router/embed.py`).
3. **Find the closest example.** Vectors are unit length, so a dot product against every example gives the cosine similarity scores.
4. **Decide.** Take the best score in each route and compare the top two. If the best route is ahead of the runner-up by at least the margin (`min_margin`, default 0.03, tuned for bge-small), it wins. Otherwise it's a near tie, and the query falls back to a local default route (`fallback`, default `talk`). `Router.decide(query)` returns the route, score, margin, matched example, runner-up, and the reason.

Seed examples live in `router/examples.json` and are loaded with `load_examples()`. `main.py` and the eval use the same file, so the eval measures what the CLI does. `Router.add_rules(...)` / `add_rule(query, route)` add more.

## Files

| File | Purpose |
|---|---|
| `router/router.py` | Routing logic, margin check, fallback, `load_examples()` |
| `router/examples.json` | Seed example queries for each route |
| `router/embed.py` | Converts text into embeddings locally with fastembed (`BAAI/bge-small-en-v1.5` by default, 384 dimensions) |
| `router/intent.py` | Early keyword-based intent classifier for the planned intent layer (not yet wired in) |

## Known limitations

- Accuracy is limited by the small number of routing examples.
- The margin cutoff depends on the embedding model: 0.03 for bge-small, 0.10 for MiniLM. Re-run the eval when changing the embedder.
- At 0.03, bge-small gets 97% on 225 queries with no query sent confidently to the wrong route. One vague query ("fix it") lands on refine instead of talk.

## Choosing the embedder

bge-small replaced MiniLM as the default after the seed set grew to 15 per route. Results on the full eval (225 labeled queries, 40 vague):

| | MiniLM @ 0.10 | bge-small @ 0.03 |
|---|---|---|
| Accuracy | 92% | 97% |
| Sent confidently to the wrong route | 0 | 0 |
| Vague not landing on talk | 0/40 | 1/40 |
| Speed | ~2 ms/query | ~4 ms/query |

On the newest batch of 75 queries, written before either setting was picked, bge-small was also ahead (99% at margin 0.02 vs MiniLM's best of 96%). 0.03 was picked over 0.02 because 0.02 sent "Who wrote Pride and Prejudice?" to refine, the most expensive route.

## Measuring accuracy

`python -m tests.eval_router` routes the labeled queries in `tests/route_cases.json` and prints accuracy per route, speed per query, misroutes, margin spread, and accuracy across margin cutoffs. Use `--model` to compare embedders and `--margin` / `--fallback` to try settings. The set has 75 labeled queries per route and 40 vague ones. For vague queries it reports where they land (the fallback route) rather than only whether they fell back.

Unit tests: `python -m pytest` runs offline with a fake embedder. `SCRAPPY_SLOW=1 python -m pytest` also checks the real model stays above 80% accuracy and 80% vague fallback.

## Planned improvements

- An intent layer between routing and model calls
- Routing that accounts for privacy, cost, available hardware, latency, and model availability
- Storing past queries with their routes and outcomes, so successful routes inform future ones
- Handing routing decisions to Cluster as its model-selection input

For the history of how the router evolved, see the devlogs in `documentation/devlogs/`.
