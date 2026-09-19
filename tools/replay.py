"""Seed gold replay harness. Holdouts never enter the prompt. Live mouth is opt-in."""

from __future__ import annotations

from pathlib import Path

from holdouts import ci_ids, load_holdout_bodies, sealed_ids, seed_ids

ROOT = Path(__file__).resolve().parents[1]


class MouthNotWired(NotImplementedError):
    pass


def seed_prompt_episode_ids() -> set[str]:
    rows = load_holdout_bodies("seed")
    return {row["episode_id"] for row in rows}


def assert_prompt_is_seed_only(episode_ids: set[str]) -> None:
    bad = episode_ids & (ci_ids() | sealed_ids())
    if bad:
        raise ValueError("holdout ids in prompt")
    extra = episode_ids - seed_ids()
    if extra:
        raise ValueError("non-seed ids in prompt")


def _packet_for(row: dict) -> dict:
    return {
        "schema_version": "1",
        "account_id": "seed",
        "person_id": row["session_id"],
        "register": row["register"],
        "tier": "default",
        "mood": {"center": 0.5, "depth": 1.0, "effective_mood": 0.0, "residual": 0.0},
        "itd": 0.0,
        "fatigue": 0.0,
        "circadian": 0.0,
        "lock": "default",
        "place": None,
    }


def replay_seed() -> list[dict]:
    import os
    import sys

    if os.environ.get("HADES_MOUTH_LIVE") != "1":
        raise MouthNotWired("live replay off; set HADES_MOUTH_LIVE=1")
    sys.path.insert(0, str(ROOT))
    from hades_runtime.packet import packet_messages
    from mouth import complete

    rows = load_holdout_bodies("seed")
    assert_prompt_is_seed_only({row["episode_id"] for row in rows})
    out = []
    for row in rows:
        if row.get("role") != "user":
            continue
        text = complete(packet_messages(_packet_for(row), row["content"]))
        out.append({"episode_id": row["episode_id"], "content": text, "register": row["register"]})
    return out
