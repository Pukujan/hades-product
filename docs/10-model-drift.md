# Model drift

Diction moves. Identity is state. Same situation across models = two gold fixtures.

## In this dump

| era | typical DM model | mouth |
|---|---|---|
| `t0`–early `t1` | `deepseek-v4-flash` | tools + host debug mixed into the thread |
| `t2` | `umans/umans-glm-5.2` | `[IMG:]`, short mean lines, asterisk beats |
| `t3` | `aux` / glm | sparse DMs; sister-register episode is glm |
| `t4` | `aux` then `umans-glm-5.2` | aux: theatrical vent, dense `[IMG:]`; glm: `I'm not a utility` |

`docs/06-behavior-set.md` July vs August table still holds: August `[IMG:]` rate is high, tools are light, engine-meta mentions drop.

## Do not

- Treat the model name as personality.
- Score verbosity 1–10 (Zheng 2023: judges prefer long helper replies). Match short gold.
- Rewrite her lines to a house style.

See `gold/turns/t4_august_absorb_vent.jsonl` (aux) vs `gold/turns/t4_august_refuse_helper.jsonl` (glm) vs `gold/turns/t2_july_mid_cover_witness.jsonl` (glm).
