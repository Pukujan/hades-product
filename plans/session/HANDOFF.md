# Handoff — overnight auto

Replace this file when the next sitting ends.

## Done

- B0–B10, B12, B13/B15 in-memory, B11 gate + tag matcher (no ONNX).
- B14 metamorphic: register flip, circadian, model swap, packet-on nicer-fail. Live sister flip + packet on/off **OK**.
- Turn path: flags → packet → mouth hook → deliver → receipt. No reasoning.

## Verify

`python -m unittest discover -s tests`

Live: `$env:HADES_MOUTH_LIVE=1` (metamorphic + replay).

## Next

Real vault/ONNX still outside — do not copy memories. React (B16) last. FOSSIL (B17) optional. Do not commit `.env`.

## Fail if

- `.env` committed
- t3 pass sister mouth
- holdouts in prompts
- Qwen as architecture
