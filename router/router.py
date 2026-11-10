import numpy as np

from router.embed import make_embedder

# Routes a query to the route of its closest example (cosine similarity).
# Embeddings are unit length, so a dot product is the cosine score.


class Router:
    def __init__(self, embedder=None, threshold: float = 0.6, fallback: str = "remote"):
        # Local embedder; backend set by SCRAPPY_EMBED_BACKEND (default: fastembed)
        self.embedder = embedder or make_embedder()
        self.threshold = threshold
        self.fallback = fallback  # used when no example is close enough
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
        """Pick a route and say why: best match, its score, and whether we fell back."""
        if not self.examples:
            return {"route": self.fallback, "score": 0.0, "match": None,
                    "reason": "no examples"}

        scores = self.vectors @ self.embedder.embed(query)
        best = int(np.argmax(scores))
        score = float(scores[best])
        match, route = self.examples[best]

        if score < self.threshold:
            return {"route": self.fallback, "score": score, "match": match,
                    "reason": f"below threshold {self.threshold} (closest: {route})"}
        return {"route": route, "score": score, "match": match, "reason": "closest example"}

    def route(self, query: str) -> str:
        return self.decide(query)["route"]
