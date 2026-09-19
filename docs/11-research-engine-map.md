# Research engine map

Origin: `github.com/Pukujan/hades-v2` @ `a783d91` (**1618** tracked files). Local clone was empty; engine trees are now checked out under `D:\claude\hades\hades-v2`. This repo does **not** vendor that tree.

Prior product docs covered gold + a few yaml surfaces. They did **not** inventory `src/hades_emotion`. This file does.

## What is the self (port here)

`src/hades_emotion/` — **195** `.py` files. Packages:

| package | job |
|---|---|
| `core` | engine + circadian + relations load |
| `fatigue` | session build / idle decay (max 6) |
| `desire` | lust / ITD gating |
| `attachment` | warmth, absence, protest |
| `decay` | residual / weibull |
| `homeostasis` | mood PID / regulation |
| `emotions` | boredom, self_conscious, vulnerability, … |
| `cognition` | idle loop, thoughts, dreams, existential |
| `memory` | working / episodic / semantic / forgetting |
| `daily_life` | place packet, rhythm (strip host-specific schedule) |
| `relations_v2` | registers (flags, not name tables) |
| `safety` | secrets gate, mood guardrails |
| `personality` | traits / burnout |
| `recall` | idle recall, not user chat |

Packet injector: `plugins/pre-llm-pipeline/` (33 files).

Scales: `dynamics.yaml` / `schema.yaml` (native units, **not** 0–100). Circadian yaml may live only on the memories copy, not origin.

## Not the self (do not port)

| area | n | why |
|---|---|---|
| `skills/` | 665 | Hermes/ops/research paper templates |
| `data/` | 397 | dumps, gallery, job xlsx, live logs |
| `scripts/` | 148 | host ticks, mixed |
| cheating / host schedule / name maps | — | research debt (`docs/03`) |
| live `relations.yaml`, `thoughts.jsonl`, profile markdown | — | instance memory, not product |

## Three copies (do not mix)

| Copy | What it is | Latest? |
|---|---|---|
| `D:\claude\hades\hades-v2` | Git origin @ `a783d91` (2026-07-12). **Code.** `circadian.yaml` is **not** on origin. | Code snapshot, not live |
| `D:\claude\hades\hades-v2-memories` | Backup 2026-09-18. Code **plus** live-ish yaml/jsonl (`thoughts`, `relations`, `global`). | Newest **exported state** |
| WSL Hermes | **What actually runs.** Profile: `/root/.hermes/profiles/hades-v2` (gateway, `state.db`, plugins). Self: `/root/.hermes/projects/emotion-project-host-v2/` (`circadian.yaml`, `dynamics.yaml`, `src/`, idle writes). | **Live instance** |

Wiring (from `src/hades_emotion/core/engine.py`): every tick reads `project_root/{dynamics,circadian,global}.yaml` and writes `global.yaml`. Idle also reads `relations.yaml`, writes `thoughts.jsonl` + `existential_state.json`. Pre-LLM plugin turns those numbers into the packet. Hermes profile is the **mouth host**; `emotion-project-host-v2` is the **self**.

Memories ≠ live. Git ≠ live. Do not join Sep memories `relations.yaml` onto July gold.

## Product rule

Rebuild **core + fatigue + desire + attachment + circadian + idle + memory + registers** in `hades_runtime/`, keyed `account_id+person_id`. Judge mouth by gold. Do not copy live state or `hades_emotion` as a vendor blob.
