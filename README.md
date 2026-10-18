# Scrappy

**Old computers. One AI cluster.**

Progress in AI has mostly come from adding more compute: bigger models, bigger data centers, bigger cloud bills. Scrappy takes the opposite approach. Instead of scaling up, it makes the most of the hardware people already own by pooling old laptops, desktops, and spare servers into a single local AI cluster.

Scrappy is an open-source, local-first AI infrastructure project. You send a query, and Scrappy decides how it should run, which machine should run it, and which models to use, so you don't have to pick models or paths by hand.

> **Status:** early development. The router is a working prototype, and the cluster is being built this semester as a team project with the RPI AI club (RPAI). See [Current status](#current-status).

## Why Scrappy

- **Use what you have.** Idle machines become shared compute instead of e-waste.
- **Local-first.** Work runs on your own hardware whenever it makes sense. The cloud is optional and only used as an expansion, never a requirement.
- **Private by default.** Your queries and data stay on machines you control.
- **Grows with you.** Add a machine and the cluster gets more capable.

## How it works

```text
            User query
                 |
                 v
     +-----------------------+
     |        Router         |   decides how the query should run
     +-----------+-----------+
                 |
                 v
     +-----------------------+
     |        Cluster        |
     |  +-----------------+  |
     |  |    Scheduler    |<-+-- NodeWatch reports from every node
     |  +--------+--------+  |
     |           |           |
     |   +-------+-------+   |
     |   v       v       v   |
     | Node 1  Node 2  Node 3|   each node runs a Workplace
     +-----------+-----------+
                 |
                 v
             Response

  Observe   records what happened at every step
  Context   gives models the right information
  Adaptive  learns from Observe to improve future decisions
```

## Modules

Scrappy is built as a set of modules. Each one works on its own with simple inputs and outputs, so they can be developed, tested, and swapped independently.

| Module | What it does | Status |
|---|---|---|
| **Router** | Decides the best route for a query by comparing it to past queries and their routes | Working prototype |
| **Cluster** | Tracks every machine, decides which one runs each task, and runs the models | In development |
| **Observe** | Collects telemetry: route, model, node, latency, tokens, CPU/RAM/GPU use, errors, and outcomes | Planned |
| **Context** | Stores, retrieves, and injects relevant context such as conversation history, files, and past outputs | Planned |
| **Adaptive** | Learns from Observe data and user feedback to personalize routing and scheduling | Planned |

### Router

The router turns a query into an embedding and compares it with an index of example queries using FAISS. The closest match decides the route when it is confident enough, and uncertain queries fall back to a default route.

Planned improvements include confidence scoring and routing that accounts for privacy, cost, available hardware, latency, and which models are available.

See [documentation/router.md](documentation/router.md) for details.

### Cluster

Cluster combines your machines into one system. It is made of four components:

| Component | Role |
|---|---|
| **NodeWatch** | Runs on every machine and reports its health, hardware, and current tasks. Written in Rust. |
| **Scheduler** | Uses NodeWatch reports to decide which machine runs each task, based on what the task needs and how busy each node is. Reassigns work if a node goes down. |
| **Workplace** | The environment where models run. Loads models onto a node and runs queries through them. Models working on the same query share one context. |
| **Infrastructure** | Docker environments for simulated nodes, networking between machines, and a hardware testbed built from repurposed computers. |

Cluster accepts model selection as an input, so it can come from simple rules, the user, or the Router.

#### Cluster milestones

| # | Milestone | Done when |
|---|---|---|
| 0 | **Simulated nodes.** Develop on one host, with Docker containers acting as nodes with their own CPU and memory limits. | Components talk over the network from the start. |
| 1 | **NodeWatch on one node.** | It reliably reports CPU, RAM, and running tasks, and the values match the system. |
| 2 | **Scheduler tracks and assigns.** | A submitted task runs on the node and the scheduler's record stays current. |
| 3 | **Workplace runs a model.** | Queries sent through the scheduler return correct output across repeated runs. |
| 4 | **Multiple nodes.** | Tasks are split across two nodes by load, and stopping one node reassigns its work. |
| 5 | **Real hardware.** | The cluster works across two physical machines with the same capabilities as Milestone 4. |
| 6 | **Shared context.** | A query passes through models on two nodes, and the second uses the first one's result. |

## Current status

**Working now**
- Embedding-based router with a FAISS vector index
- Local-versus-remote route selection with a confidence threshold
- Command-line interface

**In progress**
- Cluster (NodeWatch, Scheduler, Workplace, Infrastructure), as the RPAI team project for Fall 2026
- An intent layer for the router

**Not yet implemented**
- Real model inference. The local and remote handlers currently return placeholder responses so the routing can be developed and tested first.
- Local embeddings. Embeddings currently come from an API through OpenRouter during prototyping and will be replaced with a local embedding model.
- Observe, Context, and Adaptive

## Roadmap

| Phase | Focus | Modules |
|---|---|---|
| **V1: Orchestration** | Route queries and run them across machines | Router, Cluster |
| **V2: Optimization** | Measure everything and improve performance | Observe, refactors |
| **V3: Personalization** | Give models the right context and learn from use | Context, Adaptive |

Longer term, Scrappy aims to split complex queries into subtasks that run in parallel across nodes, keep frequently used models ready on the right machines, and serve as shared local compute for other projects built on top of it.

## Design principles

- **Local-first.** Use local compute whenever it makes sense.
- **Modular.** Each module works independently with clear inputs and outputs.
- **Hardware-aware.** Decisions account for what each machine can actually do.
- **Model-agnostic.** No dependence on a single model or provider.
- **Clear-box.** Every routing decision and tool call should be visible and explainable.

## Repository layout

```text
Scrappy/
├── main.py            # CLI entry point
├── router/            # Router: embeddings, FAISS index, routing logic
├── models/            # Placeholder local and remote handlers
└── documentation/     # Devlogs, design notes, and module docs
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/rayanahmed1215/Scrappy.git
cd Scrappy
```

### 2. Create and activate a virtual environment

Linux or macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the embedding API

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then add your OpenRouter API key to `.env`:

```env
OPENROUTER_API_KEY=your_api_key_here
```

### 5. Run Scrappy

```bash
python main.py
```

Enter `exit` or `quit` to stop the program.

### Example

```text
You: Give me a quick greeting
Route: local
Scrappy: [LOCAL MODEL] Give me a quick greeting

You: Perform an advanced analysis of this dataset
Route: remote
Scrappy: [REMOTE MODEL] Perform an advanced analysis of this dataset
```

These responses are placeholders. The example shows the routing decision, not real model output.

## Contributing

Scrappy Cluster is being built by a student team through RPAI, and contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow. All contributors must sign the [Contributor License Agreement](CLA.md) before their pull requests can be merged.

## License

Scrappy is licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only). See [LICENSE](LICENSE).
