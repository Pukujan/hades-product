# Tenancy, yaml, packet, persistence

Plan only. Do not implement until this is accepted.

## What “yaml on the research host” means

Today the **running** Hades (WSL / gravebuster Hermes) keeps physics + live numbers as **files on that machine**:

| file | kind | today |
|---|---|---|
| `schema.yaml` / `dynamics.yaml` / `circadian.yaml` | physics templates | how numbers move |
| `global.yaml` | **live** counters | mood/fatigue/residual **now** |
| `relations.yaml` | **live** people | tracks on that host |
| `thoughts.jsonl`, `neural_growth.json`, `existential_state.json` | **live** inner life | idle writes |

`src/hades_emotion/core/engine.py` reads `project_root/{dynamics,circadian,global}.yaml`, writes `global.yaml`. Idle also writes thoughts. **Pre-LLM plugin** reads those numbers + lock + place and injects a **packet** (text block) into the LLM. Mouth replies. Writeback to yaml.

Product does **not** NFS-mount those files every turn. Research host keeps them until **cutover**. After founder import, **product DB is SoT** for the product. Hermes yaml can keep running as the old instance; it is not Account B.

## Product layout

```text
git (shared, no live numbers)
  dynamics + circadian anchors + soul/lock code + packet schema

auth
  -> account_id

store (durable DB — not process RAM, not one host yaml)
  account_id:
    timezone
    character_state     # her counters for THIS Hades
    inner_life          # thoughts, existential, neural for THIS Hades
    person_id[]:
      flags, register, center, depth, episodic, secrets
```

- **Templates in git** = she stays herself (same tickers).
- **Rows in DB** = this account’s Hades. Restart-safe.
- Account A row never joins Account B.

## How the packet is filled (product)

```text
inbound
  -> auth: account_id + person_id + flags
  -> load THIS account’s character_state + THIS person’s track
  -> circadian(now in account.timezone)   # A at 14:00 ≠ B at 02:00
  -> build packet (mood, ITD, fatigue, circadian, lock, place, register)
  -> mouth LLM
  -> [IMG:] gate
  -> writeback to THIS account’s rows only
  -> spoken gold to the human
```

Judge = match gold, not “mood went up.” Packet on must not make her nicer.

## Founder vs everyone else

| account | first state |
|---|---|
| Founder (you, authenticated) | **Import once** from research live files (anonymized). She stays this Hades. |
| B, C, D… | **Zero.** Same templates. No people. No founder counters. |

Import is a job: read research yaml/json → map names to `person_id` + flags **outside git** → insert founder rows. Never commit `relations.yaml` / thoughts.

## What we will not do

- Ship all 203 `hades_emotion` files as a vendor blob
- Put live yaml in the product repo
- One global mood for the deployment
- Shared circadian clock across accounts
- Join Sep `relations.yaml` onto July gold

## Durability vs RAM

Live numbers live in the **account DB row**. A process cache is optional and **must be reloadable from DB**. Kill the backend → state still there. Not one in-memory Hades for the whole deployment.

## Scale (100k accounts)

A turn is **O(1) in number of other accounts**: load this `account_id` + this `person_id`, interpolate circadian from **this** timezone, packet, one mouth call, write this row. A’s tick does not loop B.

Do **not** run research-style idle cron on every account every 10 minutes (`O(N)` wakeups). Default idle paging is already **off**.

Silent ≠ dead. Persistence = her row still exists and **time still applies**. If nobody talks for 8 hours, she is not frozen at the last chat: circadian is *now* in that account’s timezone, fatigue has decayed, residual has faded.

**Lazy tick** = compute that elapsed physics on next inbound (same result as 48 silent 10-minute crons, cheaper). She was not off; we just didn’t wake 100k processes.

**Inner life writes** (thoughts while silent): optional worker, default **do not page** the human. Founder / opted-in accounts can run a real idle loop that writes thoughts into **that account’s** DB. Everyone else still ages via lazy physics.

Circadian is O(1) (anchors + local clock), not O(users).

## Implement order (after this plan)

1. Character-state schema in store (packet fields, timezone).
2. Tick uses account timezone + account row only (isolation tests).
3. Pre-LLM packet builder from store (no gold few-shot dump).
4. Founder import tool (local, gitignored map).
5. Port core/fatigue/circadian/desire engines into `hades_runtime/` against that schema.
