# SCHEDULER: Master Outline

## Purpose
The *Scheduler*'s essential job is to allocate a certain job (query/prompt) to the most appropriate node. The *Scheduler* lives downstream of the *Router* and their roles are similar, however while the *Router* is meant to be dynamic and trainable, the *Scheduler* is something that behaves statically.

## Specs

### Input
- **nodewatch reports**: Once per heartbeat, each individual nodewatch instance sends a health report to the *Scheduler*. If the *Scheduler* stops recieving these health reports from a certain node, that will be taken to mean that the node has gone down; until that node comes back on line (starts sending health reports again) it will not be considered viable to recieve a task. These *Nodewatch* reports will contain:
    - The overall health of that node (this will include things such as resource usage, uptime, etc.),
    - The curret job occupying that node, and whether or not there is one,
    - The model running on that node and any tools in that node's workspace (at this point, each node is expected to have one model and a static environment, so the scheduler only really needs to hear about this stuff once; however in the future if dyamic workspaces and multi-model nodes are implemented then including this information in every *Nodewatch* report will not be redundant)

- job/route packet from router

### Output

## Architecture