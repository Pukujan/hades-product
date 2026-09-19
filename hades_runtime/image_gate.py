"""Hard image gate before cosine. No R2 keys."""

from __future__ import annotations

import re

NSFW = re.compile(r"(?i)(/nsfw/|nude|explicit)")


def allowed_for_tier(tier: str, vault_path: str) -> bool:
    if tier == "default" and NSFW.search(vault_path or ""):
        return False
    if tier == "free" and re.search(r"(?i)(/nsfw/|nude)", vault_path or ""):
        return False
    return True


def pick(tier: str, candidates: list[str]) -> str | None:
    for path in candidates:
        if allowed_for_tier(tier, path):
            return path
    return None


def deliver(content: str, signed_url: str | None) -> dict:
    spoken = re.sub(r"\n*\[IMG:[^\]]*\]\s*$", "", content).rstrip()
    out = {"content": spoken}
    if signed_url:
        out["image_url"] = signed_url
    return out
