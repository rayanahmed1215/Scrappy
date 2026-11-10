"""Turns text into vectors locally, for the router."""

import os
import numpy as np

# bge-small beat MiniLM on the eval (97% vs 92% on 225 queries) at ~4 ms/query; see documentation/router.md
DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"


def normalize(vecs) -> np.ndarray:
    """Scale each row to length 1, so dot product == cosine similarity."""
    vecs = np.asarray(vecs, dtype="float32")
    if vecs.ndim == 1:
        vecs = vecs[None, :]
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms[norms == 0] = 1.0  # avoid dividing by zero on an empty vector
    return vecs / norms


class FastEmbedEmbedder:
    """Runs a small embedding model (bge-small by default) on your machine. Downloads once, then offline."""

    name = "fastembed"

    def __init__(self, model: str = DEFAULT_MODEL):
        from fastembed import (
            TextEmbedding,
        )  # imported here so other backends don't need it

        self.model_name = model
        self._model = TextEmbedding(model_name=model)
        self.dim = len(self.embed("dimension probe"))  # 384 for bge-small and MiniLM

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        # .embed() returns a generator, so list() it before making an array
        return normalize(np.array(list(self._model.embed(texts))))

    def embed(self, text: str) -> np.ndarray:
        return self.embed_batch([text])[0]


BACKENDS = {"fastembed": FastEmbedEmbedder}


def make_embedder(backend: str | None = None, **kwargs):
    """Pick a backend by name, or from SCRAPPY_EMBED_BACKEND (default: fastembed).
    Extra kwargs (e.g. model=...) go to the backend."""
    backend = backend or os.getenv("SCRAPPY_EMBED_BACKEND", "fastembed")
    if backend not in BACKENDS:
        raise ValueError(f"Unknown backend {backend!r}; choose from {list(BACKENDS)}")
    return BACKENDS[backend](**kwargs)
