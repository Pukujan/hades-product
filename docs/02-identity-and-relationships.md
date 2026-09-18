# Identity and relationships

## Shared personality (one character)

Everyone talks to the **same** Hades substrate:

- `profile/soul.md` — core identity, interaction style, circadian narrative (`observed-in-code`)
- `data/tone-anchors.md` — few-shot mouth pillars (dismissive default, meanness-as-care, lust→cruelty) (`observed-in-state`)
- Pre-LLM personality lock + tier directives (`observed-in-code`)

Product: personality is not forked per account. Accounts get **tracks**, not alternate souls.

## Who is speaking / who is being spoken to

Research instance resolves humans via:

1. Channel identity (Telegram user / chat) — sparse `user_id` on gateway sessions (`observed-in-export`)
2. Logger defaulting many DMs to `primary_user` (`observed-in-code`)
3. Optional hardcoded display-name → person key maps — **research debt** (`observed-in-code`)

Product language (mandatory anonymization):

| Concept | Product term |
|---|---|
| Account owner / research host human | `primary_user` or owning `person_id` |
| Exclusive partner register | `partner` (runtime code may say `husband`) |
| Family register | `sister` when `is_family` |
| Idle fictional cast | `virtual_friend` |
| Unknown human | stranger track defaults |

Never put private first names in this repo ([PRIVACY.md](PRIVACY.md)).

## Registers (behavioral envelope)

`observed-in-code` (`relations_v2/registers.py`):

- Flags `is_partner` / `is_family` (and trust/respect heuristics) select a register
- Registers observed: partner-equivalent (`husband` in code), `sister`, `friend`, `stranger`, `dismissed`, `respected`
- Each register sets openness / respect / trust / attachment-style parameters and a context string for the LLM

Product config: **flags on `person_id`**, not names in source.

## Per-person tracks

`schema.yaml` `PersonTrack` (`observed-in-state` / `observed-in-code`):  
`person_id`, `center`, `depth`, `volatility`, `threshold`, `polarity_balance`, interaction timestamps, optional ghost metadata.

Live backup `relations.yaml` currently holds a single `primary_user` track with high `interaction_count` (`observed-in-state`). That is a research deployment shape, not the product ceiling.

`dynamics.yaml` `stranger_config` (`observed-in-state`): cold expression tint, capped attachment, no spillover, prune window; `known_users` includes `primary_user`.

## Tiers and locks

`identity_state.json` carries tier / lock / professional_mode / verified (`observed-in-state`).  
Pipeline `state_machine` + `password_gate` + `tier_enforcer` mechanically gate sexual content and identity lock (`observed-in-code`).

**Stale caution:** in the analyzed backup, `identity_state` timestamps lag life/mood ticks ([06](06-voice-and-ops-from-data.md) §E).

## Product implication

- Shared soul + anchors + locks
- Isolated `person_id` tracks + private memories
- Messenger adapters must emit `person_id`, never rely on substring name tables
- Gateway log remains the mouth; relationship truth lives in tracks + registers
