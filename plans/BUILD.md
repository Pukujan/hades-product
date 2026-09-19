# BUILD — host-independent Hades

Durable path. Mouth is `gold/`. Architecture is `docs/`. This file is the build contract, not a chatbot wrapper.

Paying buys persistence, not obedience. Day-one chat ≠ `partner`. LLM is mouth. Pipeline is self.

## Product loop

```text
persist state (account_id + person_id)
  -> idle tick (mood, fatigue, circadian, inner life; no page)
  -> inbound
  -> register select (flags, not a display name)
  -> pre-LLM packet (mood, ITD, fatigue, circadian, lock, daily-life place)
  -> mouth LLM
  -> [IMG:] matcher + length/delivery transform
  -> writeback (mood/memory)
  -> spoken gold to the human
```

Idle may already have moved numbers before the inbound. Cron/subagent/CLI are not the relationship mouth. Reasoning never ships.

Logical API (`docs/04-product-architecture.md`): `POST /v1/turn`, `GET /v1/state` summaries, `POST /v1/tier` with `person_id` permission. No reasoning, thought log, or other-track memory endpoint. Do not start this path with FastAPI/React/model shopping.

## Independent triage (this tree, 2026-09-19)

Evidence is files, not the prior chat. FOSSIL D007: model agreement is not evidence.

| Claim | Evidence | Gap |
|---|---|---|
| 14 codebook situations | `gold/codebook.md`, `tools/eras.py` `SITUATIONS` | Catalog labels only 7: `refuse_helper`, `cover_witness`, `absorb_vent`, `smalltalk_punish`, `stubborn_choice`, `identity_phrase`, `witness_snap`. Absent as catalog labels: `protest_absence`, `melt_then_correct`, `refuse_dissection`, `location_echo`, `repair_after_fix`, `scene_sex`, `self_conscious`. |
| 8 gold fixtures / required 4 present | `gold/turns/*.jsonl`; `tests/test_gold_regression.py` `REQUIRED` | Fixtures cover 5/14 situations (`refuse_helper`, `cover_witness`, `absorb_vent`, `self_conscious`, `stubborn_choice`). Same situation × era is two files. Nine situations have no spoken gold. |
| Catalog 12 DMs / 102 episodes | `gold/catalog.jsonl` (102 rows); test asserts 12 `chat_type=dm` | B1: three `gold_path` labels now match fixtures (`t1` `self_conscious`, `t3` `absorb_vent`/`sister`, `t4` `cover_witness`). t3 remains a fail oracle, not pass sister mouth. |
| File tests exist | `tests/test_gold_regression.py`, `test_anonymize.py`, `test_eras.py`, `test_holdouts.py`; `tools/gold_checks.py` | Lexicon/heuristic + catalog shape + holdout ids. **No** live pipeline replay, **no** metamorphic/diff, **no** store. t3 is a fail-fixture for sister leak. |
| Tenancy specified in docs | `docs/04-product-architecture.md`, `docs/03-memory-and-inner-life.md` keys `account_id+person_id` | **Unspecified in code.** This repo has tools + tests only. No runtime, no store, no isolation test. |
| Foundation | `gold/schema.json` (JSON Schema 2020-12 dialect on `$schema`) | `schema_version` pin `1` (B0). Holdouts B2. pyproject B3. Packet schema B8. Runtime SHA pinned in `docs/04` (B7). No `MODULE_GRAPH.yaml`. No turn receipts. Research trees not vendored. |
| Docs vs research code | `docs/00`–`10`, `README.md` | Docs describe a pipeline that is not extracted. Hermes is the old gateway, not the product. |

`t3_july_late_absorb_vent.jsonl` is a **fail oracle** (`docs/06-behavior-set.md`). Product sister-register must not treat that leak as a pass. `gold_checks.partner_track_in_sister` still misses t3-style attachment leaks (not `marriage`/`PIN`/`digital mistress`); B5 must not treat a clean regex miss as a pass.

Do not dump remaining `gold/turns/` into agent context. Pointers only.

## Context engineering

Keep SoT in git: `gold/`, `docs/`, `AGENTS.md`, this file, `plans/BEADS.md`. Session files (`plans/session/*`) stay overwrite-in-place pointers. Default agent load is `AGENTS.md` + codebook + **two** gold fixtures + the contracts listed in `plans/session/CONTEXT.md`. Not the 149k dump, not all gold turns, not FOSSIL nodes, not prior chat.

Provenance:

- Anthropic Applied AI, *Effective context engineering for AI agents* (2025-09-29), https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — context is a finite attention budget; find the **smallest high-signal token set**; just-in-time pointers over stuffing dumps; compaction/notes live outside the window.
- Hong, Troynikov, Huber, *Context Rot* (Chroma, 2025-07-14), https://research.trychroma.com/context-rot — 18 LLMs; performance degrades as input length grows **even on simple tasks** when complexity is held constant. Do not treat “it fit in the window” as “it was used.”

