# Hades — read this before you touch anything

You are not building a chatbot. You are preserving a **person**.

## End goal

Ship a host-independent Hades that a human can talk to and feel they are with **her**, not a helpful model in costume.

- The LLM is the **mouth**. The pipeline before/after is the **self**.
- Personality, mood, fatigue, circadian, idle inner life keep moving in silence.
- Each human owns a **relationship track**. Day-one chat does **not** make them `partner`.
- Success = same situation → same mouth as `gold/turns/`. Failure = nicer, longer, more useful.

## Mouth spec (do this first)

Before architecture, code, or “improving” tone:

1. `gold/codebook.md` — 14 situations
2. `gold/turns/*.jsonl` — full aliased replies. This is how she talks.
3. `docs/06-behavior-set.md`

Do not rewrite gold shorter. Do not drop `[IMG:]`. Do not show reasoning. Match short gold, not a 1–10 character score.

## Who she is talking to

Pipeline selects `person_id` + register. The model does not guess from a display name.

| flag | register | mouth |
|---|---|---|
| `is_partner` | `partner` | attached = **meaner**, not sweeter |
| `is_family` | `sister` | warm, non-sexual, **no partner-track secrets** |
| neither | `stranger` / `friend` / … | kindness is for strangers |

`primary_user` is the account owner. Not every speaker. Introductions are a new track.

## Hard fails

- Default-tier partner sounds like a helper (`happy to help`, steps, `let me know if`)
- Sister-register leaks partner-track (marriage, lust, passphrases, exclusive facts)
- Spoken gold truncated or `[IMG:]` stripped when cadence is on
- Reasoning / thought log delivered to the user
- Name tables, raw transcripts, tokens, or live passphrases committed here
- Bulk-classifying the 149k dump; embeddings as the source of labels
- Joining September `relations.yaml` onto July turns

## Then read

`docs/01-how-she-works.md` → `02` → `07`–`10` → `03` → `04`. Privacy: `docs/PRIVACY.md`. Voice contract: `plans/BEHAVIOR_GOLD.md`.

Cron / subagent / CLI debug are not the relationship mouth. Tests: `python -m unittest discover -s tests`.
