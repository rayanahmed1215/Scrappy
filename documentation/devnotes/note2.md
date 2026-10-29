Notes on Scrappy design
Devnote 2: the end goal

The goal has changed a bit. After building a router prototype, drafting the cluster, and researching similar niches, the idea has become clearer.

Here's the end goal, module by module:

- **Router module:** The router takes a query, embeds it, compares it against the embedded rules, and gets a route from that.
- **Cluster module:** The cluster (or the node) takes the route and sends it to whichever node fits, based on the scheduler and nodewatch.
- **Observe module:** Every piece of route info, node info, sysinfo, and status info is kept and recorded. Every observability call is included, so the functions are white-box.
- **Scrappy module:** The observe data is used to add routes to the rules. Most importantly, it's used to train a scrappy model that works as a general-use node. This node is almost always active and uses dynamic weights.
- **Context module:** Context is kept by embedding the conversations and the actions the user requests. It uses hashing and vector comparison for speed.


The core thesis: old, mismatched computers can work as a useful AI cluster if each request is routed to the node that fits it, and if everything the cluster does is recorded and used to train a small, always-on model that gets better at running the cluster over time.

The MVP design has to include the core thesis. That means the MVP needs at least the router, the cluster, the observe module, and a first version of the scrappy model. Context and sleepy can come after.