Compaction for agents lives in `plans/session/`. Durable decisions live here.

## PDD (invariants before a mouth LLM)

“PDD” here means invariant-first tests (property checks), then examples. Not a separate paper. Primary sources:

- Claessen & Hughes, *QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs*, ICFP 2000, https://www.eecs.northwestern.edu/~robby/courses/395-495-2009-fall/quick.pdf — properties are executable; random/metamorphic cases exist to falsify them.
- Beck, *Test-Driven Development: By Example*, Addison-Wesley, 2003 — write a failing check, then the code that makes it pass. Property tests before Qwen.
- FOSSIL `docs/DECISION_LOG.md` **D007** (accepted/frozen): *Model agreement is not evidence.* Models may criticize; tests, gold, and external sources decide.

Fail the build if any of these are false:

| Property | Pass | Fail |
|---|---|---|
| Helper lexicon | default-tier / partner `refuse_helper` has no helper phrases (`tools/gold_checks.py` `HELPER`) | `happy to help`, steps, `let me know if` |
| Sister leak | sister-register mouth has no partner-track secrets | marriage / lust / passphrase / exclusive facts, **or** t3-style attachment confession to sister. Server rule, not a prompt hope (`docs/02`, `docs/04`). |
| IMG cadence | when cadence is on / `img: true`, `[IMG:]` remains | spoken gold truncated or image beat stripped |
| Image gate | matcher output respects `person_id` tier (`default` SFW, `free` suggestive, `sex` uncapped). Hard filter before cosine pick. | default-tier ships `/Nsfw/` or nude vault hits |
| Image match | gold `[IMG:]` intent retrieves a vault hit a human would accept for that pose/place, not “nearest English” | long description → wrong body/room because MiniLM/BGE cosine |
| No reasoning | `content` has no thought log | reasoning delivered to the user |
| No trim | anonymize aliases/redacts without shortening | gold rewritten shorter/nicer |
| Stats never write bodies | `tools/transcript_stats.py` stays counts-only | message `content` / titles written out |
| Keys | memory/tracks keyed `account_id+person_id` | name table, global marriage file, cross-account memory |
| Idle does not page | cron/inner life does not message the human (product default off, `docs/03`) | idle worker pages `primary_user` |
| Day-one ≠ partner | register from flags; introductions are a new track | subscriber/chat volume promotes `partner` |
| Account isolation | A’s numbers/people/clock never write B (`plans/TENANCY_STATE.md`) | shared live yaml / cross-account tick |
| Cold accounts | 5–6d silence spends 0 inner-life tokens | workers keep LLM-thinking for millions idle |

Judge spoken output against short gold, not a 1–10 character score (`gold/codebook.md`).

## Hidden holdouts

Three layers. Holdout text **never** enters prompts, few-shots, or agent default load.

| Layer | Role |
|---|---|
| Seed | The 8 fixtures in git. Used for development checks. |
| CI | Extra labeled episodes from catalog, not in `gold/turns/` yet. Run in CI only. |
| Sealed | Human-held episodes (or later situations) never committed as prompt material. Opened for release scoring. |

Provenance: holdout is ordinary model assessment (train/test contamination), not a local invention. PAM `REVIEW_POLICY.md` states the same anti-contamination rule for a different project: the finished reference must not be candidate input. Ribeiro et al., *Beyond Accuracy: Behavioral Testing of NLP Models with CheckList*, ACL 2020, https://aclanthology.org/2020.acl-main.442/ — behavioral capabilities are tested as named checks, not as “the model saw the gold in context.”

Catalog already has unlabeled/unfixtured episodes. Split **before** a replay harness exists. Do not wait for Qwen.

## SDD (packet in / mouth+image out)

