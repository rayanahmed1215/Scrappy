# Scrappy

Scrappy is an experimental personal AI infrastructure project exploring how prompts can be routed across local models, remote models, and eventually a network of reusable computers.

The long-term goal is to turn old laptops and desktops into coordinated worker nodes for AI inference, automation, and self-hosted services.

## Current Status

Scrappy is currently an early proof of concept for semantic prompt routing.

The current version includes:

* An embedding-based semantic router
* A FAISS vector index
* Local-versus-remote route selection
* A command-line interface
* Placeholder local and remote execution handlers

The local and remote handlers currently return simulated responses. They allow the routing architecture to be developed and tested before real models and worker nodes are introduced.

Distributed worker nodes, hardware-aware routing, real model inference, persistent storage, and user profiles are planned but not yet implemented.

## The Idea

Many people have old laptops and desktops sitting unused. Scrappy explores whether those machines can be connected into a personal compute cluster instead of relying entirely on cloud infrastructure or expensive new hardware.

A completed version of Scrappy would evaluate an incoming task, inspect the available resources, and select an appropriate model or worker node.

For example:

* A simple request could be handled by a lightweight model running locally.
* A complex request could be sent to a more capable machine or remote model.
* A larger task could eventually be divided among multiple worker nodes.

## Current Architecture

```text
User
  |
  v
main.py (CLI)
  |
  v
router.py (Semantic Router)
  |
  +---> local.py  (Placeholder Local Handler)
  |
  +---> remote.py (Placeholder Remote Handler)
  |
  v
Response
```

## Core Components

| Component          | Current purpose                                   |
| ------------------ | ------------------------------------------------- |
| `main.py`          | Runs the command-line interaction loop            |
| `router/router.py` | Selects a local or remote route                   |
| `router/embed.py`  | Converts prompts into vector embeddings           |
| `router/index.py`  | Stores and searches normalized vectors with FAISS |
| `models/local.py`  | Provides a placeholder for local inference        |
| `models/remote.py` | Provides a placeholder for remote inference       |

## Semantic Routing

Scrappy currently routes prompts using embedding similarity instead of relying entirely on keyword matching.

When the application starts, predefined examples for the local and remote routes are converted into embeddings and stored in a FAISS index. A new prompt is embedded and compared with those examples using cosine similarity.

The closest example determines the route when its similarity score meets the configured confidence threshold. Prompts below that threshold default to the remote route.

This implementation is experimental. Its accuracy is currently limited by the size and diversity of the example dataset.

## Planned Development

Future versions of Scrappy may include:

* Real local-model inference
* Remote worker-node communication
* Hardware and workload monitoring
* Intent and resource-aware routing
* Persistent routing data
* User-specific configuration
* Multi-worker task coordination
* Routing evaluation and automated tests

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

## Example

```text
You: Give me a quick greeting
Route: local
Scrappy: [LOCAL MODEL] Give me a quick greeting

You: Perform an advanced analysis of this dataset
Route: remote
Scrappy: [REMOTE MODEL] Perform an advanced analysis of this dataset
```

These responses are placeholders. The example demonstrates the routing decision rather than real model inference.

## Project Goals

* Explore semantic and resource-aware AI routing
* Run personal AI models with less cloud dependence
* Reuse hardware that would otherwise sit unused
* Design a system that can grow as machines are added
* Learn AI infrastructure and distributed-systems concepts through implementation

## License

See [LICENSE](LICENSE).
