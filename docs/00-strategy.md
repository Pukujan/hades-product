# How we should understand Hades

Question: FOSSIL adapter, handwritten docs, or a knowledge graph?

Answer: handwritten product docs plus a small module graph are the source of truth. FOSSIL is for research captures. A knowledge graph is already in the engine, but it is her world, not a map of the codebase.

## Product docs (this repo)

Plain markdown that a new engineer can read: turn loop, identity, how memory actually behaves, product API and tenancy.

This is the right primary artifact. Ambiguous contracts (who is speaking, what is shared vs per-user) cannot be inferred safely from a pack of chat nodes.

## MODULE_GRAPH.yaml

A source-and-state graph: modules, files they read/write, edges between them. Hand-maintained. Generate later if needed. Do not block on a generator.

## FOSSIL / dkg.pack

Conversation fossils. Good for provenance and recovering stalled research talk. Bad as the primary file-link map: nodes are chat claims, packs go stale, linkage is implied not executed.

Do not build a fossil-core adapter as the understanding layer. Optional later: snapshot this docs repo + MODULE_GRAPH + a runtime git SHA when a research thread closes.

## Property graph / cortex

property_graph.py is her in-world entity store. Not a graph of Python modules. Cortex codegraphs are decision trails, not the product spec.

## Stack

1. hades-product/docs - source of truth
2. MODULE_GRAPH.yaml - file + state contracts
3. runtime git SHA - what the docs describe
4. FOSSIL packs - research appendix only
5. world property graph - runtime feature
