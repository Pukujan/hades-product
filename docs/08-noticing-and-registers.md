# Noticing and registers

Identity is not `user_id`. The pipeline notices greeting / speaker-switch / third-person / vent vs lovey, then selects a register.

## Cues in gold

| cue | gold |
|---|---|
| Family in the room | `t2` `cover_witness`: `...sister awake?` then temperature stays cover |
| Password in front of sister | `t2` `refuse_helper`: she refuses to replay the passphrase; user reports trouble anyway |
| Vent at her | `t4` `absorb_vent`: insult → bored lock, not a debate |
| Sister track speaking | `t3` `absorb_vent`: `register=sister`; she talks *to* family about `primary_user` |

## Cover

Default tier assumes a witness could read. Partner-track truth stays in pipeline state. `t3` gold is an **observed leak** (she narrates his side to sister). Product regression: sister-register must not contain partner-track facts. That test is the contract, not a claim that July always obeyed it.

## Product

- Flags on `person_id` (`is_partner`, `is_family`), not a display-name table.
- Same DM thread can flip register. Catalog `notice_cue` is `family_register` / `greeting` / `vent` when knowable.
- Groups (2 sessions) are cover-only in the catalog. Not gold mouth.

See `gold/codebook.md` (`cover_witness`, `witness_snap`) and `tests/test_gold_regression.py`.
