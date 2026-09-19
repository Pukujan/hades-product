# Beads — ordered graph

Each bead: goal, pack paths, pass/fail property, blocked-by. Implement in order. Do not skip holdouts. Do not start a client.

Authority: `plans/BUILD.md`. Mouth: `gold/`. Architecture: `docs/`.

**Mouth verify:** `plans/BUILD.md` policy A. Cheap properties from B5; seed gold replay only on B8–B15 after B9 exists. t3 = fail fixture. Do not close a mouth-changing bead if gold went helper.

## Foundation

### B0 — gold schema version
- **Goal:** Catalog and turn rows carry `schema_version`. `gold/schema.json` remains the JSON Schema dialect; the field is the product pin.
- **Pack:** `gold/schema.json`, `gold/catalog.jsonl`, `gold/turns/*.jsonl`, `tests/test_gold_regression.py`
- **Pass:** every gold row validates; missing `schema_version` fails CI.
- **Fail:** version only in chat / BUILD prose.
- **Blocked-by:** none.

### B1 — catalog ↔ gold reconcile
- **Goal:** `gold_path`, `situation`, and `register` on catalog rows match the fixture file. Document t3 sister gold as a **negative** example, not a pass oracle.
- **Pack:** `gold/catalog.jsonl`, `gold/turns/`, `docs/06-behavior-set.md`, `tools/gold_checks.py`
- **Pass:** the three known mismatches are fixed or explicitly flagged (`t1_july_early_self_conscious`, `t3_july_late_absorb_vent`, `t4_august_cover_witness`). Sister-leak check runs on sister-register rows.
- **Fail:** catalog still labels `self_conscious` as `cover_witness`; t3 leak treated as product sister mouth.
- **Blocked-by:** B0.

### B2 — holdout split
- **Goal:** Seed / CI / sealed. Sealed never in prompts or default agent load.
- **Pack:** `gold/catalog.jsonl`, `gold/turns/` (seed only), `plans/BUILD.md`, `tests/`
- **Pass:** manifest lists seed vs CI vs sealed ids; CI job cannot read sealed; agent CONTEXT does not include holdout bodies.
- **Fail:** remaining catalog episodes dumped into `gold/turns/` as few-shots; holdout in the mouth prompt.
- **Blocked-by:** B1.

### B3 — pyproject
- **Goal:** Installable test/tool package. No runtime extract.
- **Pack:** `pyproject.toml` (new), `tests/`, `tools/`
- **Pass:** `python -m unittest discover -s tests` via the project env.
- **Fail:** Qwen/FastAPI added in the same bead.
- **Blocked-by:** none (can parallel B0). Must not land a mouth LLM.

### B4 — manifest boundaries
- **Goal:** What lives in this repo vs memories vs runtime. `MODULE_GRAPH.yaml` when it exists is file+state contracts, not FOSSIL.
- **Pack:** `README.md`, `docs/00-strategy.md`, `docs/04-product-architecture.md`, `docs/PRIVACY.md` (new `MODULE_GRAPH.yaml` later)
- **Pass:** written boundary: no `.env`, no name tables, no 149k dump, no fossil-core vendor.
- **Fail:** memories pipeline copied unredacted; fossil-core subtree.
- **Blocked-by:** none.

## Properties (before Qwen)

### B5 — property tests (PDD)
- **Goal:** Executable invariants from `plans/BUILD.md` PDD table. Still no live model.
- **Pack:** `tools/gold_checks.py`, `tests/test_gold_regression.py`, `tests/test_anonymize.py`
- **Pass:** helper lexicon, sister leak (including t3 as fail-fixture), IMG cadence, no reasoning, no trim, stats never write bodies.
- **Fail:** only synthetic helper strings; sister gold untested; reasoning check only `content[:20]`.
- **Blocked-by:** B1.

### B6 — isolation properties (no runtime yet)
- **Goal:** Spec+failing tests for `account_id+person_id` keys, no cross-track memory, idle does not page, day-one ≠ partner.
- **Pack:** `docs/02-identity-and-relationships.md`, `docs/03-memory-and-inner-life.md`, `docs/04-product-architecture.md`, new `tests/test_isolation.py`
- **Pass:** tests fail until a store exists; they encode the properties. Register from flags, not display names.
- **Fail:** tests skipped because “no engine yet”; introductions auto-`partner`.
- **Blocked-by:** B5.

## Pipeline extract

### B7 — extract pipeline SHA
- **Goal:** Pin the research runtime SHA this product describes. Copy nothing secret.
- **Pack:** `docs/04-product-architecture.md`, `docs/01-how-she-works.md`, `docs/07-mood-and-prellm.md`
- **Pass:** SHA recorded; packet fields named; `.env`/tokens/profile markdown stay out.
- **Fail:** unpinned “memories copy”; Hermes treated as product.
- **Blocked-by:** B4, B6.

### B8 — packet schema (SDD)
- **Goal:** Pre-LLM packet in; mouth+`[IMG:]` out; schema_version on the packet. Turn receipt later (B15).
- **Pack:** new schema next to `gold/schema.json` (e.g. `gold/packet.schema.json` or `docs/` contract)
- **Pass:** packet validates; no reasoning field on the output contract.
- **Fail:** OpenAPI/UI first; model name as personality.
- **Blocked-by:** B0, B7.

