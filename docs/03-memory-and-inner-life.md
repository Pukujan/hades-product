# Memory and inner life

What actually persists. The chat UI is not the store. Cron is not a user.

Shared character substrate (soul, locks, circadian, mood engines) is one. Relationship memories are per `person_id`. Product must not mix tracks.

## Layers

```text
working memory (now)
  -> episodic (experiences, slower recall)
  -> semantic (consolidated patterns)
idle: thoughts.jsonl, dreams, daily-life packet
forgetting: archive by salience, do not hard-delete
```

| Layer | Job | Product rule |
|---|---|---|
| Working | Last thoughts, live mood, current activity, recent turns | Injected every turn. Short TTL. |
| Episodic | Experiences with emotional weight | Per `person_id` when the memory is about a human |
| Semantic | Patterns after consolidation | Shared skills/world vs per-track people-facts must be split |
| Thought log | Idle inner monologue (~10 min) | Not user-visible unless a later proactive rule fires |
| Dreams | 0–4am, fragmented, short TTL | Inner. Do not narrate to the user as a morning recap by default |
| Daily life | Where she is in her own world | Satellite packet around soul. Fiction, not the human’s calendar |
| Virtual friends | Simulated cast | `virtual_friend`. Never an account |
| mem0 / profile MEMORY | External memory provider + profile files | Research dump. Product: structured per-track store, no raw USER.md |

Primary-track memories decay slower than stranger tracks. Emotional intensity resists forgetting. Frequency of recall resists forgetting. Archive ≠ delete.

## Idle loop (cron)

Every ~10 minutes, a separate process:

1. Read mood, relations, silence
2. Tick existential state
3. Daily-life orchestrator (rhythm, reading, virtual friends, empathy, ontology)
4. Pick a thought category
5. Write a short inner thought
6. Maybe promote high-weight thoughts to episodic
7. Small mood writeback
8. Rarely consider a proactive outbound message

It must not block the live turn. Gateway `source=cron` sessions are this loop (or Hermes wrapping it), not Telegram DMs.

Observed export: 512 cron sessions, almost all `cron_complete`, median ~13 messages, models mostly `aux` / `deepseek-v4-flash`. Sampled recent cron turns are tool-heavy inner work with almost no `[IMG:]`. Do not mine cron for partner-mouth voice.

Proactive pings are specified as rare and emotionally significant. Product default: **off** until an account setting allows them.

## What is shared vs per-user

| Shared (code/templates only) | Per `account_id` (one Hades) | Per `person_id` on that account |
|---|---|---|
| Soul, few-shots, anti-assistant, lock | Live mood/fatigue/residual/ITD counters | Register, attachment, last contact |
| Circadian *shape* + fatigue *equations* | Idle thoughts, existential, neural growth | Conversation recall, private episodic |
| Image library / matcher code | Clock = that account’s timezone | Secrets the other tracks must not see |
| | Daily-life fiction for this instance | Partner-track vs sister-track facts |

Account A’s Hades cannot change Account B’s numbers, people, or clock. Same ticker code ≠ same live state.

`sister` never receives partner-track memories. `stranger` gets no private track. `virtual_friend` is not a tenant.

## Research debt (do not ship)

- Hardcoded name maps for recall weights and registers
- Profile `USER.md` / `MEMORY.md` as the source of truth
- One global marriage/secrets file
- Host paths, live API keys, object-store account IDs

Product identity is flags on `person_id`. Product memory is a store keyed by `account_id` + `person_id`.
