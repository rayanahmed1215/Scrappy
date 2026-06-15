import numpy as np
import embed
import index

# Second Draft for routing using embeddings

class Router: 
    def __init__(self):
        self.embedder = embed.Embedder()
        self.index = index.VectorIndex(dim=1536)  # Assuming 1536-dim embeddings

        # Add Basic routing examples to the index
        self.index.add(
        self.embedder.embed("execute inference on local machine without API calls"),
        {"route": "local"}
        )

        self.index.add(
        self.embedder.embed("execute inference using cloud API or remote large model"),
        {"route": "remote"}
        )

    # Route query based on embedding similarity to examples in the index 
    def route(self, query: str) -> str:
        query_vec = self.embedder.embed(query)
        results = self.index.search(query_vec, k=1)

        if not results:
            return "remote"
        
        best = results[0]

        if best["score"] < 0.6:
            return "remote"
       
        return best["meta"]["route"]