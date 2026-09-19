# Product architecture

Research: one character, one host, one primary relationship, Hermes gateway, Telegram/CLI as mouths.

Product: the same engine with **accounts**, **isolated tracks**, and **no host lock-in**.

## Tenancy

```text
deployment
  character runtime (shared soul, locks, mood engines, image matcher)
    account
      person_id  (primary_user of that account)
      relationship tracks[]  (partner / sister / friend / …)
      private memory
      channel bindings (telegram, later others)
```

One deployment may serve many accounts. Each account is a **separate Hades**. Shared is **code/templates only** (soul, lock, circadian *shape*, dynamics *equations*). Not one running wave. Not one `global.yaml`.

Hard isolation:

- Numbers (mood, fatigue, residual, ITD, attachment, ticks) exist **only** on that `account_id`.
- People she meets exist **only** in that account’s store (`person_id` tracks). Account A never sees B’s people.
- Circadian **ticker code** is the same; **clock is the account timezone**. A at 14:00 is not tired because B is at 02:00.
- B pissed does not move A’s mood. Literally no numeric bleed.

Auth → `account_id`. Tracks → `person_id` inside that account only.

## Identity

- Auth yields `account_id` + `person_id`.
- Register is computed from flags (`is_partner`, `is_family`) plus trust/respect/attachment — not from a display-name substring.
- Gateway `user_id` on transcript rows is not identity (usually unset).
- Family cover / secrets gate is a server rule, not a prompt the model is trusted to keep.

## Mouths

| Channel | Role in research | Product |
|---|---|---|
| Telegram DM | Relationship mouth (gold source) | Not v0. Adapter later if ever. |
| React web | none | **v0 client.** Consumes `POST /v1/turn`; renders `content` + signed image URL. |
| Telegram group | Rare (2 sessions in export) | Out of v0 |
| CLI | Host debugging + character | Operator/admin, not the consumer app |
| Cron / subagent | Inner life / workers | Never a user-visible channel |
| Discord / email | Present in research config | Out of v0 unless routed |

API shape (logical, not a shipped OpenAPI yet):

- `POST /v1/turn` — inbound message, `person_id`, channel
- `GET /v1/state` — mood/circadian/tier **summaries**, not raw files, not reasoning
- `POST /v1/tier` — explicit transition with permission on `person_id`
- No endpoint that returns reasoning, thought log, or another track’s memory

## Turn path

Inbound → auth → register select → pre-LLM state block → model → output transform (length, `[IMG:]`, channel formatting) → persist mood/memory → deliver.

The model provider is swappable. Personality is not in the model name.

## Media

Spoken turns may close with `[IMG:]`. Delivery is channel-specific (Telegram markdown image vs CLI URL). Object storage stays behind signed URLs. Do not commit bucket credentials or account IDs in this repo.

## What stays out of v0

- Copying the research host
- Shipping research kink scripts as default personality
- Name tables
- Showing idle thoughts as chat
- Cross-account memory
- Treating FOSSIL / cortex / in-world property graph as the product spec

## Extraction

Runtime code lives in the research tree (currently a pipeline copy under memories; the sibling `hades-v2` checkout here is empty). This repo holds the anonymized contract and is where the product is built. Do not copy `.env`, tokens, live profile markdown, name tables, the 149k dump, fossil-core, or `hades_emotion` source. Mood/idle are rebuilt here.

Pinned research SHAs (B7). These describe the research trees; they are not vendored here.

| Tree | SHA | Role |
|---|---|---|
| `hades-v2` | `a783d91a3ba1e847371e0f3aaef2a65b5cf50507` | runtime this product describes |
| `hades-v2-memories` | `2c62ff1266c5047cd9d26a6cb306f9f6022fbddf` | export/backup only, not product |
