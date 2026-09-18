# Hades Product

This repository is the **product specification and architecture home** for Hades.

It is not the live research instance. The living engine and state live in the runtime / memories trees. This repo exists so product work has a durable, anonymized map of *how she works* and *what must change* to ship a host-independent, multi-user Hades.

## What Hades is

Hades is a **persistent character runtime**, not a chatbot wrapper.

- Personality is a shared substrate (soul + locks + few-shots).
- Mood, fatigue, circadian rhythm, and idle inner life keep moving when nobody is talking.
- Each human should own a **relationship track + private memories**.
- The large language model is the mouth. The pipeline before and after the model is the self.

The research instance is one character bound to one host and one primary relationship. The product is the same character engine with **accounts**, **isolated tracks**, and **no host lock-in**.

## Read in this order

1. [docs/00-strategy.md](docs/00-strategy.md) — docs vs FOSSIL vs knowledge graph
2. [docs/01-how-she-works.md](docs/01-how-she-works.md) — turn loop and idle life
3. [docs/02-identity-and-relationships.md](docs/02-identity-and-relationships.md) — who she thinks she is talking to
4. [docs/03-memory-and-inner-life.md](docs/03-memory-and-inner-life.md) — what actually persists
5. [docs/06-voice-and-ops-from-data.md](docs/06-voice-and-ops-from-data.md) — **live export + state evidence** (traffic, voice, ops, stale vs live)
6. [docs/transcripts-stats.md](docs/transcripts-stats.md) — anonymized gateway counts
7. [docs/transcripts-schema.md](docs/transcripts-schema.md) — export field names only
8. [docs/05-workspace.md](docs/05-workspace.md) — local Cursor workspace for all three repos
9. [docs/MODULE_GRAPH.yaml](docs/MODULE_GRAPH.yaml) — how files link
10. [docs/PRIVACY.md](docs/PRIVACY.md) — no private names in this repo

`docs/04-product-architecture.md` (auth / API / tenancy) is not written yet.

## Local workspace

Long-term file inspection happens in Cursor, not in chat.

- [hades.code-workspace](hades.code-workspace) — multi-root window over sibling clones
- [tools/transcript_stats.py](tools/transcript_stats.py) — stream the gateway export; write counts only
- [.cursor/rules/privacy.mdc](.cursor/rules/privacy.mdc) — keep names and raw chats out of this repo

```bash
python3 tools/transcript_stats.py --memories ../hades-v2-memories --out docs/transcripts-stats.md
```

## Source trees (research)

| Repo | Role |
|---|---|
| Runtime repo | Code + contracts (`schema.yaml`, `dynamics.yaml`, engine) |
| Memories repo | Live backup of state + a newer pipeline copy |
| This repo | Product docs and eventual extracted runtime |

Do not copy live secrets, passphrases, API keys, or private display names here.
