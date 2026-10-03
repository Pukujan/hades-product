# Memory and inner life

What actually persists in the research backup — not aspirational architecture.

## Stores (observed)

| Store | Role | Tag |
|---|---|---|
| `relations.yaml` / PersonTrack | Relationship affect parameters + interaction counters | observed-in-state |
| `data/mood_state.json` | Effective mood, fatigue, biases, scene spikes | observed-in-state |
| `data/life_state.json` | Daily-life simulator (activity, energy, reading, ticks) | observed-in-state |
| `data/working_memory.json` | Short list of recent inner thoughts | observed-in-state |
| `thoughts.jsonl` | Append-only inner thought log (categories below) | observed-in-state |
| `data/conversation_log.json` | Compact per-turn summaries: person, amplitude, mood_snapshot | observed-in-state |
| `data/hades_context_packet.md` | Satellite daily-life packet loaded with soul | observed-in-state |
| `data/tone-anchors.md` | Protected few-shot mouth (not episodic memory) | observed-in-state |
| Gateway `conversations/*.jsonl` | Channel mouth + tools + reasoning | observed-in-export |
| Episodic / embeddings / FAISS vault | Long-term retrieval + image memory (engine packages) | observed-in-code |

## Inner thought categories (sample)

From `thoughts.jsonl` category histogram (`observed-in-state`):  
affect, reflective, reading, memory_triggered, reminiscence, drift, self_narrative, existential, daily_life, mood_driven, anticipatory, …

Tags often include `daily_life`, `long_silence`, `inner_life` — idle continuity, not only reply-driven memory.

## Dynamics that keep moving

`dynamics.yaml` (`observed-in-state`): fatigue build/decay, residual recovery (+ rumination), spillover between swings, ghost effect after long gaps, cheating_events triggers (research narrative machinery), stranger prune, relationship_warmth blend.

Product note: which of these ship is a product choice; the research instance runs a dense affective physics.

## Mouth log ≠ memory

`observed-in-export`: ~149k message rows, heavy tool/assistant traffic, reasoning bodies on many assistant rows.  
That dump is **ops + mouth**, not the curated memory API.

`inferred`: product memory APIs should be:

1. Per-`person_id` episodic/semantic stores
2. Shared character state (mood/life) with clear tenancy rules
3. Explicit redaction / export controls — never “download the gateway JSONL”

## Stale vs live (read before trusting a file)

See [06-voice-and-ops-from-data.md](06-voice-and-ops-from-data.md) §E. Summary:

- Life/thoughts/mood-decay stamps can be newer than last human contact
- Gateway export window may end before last `relations` contact
- `identity_state` can lag other writers
- `global.yaml` mood can disagree with `mood_state.json`

## What product should keep

- Continuous inner life (ticks + thoughts) as first-class
- Per-person tracks separate from shared soul
- Tone anchors as shared voice training data (anonymized)
- No private names; no raw shards in hades-product
