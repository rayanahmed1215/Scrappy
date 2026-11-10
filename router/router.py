from router.embed import make_embedder
from router.index import VectorIndex

# Second Draft for routing using embeddings

class Router: 
    def __init__(self):
        # Local embedder; backend set by SCRAPPY_EMBED_BACKEND (default: fastembed)
        self.embedder = make_embedder()
        self.index = VectorIndex(dim=self.embedder.dim)

    # Add a new routing rule to the index with its corresponding embedding
    def add_rule(self, query: str, route: str): 
        query_vec = self.embedder.embed(query)
        self.index.add(query_vec, {"route": route})


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