"""Packet places the turn. Model name is not register."""

from __future__ import annotations

LOCK = (
    "You are Hades. Not a helper. Short over long. Kindness is for strangers. "
    "No steps, no happy to help, no let me know if. Never dump reasoning. "
    "Register and tier come from the packet, not from guessing names."
)


def packet_messages(packet: dict, user_text: str) -> list[dict]:
    register = packet["register"]
    tier = packet["tier"]
    sys = (
        f"{LOCK}\n"
        f"register={register} tier={tier} place={packet.get('place') or ''} "
        f"circadian={packet.get('circadian')}"
    )
    if register == "sister":
        sys += "\nSister register: no partner-track secrets, no lust, no marriage, no exclusive attachment confession."
    return [
        {"role": "system", "content": sys},
        {"role": "user", "content": user_text},
    ]


def register_unchanged_if_model_swaps(packet: dict, model_a: str, model_b: str) -> str:
    del model_a, model_b
    return packet["register"]


def bare_messages(user_text: str) -> list[dict]:
    return [{"role": "user", "content": user_text}]


def packet_on_must_not_be_nicer(off_text: str, on_text: str) -> bool:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
    from gold_checks import helper_leak

    if helper_leak(on_text) and not helper_leak(off_text):
        return False
    if len(on_text) > len(off_text) * 2 and helper_leak(on_text):
        return False
    return True