## Mouth

### B9 — gold replay harness
- **Goal:** Drive seed gold through packet → mouth stub/LLM; compare full aliased text (length, `[IMG:]`).
- **Pack:** `gold/turns/` seed only, `tests/`, `plans/BEHAVIOR_GOLD.md`
- **Pass:** mismatch on helper rewrite / missing `[IMG:]` / trim fails the job. Holdouts not in the prompt.
- **Fail:** gold bodies stuffed into system prompt as the whole mouth; sealed holdout used as few-shot.
- **Blocked-by:** B2, B5, B8.

### B10 — local mouth LLM
- **Goal:** Swappable mouth. Key stays outside the repo.
- **Pack:** runtime extract (B7), env outside git
- **Pass:** provider swap does not change register/tier rules; property tests still gate.
- **Fail:** “pick Qwen” as architecture; keys committed.
- **Blocked-by:** B9.

### B11 — image matcher
- **Goal:** Post-speech `[IMG:]` → gated vault hit → signed URL for React. Not a second chatbot.
- **Pack:** research `image_matcher.py` (extract at B7), gold `img: true` rows, `docs/01-how-she-works.md`
- **Pass:** (1) cadence keeps `[IMG:]` in gold; delivery strips it and returns a URL. (2) Hard gate: `default` SFW, `free` suggestive, `sex` uncapped — filter **before** cosine. (3) Match tests: gold intents must not return a random nearest-English miss; structured tags / same-language index / rerank beat raw MiniLM on long prose.
- **Fail:** cosine-only ONNX as the product; default-tier `/Nsfw/` URL; R2 keys in the client.
- **Blocked-by:** B9, B8.

### B12 — idle worker
- **Goal:** Mood/fatigue/circadian/inner life tick while silent. Default: do not page.
- **Pack:** `docs/03-memory-and-inner-life.md`, `docs/01-how-she-works.md`
- **Pass:** idle mutates state; no user-visible message unless an explicit later account setting.
- **Fail:** cron sessions mined as partner mouth; idle pages `primary_user`.
- **Blocked-by:** B7, B6.

## Hardening

### B13 — isolation tests (live store)
- **Goal:** Two accounts, partner vs sister tracks, no secret leak, no cross-account memory.
- **Pack:** `tests/test_isolation.py`, store keyed `account_id+person_id`
- **Pass:** sister cannot read partner-track facts; stranger gets no private track.
- **Fail:** name map; one global secrets file.
- **Blocked-by:** B6, B8, B12.

### B14 — metamorphic + differential
- **Goal:** Paraphrase, register flip, circadian change; pre-LLM on/off; model swap.
- **Pack:** `tests/`, seed gold (not sealed holdout)
- **Pass:** register flip drops partner secrets; pre-LLM on does not make the mouth nicer; model swap keeps situation mouth.
- **Fail:** judged by “sounds helpful”; 1–10 character score.
- **Blocked-by:** B9, B10.

### B15 — turn receipt
- **Goal:** Idempotent persist receipt (ids, hashes, schema_version). Not a second mouth.
- **Pack:** packet schema, store
- **Pass:** duplicate inbound does not double-write mood/memory.
- **Fail:** receipt endpoint returns reasoning or other-track memory.
- **Blocked-by:** B8, B13.

## Last / optional

### B16 — React client last
- **Goal:** One React consumer of `POST /v1/turn`. Renders spoken `content` plus `<img src={signed_url}>`. Not Telegram.
- **Pack:** `docs/04-product-architecture.md`
- **Pass:** client cannot select `partner` by chatting; cannot fetch reasoning; images are signed URLs, not R2 keys, not `[IMG:]` left on the page.
- **Fail:** React built before B5–B13; Telegram treated as v0.
- **Blocked-by:** B13, B11, B10.

### B17 — FOSSIL project pack (optional, outside this repo)
- **Goal:** Redacted project-decision lineage in fossil-core, PAM pattern. Verbatim vs reconstructed.
- **Pack:** fossil-core knowledge pack (not vendored). Precedent: `pam-projectization-decision-chain`.
- **Pass:** gold/docs remain SoT; pack is appendix; no DMs/149k/names/`.env`.
- **Fail:** adapter becomes understanding layer; reconstructed share treated as gold.
- **Blocked-by:** B4. Not required to ship mouth.

## Graph (blocked-by)

```text
B0 → B1 → B2 → B9
B3 ∥ B0
B4 → B7 → B8 → B9 → B10
                 B9 → B11
B5 → B6 → B7
B5 → B9
B6 → B12 → B13 → B15
B6 → B13
B9 → B14
B10 → B14
B13 + B11 + B10 → B16
B4 → B17 (optional)
```

## Out of scope as beads

Qwen wiring as a first step. Building the React app before B13. Extracting `hades_emotion` into this tree. Reading live keys. Bulk-labeling the 149k dump. Joining September `relations.yaml` to July turns. Vendoring fossil-core. Ingesting DMs or kilo transcripts.
