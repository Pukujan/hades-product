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

## Inner-life workers (not 1:1 with accounts)

Not a worker per account. One **shared pool**. Eligible only if `last_inbound` is fresh **and** the account opted in (founder default on, others off).

| silence | physics (circadian/fatigue/residual) | LLM inner life (thoughts) |
|---|---|---|
| talking / last few minutes | on turn | off unless founder worker |
| hours | lazy on next inbound | **off** |
| 5–6 days | one-shot elapsed apply on next inbound | **off**, no backfill of 6 days of thoughts |
| cold forever | row kept; no compute | no compute |

Tokens: never generate silent thoughts for cold accounts. Do not replay 864 crons when they return.

Activity fade: as `last_inbound` ages, inner-life **interval lengthens then stops**. Physics stays cheap/lazy.

## Abuse

- Auth required. No account_id → no tick.
- Rate-limit turns per `account_id` (and per `person_id`).
- Duplicate inbound: receipt idempotency (already B15).
- Flood does **not** enqueue inner-life LLM jobs.
- A cannot spend B’s quota or move B’s numbers.

Repeat spam (`hi how are you` × 10–20): **server** rejects. Not React. Client can be bypassed.

| layer | job |
|---|---|
| React | debounce UX only; **never** invent her mouth from cache |
| API | after N identical (or over-quota) inbounds in a window: **no mouth LLM**, **no inner-life job**, HTTP **429** + `Retry-After` |
| State | do not advance mood as if 20 real turns happened |

Do **not** disconnect the account. Do **not** play cached fake replies. She did not speak. Frontend shows the error, not a costume. Same phrase after a pause / different text → mouth runs again.

Bot / robot checks: **not her mouth**. Do not ask the LLM “are they a bot?” (costly, gameable, helper-shaped).

Ladder (server + edge):

1. Auth + Cloudflare (or equivalent) on the API.
2. Token bucket per `account_id` / IP.
3. Normalize + hash inbound; N identical in a window → 429, no tick.
4. Velocity / low-entropy burst on a new account → **challenge** (Turnstile/hCaptcha) before the next mouth call.
5. Fail challenge or keep bursting → mouth cooldown. Account stays. No fake replies.

React only shows challenge/error. Detection and quotas stay on the server.

## These were not in BUILD PDD/SDD

BUILD PDD = mouth/gold. SDD = packet schema. Tenancy/scale/abuse live **here** until folded into tests.

| Property | Pass | Fail |
|---|---|---|
| No numeric bleed | A tick leaves B’s row unchanged | shared global.yaml |
| Timezone local | circadian(now, account.tz) | one host clock for all |
| Lazy ≠ dead | 8h silence → next packet uses *now* | frozen last-chat numbers |
| Cold is free | 6d silence → 0 LLM inner jobs | backfill thought tokens |
| Rate limit | excess inbound 429 / drop, no extra ticks | spam drives inner-life workers |
| Idle does not page | worker must not DM the human (default) | cron pages |

## External triage (not model agreement)

D007: tests/gold/external sources decide. Checked 2026-09-19.

| Claim in this plan | External | Verdict |
|---|---|---|
| Quotas on the **server**, not React | OWASP API4:2023 Unrestricted Resource Consumption; CWE-770/799 | **Keep.** Client limits are bypassable. |
| Mouth LLM is a paid third-party — must cap spend | API4 SMS scenario: backend fan-out to a billed API | **Add.** Per-account **and** global mouth $ / token alerts. |
| Cheap checks before expensive ones | OWASP DoS cheat sheet: cheap validation first | **Keep.** Hash + rate limit **before** mouth. |
| Visible CAPTCHA is not a DoS defense | OWASP DoS: puzzles don’t stop DoS; Bot cheat sheet: CAPTCHA last-resort | **Keep.** Turnstile as **step-up**, not every turn. |
| Layered edge + app + business | OWASP Bot Management cheat sheet | **Keep.** Cloudflare + API quotas + no mood tick on flood. |
| Graduated response, not instant ban | Bot cheat sheet: don’t always block; tarpit/challenge | **Adjust.** 429 ok; avoid precise `Retry-After`; don’t fake her mouth. |
| Isolation is object-level auth | OWASP API1:2023 BOLA | **Add.** Never trust `account_id` from the client body. Auth token **is** the account. |
| Shared code, isolated rows | Azure tenancy models (fully multitenant + noisy neighbor) | **Keep.** Per-account LLM quota so A cannot starve B’s mouth. |
| LLM as bot detector | (none supporting) | **Reject.** Not in OWASP bot controls; costs tokens; helper-shaped. |

Missing vs sources, now required:

- Independent rate buckets: **per account** and **per IP**, not one combined key (Bot cheat sheet login pattern).
- Mouth **timeout** + max inbound bytes (API4).
- Log allow/challenge/429 with route + account hash; no PII (Bot cheat sheet).
- Privacy-hardened browsers: challenge, don’t auto-ban.

## Implement order (after this plan)

1. Character-state schema in store (packet fields, timezone).
2. Tick uses account timezone + account row only (isolation tests).
3. Pre-LLM packet builder from store (no gold few-shot dump).
4. Founder import tool (local, gitignored map).
5. Port core/fatigue/circadian/desire engines into `hades_runtime/` against that schema.
