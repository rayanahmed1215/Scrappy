Node infrastructure design

NODE [
    node.toml    - defines the node's budget (cpus, memory, disk)
    Podman       - fences the budget so the node can't exceed it
    llama-server - runs inference inside the fence (threads = cpu limit)
    models       - model files on the host, mounted read-only
    NodeWatch    - heartbeat + reports budget and live usage from cgroups
]

API: health, status, submit task (llama-server HTTP for now)

First design: ONE static node on a local machine.
Done when: node starts from node.toml, NodeWatch reports correct limits
and usage, a query runs through llama-server within the limits.