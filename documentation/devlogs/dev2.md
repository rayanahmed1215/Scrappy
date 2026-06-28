# Scrappy DevLog 2 — Embedding Router

## Overview
Added in more examples into the router and changed the addition to be callable function to take a query and a route into it.


---

## Architecture 

client → main.py → router → embedder → index (FAISS) → route decision → local.py / remote.py → response

---

## Components

### main.py *
CLI entry point. Handles user input and runs the main interaction loop. Passes queries into the routing system.

### router.py * 
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
Now the behavior does work with additional examples albeit simple. It detects basic local and remote based on sameness.

---

## Known Limitations
Still inaccurate in some fields and one way to fix it is with more and more examples but my other plan is to focus down on the routes as in adding intents next

---

## Next Steps
Add in an intent layer in the router so query - into router - into intent layer - into model call

---

## Thoughts

No thoughts
