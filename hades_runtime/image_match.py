"""Tag match after gate. Not cosine-only ONNX."""

from __future__ import annotations

import re

from hades_runtime.image_gate import allowed_for_tier


def _toks(text: str) -> set[str]:
    return set(re.findall(r"[a-z]+", (text or "").lower()))


def match_intent(intent: str, catalog: list[dict], tier: str) -> str | None:
    want = _toks(intent)
    best_path = None
    best = 0
    for row in catalog:
        path = row["path"]
        if not allowed_for_tier(tier, path):
            continue
        tags = {t.lower() for t in (row.get("tags") or [])}
        score = len(want & tags)
        if score > best:
            best = score
            best_path = path
    return best_path if best > 0 else None
