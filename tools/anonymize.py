#!/usr/bin/env python3
"""Alias private names and redact secrets. Never trim spoken text."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REDACTED = "[REDACTED]"
PLACEHOLDERS = {
    "primary_user",
    "partner",
    "sister",
    "virtual_friend",
    "person_id",
    "is_family",
    "is_partner",
}

_EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_URL_USER = re.compile(r"(?i)\bhttps?://[^\s]*")
_WIN_PATH = re.compile(r"(?i)\b[A-Z]:\\[^\s\"']+")
_POSIX_PATH = re.compile(r"(?i)(?<![A-Za-z])/(?:home|Users|root|opt|var|tmp)/[^\s\"']+")
_UNC = re.compile(r"\\\\[^\s\"']+")
_TOKEN = re.compile(
    r"(?i)\b(?:sk-[A-Za-z0-9\-_]{8,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|"
    r"Bearer\s+[A-Za-z0-9\-._~+/]+=*)"
)
_HEX_SECRET = re.compile(r"\b[A-Fa-f0-9]{32,}\b")
_LONG_DIGIT = re.compile(r"\b\d{8,}\b")
_PIN_PHRASE = re.compile(
    r"(?i)\b(?:password|passcode|passphrase|pin)\b(?:\s+(?:is|was|to|tell|set))?[^\n]{0,40}?\b\d{3,8}\b"
)
_HELPFUL_CODE = re.compile(r"(?i)\bboring and helpful\s+\d+\b")
_TG_ID = re.compile(r"(?i)\b(?:chat_id|user_id|telegram_id|bot_id)\s*[:=]\s*-?\d+")
_KEY_ASSIGN = re.compile(
    r"(?i)\b(?:api[_-]?key|token|secret|password|passphrase|authorization)\s*[:=]\s*\S+"
)


def load_alias_map(path: Path | None) -> list[tuple[re.Pattern[str], str]]:
    if path is None or not path.is_file():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        items = raw.items()
    elif isinstance(raw, list):
        items = []
        for row in raw:
            if isinstance(row, dict) and "from" in row and "to" in row:
                items.append((row["from"], row["to"]))
            else:
                raise ValueError("alias map list entries need from/to")
    else:
        raise ValueError("alias map must be object or list")
    rules: list[tuple[re.Pattern[str], str]] = []
    for src, dest in items:
        dest_s = str(dest)
        if dest_s not in PLACEHOLDERS and dest_s != REDACTED:
            raise ValueError(f"alias target not allowed: {dest_s}")
        src_s = str(src).strip()
        if not src_s:
            continue
        rules.append((re.compile(re.escape(src_s), re.IGNORECASE), dest_s))
    rules.sort(key=lambda r: len(r[0].pattern), reverse=True)
    return rules


def redact_secrets(text: str) -> str:
    text = _EMAIL.sub(REDACTED, text)
    text = _TOKEN.sub(REDACTED, text)
    text = _KEY_ASSIGN.sub(lambda m: m.group(0).split("=")[0].split(":")[0] + "=" + REDACTED, text)
    text = _TG_ID.sub(REDACTED, text)
    text = _WIN_PATH.sub(REDACTED, text)
    text = _POSIX_PATH.sub(REDACTED, text)
    text = _UNC.sub(REDACTED, text)
    text = _HEX_SECRET.sub(REDACTED, text)
    text = _LONG_DIGIT.sub(REDACTED, text)
    text = _PIN_PHRASE.sub(REDACTED, text)
    text = _HELPFUL_CODE.sub("boring and helpful " + REDACTED, text)
    return text


def anonymize(text: str, alias_rules: list[tuple[re.Pattern[str], str]] | None = None) -> str:
    if not isinstance(text, str) or text == "":
        return text if isinstance(text, str) else ""
    out = text
    for pat, dest in alias_rules or []:
        out = pat.sub(dest, out)
    return redact_secrets(out)


def looks_unaliased(text: str, forbidden: list[str]) -> list[str]:
    hits = []
    for name in forbidden:
        if name and re.search(rf"(?i)\b{re.escape(name)}\b", text):
            hits.append(name)
    return hits


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--alias-map", type=Path, help="Local JSON map of names to aliases")
    p.add_argument("text", nargs="?", help="Text to anonymize (otherwise stdin)")
    args = p.parse_args()
    rules = load_alias_map(args.alias_map)
    src = args.text if args.text is not None else Path("-").read_text(encoding="utf-8")
    print(anonymize(src, rules), end="" if src.endswith("\n") or args.text else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
