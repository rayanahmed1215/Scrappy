Notes on Scrappy design
Devnote 3: modular cluster and test cluster (draft)

The structure should be modular, so any node design can be plugged in and the fallback still works. To test it, build a test cluster that plugs into the cluster and the router. This is a draft and planning note, nothing is built yet.

## The contract

```
query → Router.decide() → route (models, steps) → Cluster.submit() → Scheduler.pick() → Node.run() → Result
```

- **Router:** query → route. A route says what the query needs (models, steps, constraints). It never names a node. When uncertain it returns the default local route. No remote fallback for now.
- **Cluster:** `submit(task)` → Result, where the task carries the selected model. The model can come from the router, a rule, or a CLI flag, so Cluster never imports Router. Owns the execution fallback and logs every step with its reason.
- Two separate maps, so a node failing never breaks routing:
  - route → models lives in Router.
  - node → loaded models lives in Cluster.

## The node plug point

Any node design only has to implement this:

```python
class Node(Protocol):
    id: str
    def health(self) -> NodeStatus: ...  # alive, budget, live usage, loaded models
    def run(self, task) -> Result: ...
```

- Nodes report the models they have loaded, not routes. Matching a route's model to a node is the Scheduler's job.
- `FakeNode`: in-memory test node.
- Real node: the design in `devlogs/nodestart.md` (node.toml + Podman + llama-server). `health()` reads the NodeWatch report, so the Rust side sits behind that one method.
- **Scheduler:** `pick(task, statuses)` → node. First rule: alive, has the task's model loaded, lowest load. Can change without touching anything else.

## Fallback chain

| Level | Who | Trigger | What happens |
|---|---|---|---|
| Routing | Router | score below cutoff | returns the default local route (talk) |
| Execution | Cluster | node down, timeout, or error | 1. another node with the same model loaded<br>2. a node with room to load that model<br>3. clear "no node can run this model" error with the reason, never a silent remote call |

The cluster never swaps the model itself, since that would break the route. If step 3 happens, the caller decides whether to retry with the default route.

## Test cluster

`FakeNode` options: `models`, `budget`, `latency_ms`, `fail_rate`, `down`. A small config builds 3–5 fake nodes. Fake nodes are test code only, so they live in `tests/`.

Scenarios:
1. All healthy: each task lands on a node with its model loaded, least-loaded first.
2. One node down: its work goes to another node with the same model.
3. No node has the model loaded: it goes to a node with room to load it.
4. Nothing can run the model: clean error with the reason, nothing hangs.
5. Slow node: times out and retries somewhere else.
6. End to end: router (fake embedder) → glue → cluster → fake nodes, checking the full path and the log.

Stages:
1. In-process with pytest. Fast, no infra.
2. Same tests with fake nodes in Podman containers (Milestone 0).
3. Swap in the real node. The tests shouldn't need to change.

## Draft layout

```
cluster/
  scheduler/    Node protocol, Task/Result/NodeStatus shapes, pick(), submit() + fallback
  workplace/    real node runtime: loads models, runs llama-server (later)
  nodewatch/    Rust crate (Sahaanaa)
  infra/        Podman, node.toml, networking
tests/
  fake_nodes.py    FakeNode + test cluster config
  test_cluster.py  the scenarios above
```

main.py becomes the glue: `decision = router.decide(q)`, map the route to a model, then `cluster.submit(task)`.

## Open questions

- Is talk the right default local route?
- Task, Result and NodeStatus shapes cross component boundaries, so they need to be agreed with Andrew (Scheduler) and Sahaanaa (NodeWatch) before any code.
- Where does Workplace's "load a model on demand" fit while Workplace has no owner?
