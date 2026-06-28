# Scrappy DevLog X — [Feature Name]

## Overview



---

## Architecture 

client → main.py → router → embedder → index (FAISS) → route decision → local.py / remote.py → response

---

## Components

### main.py
CLI entry point. Handles user input and runs the main interaction loop. Passes queries into the routing system.

### router.py
Core decision engine. Uses embeddings + FAISS similarity search to determine whether a query should be routed to local or remote execution.

### embed.py
Converts raw user queries into vector embeddings using a model (currently OpenAI for testing). These vectors are used for similarity matching.

### index.py
Stores embedding vectors and performs similarity search using FAISS. Returns the closest matching routing intent.

### local.py
Handles execution of queries routed to local inference. Currently a lightweight/toy implementation.

### remote.py
Handles execution of queries routed to cloud or API-based models. Currently a placeholder implementation.

### documentation/
Stores development logs, experiments, and system design notes.

---

## Current Behavior


---

## Known Limitations


---

## Implementation Notes


---

## Next Steps


---

## Thoughts
