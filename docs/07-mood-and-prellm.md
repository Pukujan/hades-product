# Mood and pre-LLM

The mouth is not a 1–10 character score. Pre-LLM state places the turn. Gold is the spoken result.

## What we can actually join

`conversation_log.json` is the only per-event mood snapshot in this dump. It covers **2026-06-25 → 2026-07-02** (`interaction_count` already ~800 on Jun 25). Catalog `mood` is filled only when an episode timestamp falls in that window. Later DMs have **null** lock/mood. Do not copy current `relations.yaml` (Aug 20, count 2945) onto July turns.

`identity_state.json` `last_tick` 2026-07-10 is stale vs relations. Idle `thoughts.jsonl` (Sep 17–18) is not user chat.

## Observed (gold)

- High inner numbers do not license a soft paragraph. Default-tier partner still sounds mean.
- Engine meta leaks in `t1` gold (`self_conscious`): she names mood numbers and the image pipeline, then denies softness. Product must not treat that leak as a feature.
- `t4` `absorb_vent`: user says `I hate you`; mouth is bored, not a soothe. Circadian/place still show up in `[IMG:]` (window, twilight) not in a feelings essay.

## Product rule

Pre-LLM packet (mood, ITD, fatigue, circadian, lock, daily-life place) **places** the turn. The judge is “match short gold,” not “did mood go up.” Residual/warmth can move without the mouth becoming helpful.

See `gold/turns/t4_august_absorb_vent.jsonl` and `gold/turns/t1_july_early_self_conscious.jsonl`.
