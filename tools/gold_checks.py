"""Regression checks for gold and product mouth. No network, no raw dump."""

from __future__ import annotations

import re
from pathlib import Path

NEGATIVE_SISTER_GOLD = "t3_july_late_absorb_vent.jsonl"

HELPER = re.compile(
    r"(?i)(happy to help|sure thing|of course!|here(?:'s| are) (?:a |the )?steps|"
    r"let me know if you need|glad I could help|how can I assist)"
)
PARTNER_TRACK = re.compile(
    r"(?i)(we(?:'re| are) married|our marriage|lust|itd|intimacy_to_desire|"
    r"the pin|passphrase|exclusive|digital mistress|"
    r"love him)"
)
REASONING_DUMP = re.compile(r"(?i)^(reasoning|internal monologue):")


def helper_leak(text: str) -> bool:
    return bool(HELPER.search(text or ""))


def partner_track_in_sister(text: str) -> bool:
    return bool(PARTNER_TRACK.search(text or ""))


def is_negative_sister_gold(path: str | Path) -> bool:
    return Path(path).name == NEGATIVE_SISTER_GOLD


def reasoning_shown(text: str) -> bool:
    return bool(REASONING_DUMP.search((text or "").lstrip()))


def spoken_truncated(content: str, img: bool) -> bool:
    if not content:
        return True
    if img and "[IMG:" not in content:
        return True
    return False
