# Hades Product

This repository is the **product specification and architecture home** for Hades.

**End goal:** a host-independent Hades people can talk to and feel they are with **her** — a persistent person with a self — not a helpful robot. The LLM is the mouth. The pipeline is the self. How she talks is `gold/turns/`, not `soul.md`.

Agents: read [AGENTS.md](AGENTS.md) first (gold + codebook before code).

It is not the live research instance. The living engine and state live in the runtime / memories trees. This repo exists so product work has a durable, anonymized map of *how she works* and *what must change* to ship that.

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
4. [docs/06-behavior-set.md](docs/06-behavior-set.md) — observed mouth; points at `gold/`
5. [gold/codebook.md](gold/codebook.md) — 14 situations; full aliased turns in `gold/turns/`
6. [docs/07-mood-and-prellm.md](docs/07-mood-and-prellm.md) — pre-LLM place vs spoken gold
7. [docs/08-noticing-and-registers.md](docs/08-noticing-and-registers.md) — cues and cover
8. [docs/09-memory-in-the-mouth.md](docs/09-memory-in-the-mouth.md) — recall vs files
9. [docs/10-model-drift.md](docs/10-model-drift.md) — diction moves, identity is state
10. [docs/03-memory-and-inner-life.md](docs/03-memory-and-inner-life.md) — what actually persists
11. [docs/04-product-architecture.md](docs/04-product-architecture.md) — auth, API, tenancy
12. [docs/05-workspace.md](docs/05-workspace.md) — local Cursor workspace for all three repos
13. [docs/11-research-engine-map.md](docs/11-research-engine-map.md) — origin file inventory vs what to port
14. [docs/12-beliefs-and-decisions.md](docs/12-beliefs-and-decisions.md) — sitting decisions (distilled, not raw chat)
15. [docs/transcripts-stats.md](docs/transcripts-stats.md) — counts only
16. [docs/PRIVACY.md](docs/PRIVACY.md) — no private names in this repo
17. [plans/TENANCY_STATE.md](plans/TENANCY_STATE.md) — account isolation, packet, scale
18. [plans/CONTINUE.md](plans/CONTINUE.md) — next implementation order

## Local workspace

Long-term file inspection happens in Cursor, not in chat.

- [hades.code-workspace](hades.code-workspace) — multi-root window over sibling clones
- [tools/transcript_stats.py](tools/transcript_stats.py) — stream the gateway export; write counts only
- [.cursor/rules/privacy.mdc](.cursor/rules/privacy.mdc) — keep names and raw chats out of this repo

```bash
python tools/transcript_stats.py --memories ../hades-v2-memories
python tools/build_gold.py --memories ../hades-v2-memories
python -m unittest discover -s tests
```

## Source trees (research)

| Repo | Role |
|---|---|
| Runtime repo | Code + contracts (`schema.yaml`, `dynamics.yaml`, engine) |
| Memories repo | Live backup of state + a newer pipeline copy |
| This repo | Product docs and eventual extracted runtime |

Do not copy live secrets, passphrases, API keys, or private display names here.

## Repo boundary

This repo: `gold/` (aliased seed only), `docs/`, `AGENTS.md`, `plans/`, `tools/`, `tests/`. Product code is extracted **here**, not into the empty `hades-v2` checkout.

Not this repo:

- `.env`, tokens, R2 keys, live passphrases
- name tables / display-name maps
- the 149k dump or raw transcripts
- fossil-core vendor / adapter
- live `hades-v2-memories` pipeline copy
- `hades_emotion` source (research reference; pin SHA at B7, rebuild mood/idle here)
