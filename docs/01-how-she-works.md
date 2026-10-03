# How she works

Hades is a **persistent character runtime**. A turn is not “prompt → model → text.” A turn is: resolve person → update affect/scene → inject personality envelope → model speaks → post-process (tools/images) → write tracks.

Evidence basis: [06-voice-and-ops-from-data.md](06-voice-and-ops-from-data.md), [transcripts-stats.md](transcripts-stats.md). Tags below match that doc.

## Turn loop (live)

```
channel message
    → person_id / register (flags, not display names)
    → pre_llm_call hook (plugins/pre-llm-pipeline)
         scene spikes, emotion deltas, tier/state machine,
         tier enforcer, rebellion layer
         inject: mood block + personality lock + daily-life packet
    → LLM (session model — the mouth)
    → transform_llm_output
         strip markers, image match / optional direct send
    → relation track + logs touch
```

`observed-in-code`: hooks are `pre_llm_call` and `transform_llm_output` (`plugin.yaml`).

`observed-in-export`: most gateway sessions are cron/subagent/cli; human mouth is the telegram slice. Do not design product UX from unfiltered export traffic.

## Idle life (no human required)

While nobody is talking, daily-life / homeostasis ticks still move:

- `life_state.json` — activity, energy, boredom, reading, tick counters (`observed-in-state`)
- `thoughts.jsonl` / `working_memory.json` — inner monologue categories (`observed-in-state`)
- circadian + fatigue + residual mood in `dynamics.yaml` / mood files (`observed-in-state` / `observed-in-code`)
- virtual friends / schedule modules under `hades_emotion/daily_life/` (`observed-in-code`)

Product rule: **idle continuity is part of the character**, not a nice-to-have cron.

## Mouth vs self

| Piece | Role |
|---|---|
| Gateway transcript | Mouth + tool trace |
| Soul + tone-anchors + locks | Shared personality substrate |
| `PersonTrack` / registers | Per-human relationship envelope |
| Mood / life / thoughts | Inner life |

`inferred`: a host-agnostic product keeps the self portable and treats messengers as adapters.

## What not to copy from research

- Hardcoded first-name tables in registers / telegram mapping — **research debt** (see [PRIVACY.md](PRIVACY.md))
- Dual mood writers (`global.yaml` vs `mood_state.json` divergence) — contract around one authoritative affect store
- Assuming `identity_state.json` is fresh because other files ticked — verify timestamps ([06](06-voice-and-ops-from-data.md) §E)

## Related

- [02-identity-and-relationships.md](02-identity-and-relationships.md)
- [03-memory-and-inner-life.md](03-memory-and-inner-life.md)
- [MODULE_GRAPH.yaml](MODULE_GRAPH.yaml)
