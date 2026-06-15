# router/embedder.py
from openai import OpenAI

client = OpenAI()
# Simple Embedder class to generate embeddings for routing
# Uses text-embedding-3-small model for efficient embedding generation

class Embedder:
    def __init__(self, model="text-embedding-3-small"):
        self.model = model

    def embed(self, text: str):
        res = client.embeddings.create(
            model=self.model,
            input=text
        )
        return res.data[0].embedding