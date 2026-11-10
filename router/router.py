import json
from pathlib import Path

import numpy as np

from router.embed import make_embedder

EXAMPLES = Path(__file__).with_name("examples.json")


def load_examples(path=EXAMPLES) -> list[tuple[str, str]]:
    """Read {route: [example queries]} into (query, route) pairs."""
    data = json.loads(Path(path).read_text())
    return [(q, route) for route, queries in data.items() for q in queries]

# Routes a query to the route of its closest example (cosine similarity).
# Embeddings are unit length, so a dot product is the cosine score.
# Confidence is the margin: how far the best route is ahead of the runner-up.
# Raw scores depend on the embedder; near-ties are what signal a guess.


class Router:
    def __init__(self, embedder=None, min_margin: float = 0.10, fallback: str = "talk"):
        # Local embedder; backend set by SCRAPPY_EMBED_BACKEND (default: fastembed)
        self.embedder = embedder or make_embedder()
        self.min_margin = min_margin
        self.fallback = fallback  # local route used when the router is unsure
        self.vectors = np.empty((0, self.embedder.dim), dtype="float32")
        self.examples = []  # (query, route), same order as self.vectors

    def add_rules(self, rules: list[tuple[str, str]]):
        """Add many (query, route) examples in one embedding batch."""
        if not rules:
            return
        vecs = self.embedder.embed_batch([q for q, _ in rules])
        self.vectors = np.vstack([self.vectors, vecs])
        self.examples.extend(rules)

    def add_rule(self, query: str, route: str):
        self.add_rules([(query, route)])

    def decide(self, query: str) -> dict:
        """Pick a route and say why: best match, its score, the margin, and whether we fell back."""
        if not self.examples:
            return {"route": self.fallback, "score": 0.0, "margin": 0.0, "match": None,
                    "runner_up": None, "reason": "no examples"}

        scores = self.vectors @ self.embedder.embed(query)

        # best score per route, then compare the top two routes
        best_by_route = {}
        for i, (_, route) in enumerate(self.examples):
            if route not in best_by_route or scores[i] > scores[best_by_route[route]]:
                best_by_route[route] = i
        ranked = sorted(best_by_route, key=lambda r: scores[best_by_route[r]], reverse=True)

        top = ranked[0]
        score = float(scores[best_by_route[top]])
        runner_up = ranked[1] if len(ranked) > 1 else None
        margin = score - float(scores[best_by_route[runner_up]]) if runner_up else score
        result = {"score": score, "margin": margin, "match": self.examples[best_by_route[top]][0],
                  "runner_up": runner_up}

        if margin < self.min_margin:
            return {**result, "route": self.fallback,
                    "reason": f"near tie between {top} and {runner_up} "
                              f"(margin {margin:.2f} < {self.min_margin}), fell back to {self.fallback}"}
        return {**result, "route": top,
                "reason": f"{top} ahead of {runner_up} by {margin:.2f}"}

    def route(self, query: str) -> str:
        return self.decide(query)["route"]
