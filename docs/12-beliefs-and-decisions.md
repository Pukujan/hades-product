# Beliefs and decisions (2026-09-19 sitting)

Distilled knowledge pack. **Not** the raw Kilo transcript (secrets, names, BUILD: no kilo dumps). SoT for tenancy/scale: `plans/TENANCY_STATE.md`. Mouth: `gold/` + BUILD PDD.

## Believed until now

1. Product lives in **this repo**. Research `hades-v2` is reference (SHA `a783d91`). Do not vendor `hades_emotion` as a blob.
2. Origin has **1618** files. Self ≈ `src/hades_emotion` (~203 py) + `plugins/pre-llm-pipeline` + `schema`/`dynamics`/`circadian`. Skills/data dumps are not the self.
3. Three copies: **git** = July code; **memories** = Sep export; **WSL Hermes** = live (`emotion-project-host-v2`). Gravebuster not reached this sitting.
4. `schema.yaml`/`dynamics.yaml` hashes match across copies. Live yaml/json **do not**.
5. Native scales stay (mood −10…10, fatigue 0–6, depth 0–200). No 0–100 engine remap. Pre-LLM may *display* percents; physics do not change.
6. Each **account** is a separate Hades. Shared = code/templates only. Numbers, people, timezone clock never bleed. Auth token **is** `account_id` (OWASP API1).
7. **Founder** (you): one-time anonymized import of live state. **B/C/D:** start at zero.
8. SoT = **DB row**, not RAM, not client, not host yaml after cutover.
9. Silent ≠ dead. Lazy elapsed physics. LLM inner life only hot/opt-in. 5–6d cold = 0 thought tokens. Default **does not page**.
10. Mouth: gold replay. Cascade cheap→strong. Not frontier-for-everything. Not a reply library. Not on the client.
11. Hebbian **27×27** exists; memories ~17k ticks, 47 nonzero, capability `emotional_nuance` only. **No new emotion nodes.** Flag unread by pre-LLM — does **not** drive deltas today.
12. Packet is short `[CURRENT STATE]`+lock every turn. KV cache ≠ attention. Hermes **session** compaction ≠ her memory.
13. Recall: salience + recency + rehearsal (research). Product: top-k episodic on server. No React memory cache.
14. Observability: OTEL $ / latency. No Langfuse full prompts. D007: LLM-as-judge is not a pass.
15. Standing git: commit each green bead, then push. `.env` never committed.

## External sources used

OWASP API4, API1, DoS + Bot cheat sheets; Cloudflare Turnstile; Azure tenancy models; FrugalGPT; RouteLLM; vLLM PagedAttention; EmotionPrompt; Lost in the Middle; Hebb/STDP/Oja; Mead/Loihi (neuromorphic ≠ this numpy matrix).

## Not done

Port engines. Real DB. Founder import. Gravebuster inventory. Vault/ONNX. React. CI. Wire `activate()` → mood_delta. FOSSIL of **this chat raw**.

## Continue

`plans/CONTINUE.md` + `plans/session/HANDOFF.md`.
