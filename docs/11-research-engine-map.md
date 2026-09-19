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

## Product rule

Rebuild **core + fatigue + desire + attachment + circadian + idle + memory + registers** in `hades_runtime/`, keyed `account_id+person_id`. Judge mouth by gold. Do not copy live state or `hades_emotion` as a vendor blob.
