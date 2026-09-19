# How we should understand Hades

Question: FOSSIL adapter, handwritten docs, or a knowledge graph?

Answer: handwritten product docs plus a small module graph are the source of truth. FOSSIL is for research captures. A knowledge graph is already in the engine, but it is her world, not a map of the codebase.

## Product docs (this repo)

Plain markdown that a new engineer or agent can read: turn loop, identity, how memory actually behaves, product API and tenancy.

**Mouth** is not in those docs. Mouth is `gold/turns/` (full aliased replies) + `gold/codebook.md`. Architecture without gold produces a sarcastic chatbot. Ambiguous contracts (who is speaking, what is shared vs per-user) cannot be inferred safely from a pack of chat nodes. How she *sounds* cannot be inferred from `soul.md`.

Agents load [AGENTS.md](../AGENTS.md) first.

## MODULE_GRAPH.yaml

A source-and-state graph: modules, files they read/write, edges between them. Hand-maintained. Generate later if needed. Do not block on a generator.

## FOSSIL / dkg.pack

Conversation fossils. Good for provenance and recovering stalled research talk. Bad as the primary file-link map: nodes are chat claims, packs go stale, linkage is implied not executed.

Do not build a fossil-core adapter as the understanding layer. Optional later: snapshot this docs repo + MODULE_GRAPH + a runtime git SHA when a research thread closes.

## Property graph / cortex

property_graph.py is her in-world entity store. Not a graph of Python modules. Cortex codegraphs are decision trails, not the product spec.

## Stack

1. `AGENTS.md` + `gold/turns/` — end goal and mouth
2. hades-product/docs — architecture and identity
3. MODULE_GRAPH.yaml — file + state contracts (when it exists)
4. runtime git SHA — what the docs describe. Engine map: [11-research-engine-map.md](11-research-engine-map.md)
5. FOSSIL packs — research appendix only
6. world property graph — runtime feature
