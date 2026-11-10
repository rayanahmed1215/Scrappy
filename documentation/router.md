# Router

The router decides how a query should run. It is currently a working prototype. The eval uses the planned code / talk / refine routes; `main.py` still uses the older local / remote routes.

## How it works

1. **Embed the examples.** When Scrappy starts, a set of example queries for each route is converted into embeddings in one batch and kept in a numpy array.
2. **Embed the query.** A new query is converted into an embedding with the same model (`router/embed.py`).
3. **Find the closest example.** Vectors are unit length, so a dot product against every example gives the cosine similarity scores.
4. **Decide.** Take the best score in each route and compare the top two. If the best route is ahead of the runner-up by at least the margin (`min_margin`, default 0.10), it wins. Otherwise it's a near tie, and the query falls back to a local default route (`fallback`, default `talk`; `main.py` uses `local`). `Router.decide(query)` returns the route, score, margin, matched example, runner-up, and the reason.

Routing examples are added with `Router.add_rule(query, route)`. They are currently defined in `main.py`.

## Files

| File | Purpose |
|---|---|
| `router/router.py` | Routing logic, margin check and fallback |
| `router/embed.py` | Converts text into embeddings locally with fastembed (`all-MiniLM-L6-v2` by default, 384 dimensions) |
| `router/intent.py` | Early keyword-based intent classifier for the planned intent layer (not yet wired in) |

## Known limitations

- Accuracy is limited by the small number of routing examples.
- The margin cutoff depends on the embedding model. 0.10 fits MiniLM (89%); bge-small does better near 0.08. Re-run the eval when changing the embedder.
- The test set is small (36 labeled queries), so one query moves accuracy by about 3%.
- main.py still uses local / remote routes, so a confident remote match can still reach the remote handler.

## Measuring accuracy

`python -m tests.eval_router` routes the labeled queries in `tests/route_cases.json` and prints accuracy per route, speed per query, misroutes, margin spread, and accuracy across margin cutoffs. Use `--model` to compare embedders and `--margin` / `--fallback` to try settings.

## Planned improvements

- An intent layer between routing and model calls
- Routing that accounts for privacy, cost, available hardware, latency, and model availability
- Storing past queries with their routes and outcomes, so successful routes inform future ones
- Handing routing decisions to Cluster as its model-selection input

For the history of how the router evolved, see the devlogs in `documentation/devlogs/`.
