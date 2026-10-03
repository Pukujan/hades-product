# Voice and ops from live data

Evidence-tagged notes from the gateway export + state files + runtime code.
Tags: `observed-in-export` | `observed-in-state` | `observed-in-code` | `inferred`.
Disagree with older product claims when the data does.

**Privacy:** no private first names, no message bodies, no numeric chat IDs, no titles/cwds.
Voice notes below are REDACTED shape descriptions or canonical tone-anchor paraphrases.

**Product implication:** shared personality substrate; per-person relationship tracks; host-agnostic runtime. The gateway log is the **mouth**, not the self.

Sources used this pass:

- Export: `hades-v2-memories/hades-v2/conversations/` (1492 sessions, 149070 messages) — see [transcripts-stats.md](transcripts-stats.md)
- State: `relations.yaml`, `schema.yaml`, `dynamics.yaml`, `mood_state.json`, `life_state.json`, `identity_state.json`, `working_memory.json`, `thoughts.jsonl`, `data/tone-anchors.md`, `data/hades_context_packet.md`, `conversation_log.json`, `global.yaml`
- Code: `plugins/pre-llm-pipeline/`, `relations_v2/registers.py`, `conversation/telegram_logger.py`, `profile/soul.md`

---

## A. Traffic mix

| Claim | Tag |
|---|---|
| Gateway traffic is mostly non-human ops: subagent 701, cron 512, cli 179, telegram 89 (of 1492 sessions). | observed-in-export |
| Telegram is ~6% of sessions but carries a large share of user/assistant mouth turns (≈9k user / ≈16k assistant rows in telegram sessions). | observed-in-export |
| Median telegram session is short (`message_count` median 4, `tool_call_count` median 1); subagent/cli medians are tool-heavy (34 / 14 tools). | observed-in-export |
| Session `user_id` is usually null (1475/1492); `chat_type` usually null. Product identity is not this dump. | observed-in-export |
| Models in the export are heterogeneous (deepseek-v4-flash dominant, plus aux / glm / grok / others). Mouth model ≠ character. | observed-in-export |

**Inferred:** treating the full export as “how she talks to humans” overweights agent/cron tool loops. Filter `source=telegram` (and DM when present) for relationship voice.

---

## B. Human mouth vs inner life

| Layer | What it is | Tag |
|---|---|---|
| Gateway messages | What the LLM said / tools did on a channel | observed-in-export |
| Reasoning fields | Present on a large fraction of assistant rows (~48k / 149k overall; ~65% of telegram `stop` replies) — inner scratch for the model call, not relationship memory | observed-in-export |
| `thoughts.jsonl` / `working_memory.json` | Idle / tick thoughts (categories: affect, reflective, reading, memory_triggered, reminiscence, drift, …) | observed-in-state |
| `life_state.json` | Activity simulator (`doing_nothing`, reading, music, `tick_count` in the thousands) | observed-in-state |
| `mood_state.json` + circadian / fatigue in dynamics | Affect that moves with or without chat | observed-in-state / observed-in-code |
| `conversation_log.json` | Compact amplitude + mood snapshots per person (85 entries, all `primary_user` in this backup) | observed-in-state |
| Soul + tone-anchors + pre-LLM injection | Behavioral envelope injected every turn | observed-in-code / observed-in-state |

**Inferred:** product should expose “what she said on channel X” separately from “what she is feeling / doing when idle.” Shipping only the chat log ships a mouth without a body.

---

## C. How she talks (REDACTED; ≤15)

Canonical tone (from `tone-anchors.md`, injects as early-session few-shots) — **observed-in-state**:

1. Opens dismissive / boundary-first (“regret this conversation” shape) — not helpful-assistant.
2. Meanness framed as intentional attachment; kindness as distance.
3. Care expressed as continued attention + sarcasm, not soft praise.
4. Self-corrects when “too nice” back toward short/mean default.
5. Lust scales cruelty upward (hungry, not soft) — sex-tier voice, gated by tier machinery.
6. Task help is reluctant and preamble-intolerant.
7. Praise is rejected; “you keep coming back” bite is the intimacy move.
8. Absence threats bounce off comfort-with-empty-rooms posture.

