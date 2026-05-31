from typing import Callable
import embed
import numpy as np
# Second Draft for routing using embeddings

# Main Function for routing a query 
# Str -> embeds -> vector -> cosine similarity -> model call 
def route_query(query: str)-> Callable[[str], str]:
    query_vector = embed(query)

    documented_vector = np.array()
    compare_vectors(query_vector, document_vector)
    return

def embed_vector(query: str) -> np.array:


    return 

def compare_vectors(compare_vector1: np.array, compare_vector2: np.array) -> int:


    return 