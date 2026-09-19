# Continue the product

Accepted working plan: `plans/TENANCY_STATE.md`. Mouth still gold-first.

## Next beads (in order)

1. Character-state schema in store (`account_id`, timezone, packet fields). Isolation tests: A tick ↛ B.
2. Circadian/fatigue **lazy** elapsed apply using **account timezone**.
3. Packet builder from store (short state+lock). Gold properties. Packet-on not nicer.
4. Episodic top-k recall (salience) into packet. No session dump.
5. Founder import tool (gitignored name map) — your live yaml → founder rows. Others stay zero.
6. Port ticker: core + circadian + fatigue + desire + attachment + idle (no host paths).
7. Optional: `activate()` → small mood_delta; A/B vs gold.
8. Mouth cascade behind gold. OTEL metrics no bodies.
9. Image vault/ONNX still outside. React last.

Do not: commit `.env`, copy `relations.yaml`, vendor 203 files, React-as-memory, LLM-as-bot, cron-all 100k.
