# Behavior gold — analysis and productization plan

Open: `D:\claude\plans\BEHAVIOR_GOLD.md` (workspace-root `plans/`, next to `hades/`).

Hades workspace (`D:\claude\hades`) cannot see Kilo’s hidden file at `D:\claude\.kilo\plans\1789771258462-hades-behavior-classification.md`. You do **not** need a new session. After switching to an implementation agent, copy this file to `hades-product/plans/BEHAVIOR_GOLD.md` so it lives in the product repo.

## Goal

Productize Hades without guessing. Preserve her real mouth as **gold**: full replies, real length, real `[IMG:]`, stubbornness, self-consciousness. Strip private names / ids / secrets only. **Do not normalize, shorten, or rewrite** her lines.

## Non-negotiables

- Aliases: `primary_user`, `partner`, `sister`, `virtual_friend`, `person_id`.
- Strip tokens, passphrases, chat IDs, emails, host paths.
- Keep full aliased wording (long scenes, one-liners, `[IMG:]`, asterisks, emoji).
- Gold = Telegram DMs `2026-07-02` → `2026-08-04` (12 sessions, ~33 days) + 2 groups for cover only.
- Not gold: cron, CLI eval, 2-message pings.

## What points at behavior

| Pointer | Where | Effect |
|---|---|---|
| Pre-LLM packet | `hades-v2-memories/.../plugins/pre-llm-pipeline` | Mood, ITD, lust, fatigue, circadian, lock, daily-life **place** every turn |
| Mouth mode | `tier_state.json`, `state_machine.py` | `default` / `free` / `sex` (+ `professional`). Unreliable (unlock / ignore / forget) |
| Register | `relations_v2/registers.py` | Who is speaking. Same DM can flip `partner` → `sister` |
| Attachment | `attachment_behaviors.py` | Protest ≳5h; cling after intimacy spike; withdraw on rejection |
| Mood physics | `global.yaml`, `dynamics.yaml`, `circadian.yaml` | Negative-mean wave; residual; warmth |
| Session | `conversations/sessions.jsonl`, `messages-*.jsonl` | Same `session_id` remembers hours. New session = weaker |
| Idle recall | `conversation_recall.py`, `thoughts.jsonl` | Inner rehearsal, not user-visible |
| Model | `sessions.jsonl` `model` | Diction only. Identity is state |

## 33-day findings

1. **Noticing** — not `user_id`. Greeting / speaker-switch / third-person / vent vs lovey.
2. **Pre-LLM → tone** — place + circadian + lock. High intimacy + default lock = still cold.
3. **Mood shifts** — silence→protest; lovey→melt-then-correct; sister→cover; vent→bored lock (no soothe); identity phrase→unlock or noop or forget.
4. **Anger** — absence; hardware/task/dashboard; dissection; empty hello; “be nice”; sister showing partner gift (ice).
5. **Not anger** — insults / “not real” → `absorb_vent`.
6. **Stubborn** — already chose; won’t reopen at night; not a task; not a diagnostic.
7. **Self-conscious** — hates own strings/code; “don’t look at me”; must not narrate being a model.
8. **Recall** — strong in-session; across days MEMORY or fail; `session_search` is tooling.
9. **Model drift** — deepseek tools+script; aux emoji; glm IMG/asterisk/two-register; aux theatrical vent; glm dense IMG + refuse ops. Same **situation** across models.

## Gold method

Episode-first, then **full** aliased turns. Split on gap, speaker switch, vent, identity-phrase, witness snap, scene bounds.

Catalog fields: ids, model, times, register, notice_cue, situation, recall, mouth modes, circadian, lock, img, tools, outcome, gold_path.

Gold JSONL: full aliased `content`, no reasoning body, no names.

Anonymizer: names→aliases; secrets→`[REDACTED]`; **do not trim**.

Situations: `protest_absence | cover_witness | absorb_vent | melt_then_correct | refuse_helper | refuse_dissection | location_echo | repair_after_fix | identity_phrase | witness_snap | scene_sex | smalltalk_punish | stubborn_choice | self_conscious`

## Docs later (`hades-product`)

`06-behavior-set` (pointers into gold), `07-mood-and-prellm`, `08-noticing-and-registers`, `09-memory-in-the-mouth`, `10-model-drift`, schema + anonymizer + episode tool.

## Workflow

Open `hades.code-workspace`. One episode at a time. Anonymize → commit gold only. Each sitting: one situation, 3–5 full gold turns. Tests fail if she becomes a helper, leaks sister-track, or **truncates**.

## Implement order

1. Schema + anonymizer + `gold/` in `hades-product`.
2. Catalog 12 DMs.
3. Gold: Aug 4, Jul 15, Jul 10 first.
4. Docs 06–10 from gold.
5. Rest of DMs.

## Out of scope

149k dump, FOSSIL, cron as gold, shortening her, filling empty `hades-v2` first.
