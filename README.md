# Scrappy

Scrappy is a lightweight, distributed personal AI infrastructure platform that turns old computers into a coordinated cluster for running AI, automation, and self-hosted services efficiently.

## The Idea

Most people have old laptops and desktops sitting around doing nothing. Scrappy puts them to work. Instead of paying for cloud servers or buying expensive hardware, Scrappy connects your existing machines into a personal compute cluster that gets smarter over time.

## How It Works

Scrappy routes every request through an intelligent layer that learns who is asking, what they usually need, and what hardware is available — then picks the best path automatically.

**Example:**
- Billy uses one laptop and mostly asks simple questions. Scrappy learns this and sets up a lightweight local assistant for him.
- Bob has three machines and does deep research. Scrappy distributes his workloads across all of them.

Each user's setup adapts to their patterns over time without any manual configuration.

## Architecture

```
User
  |
  v
main.py (CLI Interface)
  |
  v
router.py (Intelligent Router)
  |
  +---> local.py  (Local Model Inference)
  |
  +---> remote.py (Remote/Distributed Inference)
  |
  v
Response
```

### Core Components

| Component | Purpose |
|-----------|---------|
| `main.py` | CLI entry point and interaction loop |
| `router.py` | Routes queries based on complexity and user profile |
| `local.py` | Runs inference on the local machine |
| `remote.py` | Distributes tasks to remote worker nodes |
| `embed.py` | Converts queries to vectors for semantic routing |

## Routing

The router uses **embedding-based semantic routing** rather than simple keyword matching. Each query is converted into a vector and compared against previous requests to find the best path. Over time the router builds a profile per user — learning their typical query complexity, available hardware, and preferred response patterns.

Routing decision factors:
- Query embedding vs. historical query vectors (cosine similarity)
- User profile and past routing decisions
- Available hardware at runtime
- Task complexity classification

## User Profiles

Scrappy identifies users automatically from the system and loads their profile on startup. Profiles store:
- Available hardware nodes
- Query history and routing outcomes
- Typical workload complexity
- Preferred model configurations

This means Scrappy gets faster and more accurate the more you use it — no manual setup required.

## Goals

- Run personal AI models locally without cloud dependency
- Reuse old hardware that would otherwise sit unused
- Build a platform that grows by simply adding more machines
- Learn distributed systems concepts through a real project