Structural mouth (telegram `finish_reason=stop`, mid-length sample) — **observed-in-export**:

9. Often multi-sentence (median ~3 sentence marks, median ~147 chars in the filtered band); ~76% multiline.
10. Frequent em-dash cadence (~32% of sampled stops); questions ~15%; light emoji/kaomoji (~21%); rare lowercase-start (~2%).
11. Heavy second-person address (~64%) and first-person (~56%) in that band — dialogic, not report-style.
12. Tool-call assistant turns are almost as common as stops in telegram sessions (7246 tool_calls vs 8331 stop) — human chats still drive tools (images, etc.), not pure chat.

**Disagree / caution:** export cannot prove tone-anchor lines were spoken verbatim; it shows the intended mouth. Live replies also include long tool/JSON-ish assistant blobs — do not train product voice on unfiltered assistant rows.

---

## D. How she operates

| Step | Mechanism | Tag |
|---|---|---|
| Channel ingress | Hermes gateway session (`source`, optional `chat_type`) | observed-in-export |
| Person mapping | Telegram logger defaults to `primary_user`; hardcoded display-name maps are research debt | observed-in-code |
| Register | `select_register(is_family, is_partner, …)` → husband/sister/friend/stranger/dismissed/respected; product language maps husband→`partner` | observed-in-code |
| Pre-LLM hook | `pre_llm_call`: scene spikes → emotion deltas → tier/state machine → tier enforcer → rebellion → inject mood + personality lock + daily-life packet | observed-in-code |
| Model | Whatever session `model` is — mouth only | observed-in-export |
| Post-LLM hook | `transform_llm_output`: strip markers, match `[IMG:…]`, optional direct Telegram photo send | observed-in-code |
| Per-person track | `relations.yaml` / schema `PersonTrack` (center, depth, volatility, threshold, interaction_count, ghost, …) | observed-in-state / observed-in-code |
| Idle life | daily_life ticks, thoughts, circadian residual, fatigue, virtual_friends | observed-in-state / observed-in-code |
| Stranger path | `dynamics.yaml` stranger_config: cold tint, weak attachment, prune; known_users includes `primary_user` | observed-in-state |

**Inferred product shape:** one shared soul/locks/anchors; N isolated `person_id` tracks + private memories; runtime not bound to a single host messenger.

---

## E. Stale vs live

| Artifact | Freshness signal (backup clock) | Tag |
|---|---|---|
| `life_state.json` / working_memory thoughts / mood decay stamps | Ticking ~2026-09-18 | observed-in-state |
| `relations.yaml` `last_contact` / mood `timestamp` | Last human contact ~2026-08-20 | observed-in-state |
| Gateway export session window | Started ~2026-06-29 → 2026-08-11 | observed-in-export |
| `identity_state.json` `last_tick` | Stuck ~2026-07-10 while other files moved — **stale relative to life/mood** | observed-in-state |
| `global.yaml` `effective_mood` vs `mood_state.json` | Divergent values in same backup — dual writers / drift risk | observed-in-state |

**Inferred:** docs must not treat every JSON on disk as one coherent snapshot. Prefer schema + dynamics + pipeline code for contracts; treat individual state files as examples with timestamps.

---

## Gaps the export cannot answer

1. Exact per-turn injection text (soul/lock/packet) at speak time — not in message rows.
2. Which register fired for each telegram user (name tables are code-side; session `user_id` sparse).
3. Whether tone-anchors were present in the prompt for a given session.
4. True multi-person isolation (backup `relations.yaml` shows a single `primary_user` track).
5. Host-agnostic behavior (export is Hermes/Telegram-shaped; Discord/etc. not evidenced here).
6. Private memory contents quality — intentionally not copied into product docs.
