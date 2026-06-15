import faiss
import numpy as np

# Simple Vector Index using FAISS for efficient similarity search
# This class allows adding vectors with associated metadata and searching for similar vectors based on cosine similarity.

class VectorIndex:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []

    def add(self, vector, meta):
        vec = np.array([vector]).astype("float32")
        self.index.add(vec)
        self.metadata.append(meta)

    def search(self, vector, k=3):
        vec = np.array([vector]).astype("float32")

        D, I = self.index.search(vec, k)

        results = []

        for dist, idx in zip(D[0], I[0]):
            if idx == -1:
                continue

            results.append({
                "meta": self.metadata[idx],
                "score": float(dist)  
            })

        return results