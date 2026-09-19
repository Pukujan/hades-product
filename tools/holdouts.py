"""Seed / CI / sealed split. Sealed bodies never live in this repo."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "gold" / "holdouts.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def seed_ids() -> set[str]:
    return {row["episode_id"] for row in load_manifest()["seed"]}


def seed_paths() -> set[str]:
    return {row["gold_path"] for row in load_manifest()["seed"]}


def ci_ids() -> set[str]:
    return set(load_manifest()["ci"])


def sealed_ids() -> set[str]:
    return set(load_manifest()["sealed"])


def load_holdout_bodies(layer: str) -> list[dict]:
    if layer == "sealed":
        raise PermissionError("sealed holdouts are not readable in this repo or CI")
    if layer == "ci":
        raise FileNotFoundError("CI holdouts have no gold/turns bodies in this repo")
    if layer != "seed":
        raise ValueError(layer)
    rows = []
    for rel in seed_paths():
        path = ROOT / rel
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows
