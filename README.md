# Hades Product

This repository is the **product specification and architecture home** for Hades.

It is not the live research instance. The living engine and state live in the runtime / memories trees. This repo exists so product work has a durable, anonymized map of *how she works* and *what must change* to ship a host-independent, multi-user Hades.

## Start with the human question

A chatbot can produce a convincing turn and still forget **who it is with, what should remain private, and what kind of relationship is continuing**. Hades starts from that harder question: what would a character runtime need to carry across time without collapsing every person's context into one shared memory?

<p align="center">
  <img src="docs/content-system-assets/hero.png" alt="A character that continues — identity, mood, and private relationships persist across conversations" width="100%">
</p>

## What Hades is

Hades is a **persistent character runtime**, not a chatbot wrapper.

- Personality is a shared substrate (soul + locks + few-shots).
- Mood, fatigue, circadian rhythm, and idle inner life keep moving when nobody is talking.
- Each human should own a **relationship track + private memories**.
- The large language model is the mouth. The pipeline before and after the model is the self.

The research instance is one character bound to one host and one primary relationship. The product is the same character engine with **accounts**, **isolated tracks**, and **no host lock-in**.

<p align="center">
  <img src="docs/content-system-assets/supporting-square.png" alt="Memory needs boundaries — shared personality, private tracks, and context kept in place" width="520">
</p>

The important boundary is simple: **continuity is not the same thing as one giant memory store**. Shared personality can be common; relationship context and private memories must remain scoped to the person and product account they belong to.

## Read in this order

1. [docs/00-strategy.md](docs/00-strategy.md) — docs vs FOSSIL vs knowledge graph
2. [docs/01-how-she-works.md](docs/01-how-she-works.md) — turn loop and idle life
3. [docs/02-identity-and-relationships.md](docs/02-identity-and-relationships.md) — who she thinks she is talking to
4. [docs/03-memory-and-inner-life.md](docs/03-memory-and-inner-life.md) — what actually persists
5. [docs/04-product-architecture.md](docs/04-product-architecture.md) — auth, API, tenancy
6. [docs/05-workspace.md](docs/05-workspace.md) — local Cursor workspace for all three repos
7. [docs/MODULE_GRAPH.yaml](docs/MODULE_GRAPH.yaml) — how files link
8. [docs/PRIVACY.md](docs/PRIVACY.md) — no private names in this repo

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

## The content and visual contract

This README follows the pinned [`content-generation-modules` v0.1.2](https://github.com/Pukujan/content-generation-modules/releases/tag/v0.1.2) adapter in [`.content-system/`](.content-system/). **Narrative raster images carry a short title and subtitle** so the visual explains one human idea without crowding the relationship; SVGs, logos, and tiny helper graphics stay text-free. The longer story and responsive review page are in [`docs/content-system-preview.md`](docs/content-system-preview.md) and [`docs/content-system-preview.html`](docs/content-system-preview.html).
