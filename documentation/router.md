# Router

The router decides how a query should run. It is currently a working prototype that chooses between a local route and a remote route.

## How it works

1. **Embed the examples.** When Scrappy starts, a set of example queries for each route is converted into embeddings in one batch and kept in a numpy array.
2. **Embed the query.** A new query is converted into an embedding with the same model (`router/embed.py`).
3. **Find the closest example.** Vectors are unit length, so a dot product against every example gives the cosine similarity scores.
4. **Decide.** If the closest example's score meets the confidence threshold (currently 0.6), the query takes that example's route. Otherwise it falls back to the remote route (`router/router.py`). `Router.decide(query)` returns the route plus the score, the matched example, and the reason.

Routing examples are added with `Router.add_rule(query, route)`. They are currently defined in `main.py`.

## Files

| File | Purpose |
|---|---|
| `router/router.py` | Routing logic and confidence threshold |
| `router/embed.py` | Converts text into embeddings locally with fastembed (`all-MiniLM-L6-v2` by default, 384 dimensions) |
| `router/intent.py` | Early keyword-based intent classifier for the planned intent layer (not yet wired in) |

## Known limitations

- Accuracy is limited by the small number of routing examples.
- Good thresholds depend on the embedding model. MiniLM scores run low, so the 0.6 threshold rejects most correct matches.
- Only two routes exist: local and remote.

## Measuring accuracy

`python -m tests.eval_router` routes the labeled queries in `tests/route_cases.json` and prints accuracy per route, speed per query, misroutes, and accuracy across thresholds. Use `--model` to compare embedders and `--threshold` / `--fallback` to try settings.

## Planned improvements

- An intent layer between routing and model calls
- Confidence scoring
- Routing that accounts for privacy, cost, available hardware, latency, and model availability
- Storing past queries with their routes and outcomes, so successful routes inform future ones
- Handing routing decisions to Cluster as its model-selection input

For the history of how the router evolved, see the devlogs in `documentation/devlogs/`.