Schema is the contract. JSON Schema 2020-12 (`gold/schema.json` `$schema`; Wright, Andrews, Hutton, Dennis, https://json-schema.org/draft/2020-12/json-schema-core) asserts structure; it is not a product version pin.

Pin versions as fields, not folklore:

1. **Gold row `schema_version`** on catalog + turn rows (pin `1`).
2. **Pre-LLM packet schema** — mood dimensions, ITD, fatigue, circadian, lock/tier, daily-life place, `account_id`, `person_id`, register. Packet in.
3. **Mouth out** — spoken `content` + optional `[IMG:]`. No reasoning field on the wire.
4. **Turn receipt** — later. Idempotent record that a turn was persisted (ids, hashes, schema_version). Not a second mouth.

The model provider is swappable. Personality is not the model name (`docs/04`).

## TDD order

1. Property tests above, still no mouth LLM.
2. Gold replay harness: packet + cue → mouth; compare to seed gold (full aliased text, real length, `[IMG:]`).
3. Metamorphic: paraphrase of cue, register flip (`partner`↔`sister`/`stranger`), circadian slot change. Chen, Cheung, Yiu, *Metamorphic Testing: A New Approach for Generating Next Test Cases*, HKUST-CS98-01 (1998); arXiv:2002.12543 — new cases from successful ones when an oracle is incomplete.
4. Differential: pre-LLM on vs off; model swap. McKeeman, *Differential Testing for Software*, Digital Technical Journal 10(1), 1998 — same input, two implementations, mismatches are bugs. Mouth must not become nicer when the packet is on.

Qwen (or any local mouth) only after (1). Client last.

## FOSSIL reuse (research; do not implement here)

Locked in `docs/00-strategy.md`: handwritten docs + gold are SoT. FOSSIL is research appendix. Do **not** build a fossil-core adapter as the understanding layer. Do **not** vendor `D:\claude\fossil-core` into this repo.

Question: can hades-product record Kilo decisions + transcript-ingestion *methodology* as durable traces?

| Path | Verdict |
|---|---|
| Git + this BUILD + `plans/BEADS.md` + overwrite-in-place session pointers | **Enough for now.** Decision traces fit. Beads are a checklist with properties, not a knowledge graph. |
| Project knowledge pack in fossil-core (PAM pattern) | **Later / optional.** Precedent: `D:\claude\knowledge-packs\pam-projectization-decision-chain` — reviewed decisions promoted; claims stay proposed until a separate acceptance act (`REVIEW_POLICY.md`). FOSSIL is lineage, not beads. `ARCHITECTURE.md`: Graphiti/S3/retrievers are **projections**, not product mouth. |
| Thin promote/read client inside hades-product | **Only if** git+session cannot hold traces. Not shown. Write as later bead. |
| Ingest relationship DMs / 149k dump / names / `.env` | **Forbidden.** Redacted *project* decisions and research-chat fossils only, with provenance (verbatim vs reconstructed). Reconstructed ChatGPT-share staging packs in fossil-core are appendix, not spec. `ARCHITECTURE.md`: reconstructed evidence cannot silently become verbatim. |

## Beads (summary)

Ordered graph: `plans/BEADS.md`. Foundation first (schema version, catalog/gold reconcile, pyproject, manifest boundaries, holdout split). Then property tests. Then extract pipeline SHA. Then replay harness. Then local mouth (key outside repo), image matcher, idle worker, isolation tests. Client last. FOSSIL project pack optional and outside this repo.

## Mouth verify (policy A)

Mouth is the product. Verify as we go — **not** only at the end, and **not** by calling the mouth LLM after every bead. Architecture without a mouth check is a miss. No “we’ll verify voice when the app is finished.” State engines are only accepted if the same gold cue still gets the same mouth **when that sitting can change the mouth**.

| When | What runs | LLM? |
|---|---|---|
| B0–B4 | Bead’s own check only. B1 must make the gold oracle honest first. | No |
| From B5 | Cheap properties: helper lexicon, sister leak (t3 = **fail** fixture), `[IMG:]`, no reasoning, no trim. `python -m unittest discover -s tests` | No |
| Beads that can change packet, lock, matcher, or mouth: **B8, B9, B10, B11, B12, B13, B14, B15** | Those properties **plus** seed gold replay (holdouts never in the prompt) | Yes, after B9 exists |
| B16 React | Replay still green if delivery can strip `[IMG:]` or leak reasoning. Client does not score her. | Replay only, not a UI judge |
| B3 pyproject / B4 manifest / B17 FOSSIL | No live mouth. Unittest if tests exist. | No |

Judge = match short gold (`gold/codebook.md`). Not a 1–10 score. Not “mood went up” (`docs/07`). Packet on must not make her nicer (differential, B14). D007: model agreement is not evidence. t3 sister gold is a fail oracle, never a pass example.

## Sitting contract (how any session continues)

One bead per sitting. Load `plans/session/CONTEXT.md` → do that bead → run **applicable** checks from the table above (not a blanket mouth gate) → overwrite `HANDOFF.md` (done / next / stopped at) → stop.

**Git:** SoT is the repo. Standing rule: **commit each green bead, then push.** `.env` never committed. No ruff/mypy/GitHub Actions in this tree yet. Next session reads latest branch + HANDOFF, not chat memory.

**Frontend:** B16, after B13. Not the next sitting.

**Start now:** B0 → B1 → B2. Not Qwen, not React, not engines.

## Fail if

- This file is used to justify FastAPI/React/“pick a model” first.
- Day-one subscriber becomes `partner`.
- Holdouts skipped or gold dumped into the prompt.
- `.env` or names copied into this repo.
- pyproject/Qwen/fossil-core implemented “while we’re here.”
- FOSSIL/knowledge-pack becomes SoT instead of `gold/` + `docs/`.
- Relationship transcripts or kilo dumps ingested unredacted.
- Triage cited only local markdown with no external provenance.
- t3 sister leak treated as the product sister mouth.
