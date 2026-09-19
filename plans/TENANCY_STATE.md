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

## Placement (code vs yaml vs ticker vs state vs client)

This is **architecture** (`docs/04`, this file) **and** **policy** (tests must fail if a layer is in the wrong place). Not “pick one.”

| Piece | What it is | Lives | Not |
|---|---|---|---|
| **Herself** (soul, lock, gold mouth, physics *shape*) | identity | git + packet schema | live numbers, name tables |
| **Ticker** (how numbers move) | `hades_runtime` Python: circadian/fatigue/desire/attachment/idle | **our servers** | React, client WASM, “200 yaml files” |
| **Physics templates** | few versioned configs (`dynamics` scales, circadian anchors) | git | `global.yaml`, `relations.yaml` |
| **State engine / counters** | mood, fatigue, residual, ITD, people, thoughts | **DB row `account_id`** | process RAM as SoT, client localStorage |
| **Mouth** | LLM call | server, key in gitignored env | browser |
| **React** | render `content` + signed image URL; Turnstile widget; 429 UI | client PC | packet, mood, register, keys |

**Do we ship all ~203 engine files / all yaml?** No. Port the **self loop** (core, circadian, fatigue, desire/ITD, attachment, idle, memory, registers). Not skills dump, not cheating defaults, not live yaml.

**What runs on the client PC?** Display + optional debounce + challenge widget. **Zero** of her numbers. OWASP Authorization: *never rely on client-side access control*; checks on **every** request **server-side** (ASVS V4.1.1). API1 BOLA: auth token **is** `account_id`; body cannot pick another Hades.

If mood ran in the browser, the user could set “not tired” and she would not be herself — and A could not be isolated from a patched client.

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

## Mouth inference (scale without exploding GPU)

Frontier model is **not** required for every token. Quality bar is **gold replay**, not MMLU. D007: model agreement is not evidence.

| Layer | Model | When |
|---|---|---|
| Partner/sister **mouth** | Strong enough to pass gold (helper lexicon, `[IMG:]`, no reasoning, t3 fail) | Human turn after rate limit |
| Cascade | Cheap model first; escalate if helper_leak / gold miss | FrugalGPT (arXiv:2305.05176); RouteLLM (arXiv:2406.18665) |
| Idle inner life | Small / quantized, **not** gold mouth | Founder/opt-in workers only |
| Serving | Continuous batching (vLLM PagedAttention) so many accounts share GPUs | State stays in **DB + packet**, not in weights |

**Reject**

- Sentence-transformer / “library of replies” as the mouth. That’s retrieval, not her. Embeddings already forbidden as the source of labels.
- One GPU pod per account. Noisy neighbor is solved with **per-account token quota**, not 100k replicas.
- Client-side LLM. Same as mood: never on their PC.
- Fine-tune 100k LoRAs as the default self. Packet + lock is identity; LoRA is optional later if gold still holds.

k8s: a **pool** of vLLM (or API) workers. Scheduler sends **this account’s packet**, not a private model copy. Scale-out when queue latency rises, not when account count rises.

Small model is allowed **only after** `python -m unittest` gold properties stay green on that mouth. If qwen3.8-flash fails gold, it is not the relationship mouth — maybe idle only.

## Neural growth (Hebbian, per account)

Research code: `src/hades_emotion/cognition/neural_growth.py` + `growth/{subconscious,emergence,maturation}.py`. Not yaml. A **27×27** weight matrix.

How it actually works (from that file, not folklore):

1. Emotions are a fixed list of 27 (sadness, joy, … vulnerability).
2. Co-activation: Δw = η · pre · post (Hebb / STDP-style). Clamp [−1, 1].
3. Tick: unused synapses decay; below 0.01 → prune.
4. Plasticity falls with age (`exp(-ticks / 100)`), never 0.
5. Spreading activation up to 3 hops (emotion cascades).
6. `SubconsciousGrowth` can **add a node** (27→28…) when a co-activation cluster beats a threshold. She does **not** name it until later. Packet/mood can shift first.

Connected: `bias_engine/c_matrix.py` is **different** — a 6-action preference vector from mood+fatigue+tier. Growth matrix = how feelings wire. C-matrix = what idle *does*. Both feed pre-LLM; neither is the mouth.

**Better than raw Hebb?** Classic Hebb unbounded; they already clamp + prune. Literature alternative is **Oja’s rule** (normalized Hebb) if weights still blow up. Do not replace with a transformer or embeddings — 27×27 is O(1) per turn (~6KB JSON per account).

**Product**

