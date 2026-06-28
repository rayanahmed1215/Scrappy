from openai import OpenAI
import os


# Simple Embedder class to generate embeddings for routing
# Uses all-MiniLM-L6-v2 model for efficient embedding generation

class Embedder:
    def __init__(self, model="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = model
        self.client = OpenAI(
            base_url = "https://openrouter.ai/api/v1",
            api_key = os.getenv("OPENROUTER_API_KEY")
        )

    def embed(self, text: str) -> list[float]:
        res = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return res.data[0].embedding