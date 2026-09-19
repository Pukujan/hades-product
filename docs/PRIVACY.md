# Privacy rules for this repo

Private first names from the research instance **must never appear** in product documentation, graphs, examples, or commit messages in `hades-product`.

Use only:

| Research meaning | Product language |
|---|---|
| The human who built / lives with the instance | `primary_user` or `person_id` of the account owner |
| Family / sister register | `is_family: true` → register `sister` |
| Exclusive partner register | `is_partner: true` → register `partner` |
| Simulated idle-life friends | `virtual_friend` (fictional cast is fine) |
| Default-tier “someone could be reading” | family register presence / cover constraint — not a named witness |

Hardcoded name tables in the research engine (`registers.py`, recall weight maps, Telegram display-name substring maps) are **research debt**. Product config is flags on `person_id`, not names in source.

Never commit:

- Live passphrases / danger words
- Bot tokens, model keys, R2 keys
- Telegram / Discord numeric IDs
- Private display names
- Raw conversation transcripts
- The 149k dump
- fossil-core as a vendor subtree
- live memories pipeline copy / `hades_emotion` source

Exception: `gold/turns/*.jsonl` holds **full aliased** spoken turns (`primary_user`, `sister`, `[REDACTED]`). No reasoning bodies. Catalog rows have no `content`. Local name maps stay in `tools/alias_map.local.json` (gitignored). Local mouth key lives in gitignored `.env` (see `.env.example`). Never commit `.env`.