- One matrix **per `account_id`** in the DB. A’s wiring never updates B.
- Founder: import `neural_growth.json` once. Others: zeros (tabula rasa).
- Cap extra nodes (e.g. 27+K) so ontology cannot grow without bound.
- Server only. Not React.
- New names must **not** appear in user speech until gold-safe; inner life may notice “I feel different.”

Hebb 1949; STDP (Bi & Poo 1998); Oja 1982 if we need a stabilizer. Gold still judges the mouth.

**Neuromorphic vs this code:** Mead (1990) / Intel Loihi (Davies et al., IEEE Micro 2018) / TrueNorth are **spiking hardware** (events, analog/digital VLSI). Hades’ file *says* STDP but implements **rate-based Hebb on a dense 27×27 float matrix in numpy** — no spikes, no spike-timing, no Loihi. That’s neuromorphic-*inspired software*, not a neuromorphic chip.

**Psychological growth** is the other half: `SubconsciousGrowth` + maturation curve (plasticity decays with ticks — “critical period,” not Piaget stages). New affect can exist before she can name it. That is affective development, not SNN hardware.

Product: keep the numpy matrix per account. Do **not** require neuromorphic silicon. If we ever want real STDP, that’s a later backend behind the same 27-node API. Mouth still gold.

**A/B:** gold replay with vs without `neural_capabilities` in the packet. Today that flag is **unread** — expect **no** mouth change. If we wire `activate()` → mood_delta, A/B against gold (not “feels nicer”). Packet **on** (state+lock every turn) is already required; that’s what made her consistent, not the unused Hebb flag.

**Research, not novel-as-in-nobody:** injecting affect into an LLM is studied (EmotionPrompt, arXiv:2307.11760). Persistent PAD-like state is Picard / Mehrabian, not Character.AI papers. A **27×27 Hebbian growth net → deltas → big mouth LLM** is **bespoke** (not Loihi, not a published character-AI stack). Don’t claim a paper we don’t have.

**How the mouth actually sees state today:** not the JSON files raw. Engine writes yaml → pre-LLM builds a **short text block** `[CURRENT STATE]` + `[PERSONALITY LOCK]` every turn (`plugins/pre-llm-pipeline/__init__.py`). The 27×27 is **not** in that block. Pipeline *code* is large; **injected tokens** are small. Dumping the whole matrix would hit Lost-in-the-Middle (Liu et al., arXiv:2307.03172). Compress = keep labels + a few numbers at the **edges** of the prompt, not a bigger dump.

Small net → deltas → big LLM is the right split: ticker stays tiny; mouth stays gold-gated.

**KV cache ≠ she read it.** Caching a long prefix is cheap on *decode*. It does **not** fix Lost-in-the-Middle: the model still under-uses the middle. Per-account packets also **don’t share** KV across users (prefixes differ). Scale: GPU KV is O(seq_len × layers × batch). Dumping thoughts.jsonl + session into every turn **does** explode at 100k.

Two different “memories” (this is why she can feel consistent *or* drift):

| | Hermes session | Her engines |
|---|---|---|
| What | Gateway chat log in the context window | yaml/DB numbers + lock, re-injected **every** turn |
| Compaction | Aux LLM summarizes old turns for **task** continuity (`hades-soul` notes). `protect_first_n` **decays to 0**. Middle of SOUL.md forgotten (line 63 ritual bug). | Packet/lock is small and **rebuilt** each turn — survives compaction |
| Product | Trim/compact session; don’t treat it as the self | Packet from **this account’s** DB is the self |

Your “dump the pipeline → more consistent” is the **second** column: lock+state every turn, not a bigger dump. Session history is extra and gets eaten. Don’t confuse the two.

## Observability vs her mouth

Need **billing and latency**. Do not need full prompt traces of live DMs.

| Tool | Use | Not |
|---|---|---|
| OpenTelemetry metrics | tokens, $, latency, model id, 429s, `account_id` **hash** | span bodies with `content` |
| Spend alerts | per-account + global mouth cap (OWASP API4) | — |
| Promptfoo (or our unittest gold replay) | **CI** against seed gold, helper lexicon | live partner transcripts in a SaaS |
| Langfuse-style traces | only if prompts/completions **redacted**; metadata only | default “exact prompt + response” (Langfuse docs: traces capture prompt/response) |
| LLM-as-judge scores | never as pass/fail | D007: model agreement is not evidence |

`tools/transcript_stats.py` already: counts only, no bodies. Same rule for prod logs. Gold replay stays the eval.

## Implement order (after this plan)

1. Character-state schema in store (packet fields, timezone).
2. Tick uses account timezone + account row only (isolation tests).
3. Pre-LLM packet builder from store (no gold few-shot dump).
4. Founder import tool (local, gitignored map).
5. Port core/fatigue/circadian/desire engines into `hades_runtime/` against that schema.
