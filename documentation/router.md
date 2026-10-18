# Router

The router decides how a query should run. It is currently a working prototype that chooses between a local route and a remote route.

## How it works

1. **Build the index.** When Scrappy starts, a set of example queries for each route is converted into embeddings and stored in a FAISS index (`router/index.py`).
2. **Embed the query.** A new query is converted into an embedding with the same model (`router/embed.py`).
3. **Find the closest example.** FAISS compares the query to the stored examples using cosine similarity. Vectors are L2-normalized, so the inner-product index returns cosine scores.
4. **Decide.** If the closest example's score meets the confidence threshold (currently 0.6), the query takes that example's route. Otherwise it falls back to the remote route (`router/router.py`).

Routing examples are added with `Router.add_rule(query, route)`. They are currently defined in `main.py`.

## Files

| File | Purpose |
|---|---|
| `router/router.py` | Routing logic and confidence threshold |
| `router/embed.py` | Converts text into embeddings (`all-MiniLM-L6-v2` through OpenRouter, 384 dimensions) |
| `router/index.py` | FAISS vector index with metadata for each example |
| `router/intent.py` | Early keyword-based intent classifier for the planned intent layer (not yet wired in) |

## Known limitations

- Accuracy is limited by the small number of routing examples.
- Embeddings currently come from an API, which conflicts with Scrappy's local-first goal. A local embedding model will replace it.
- Only two routes exist: local and remote.

## Planned improvements

- An intent layer between routing and model calls
- Confidence scoring
- Routing that accounts for privacy, cost, available hardware, latency, and model availability
- Storing past queries with their routes and outcomes, so successful routes inform future ones
- Handing routing decisions to Cluster as its model-selection input

For the history of how the router evolved, see the devlogs in `documentation/devlogs/`.
