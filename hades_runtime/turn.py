"""One turn. No reasoning on the wire. Register from flags."""

from __future__ import annotations

from hades_runtime.image_gate import deliver
from hades_runtime.packet import packet_messages
from hades_runtime.receipt import apply_once
from hades_runtime.register import select_register
from hades_runtime.store import Store

store = Store()


def handle_turn(
    account_id: str,
    person_id: str,
    text: str,
    is_partner: bool = False,
    is_family: bool = False,
    display_name: str | None = None,
    complete=None,
    state=None,
    signed_url=None,
) -> dict:
    register = select_register(
        is_partner=is_partner,
        is_family=is_family,
        display_name=display_name,
    )
    packet = {
        "schema_version": "1",
        "account_id": account_id,
        "person_id": person_id,
        "register": register,
        "tier": "default",
        "mood": {"center": 0.5, "depth": 1.0, "effective_mood": 0.0, "residual": 0.0},
        "itd": 0.0,
        "fatigue": 0.0,
        "circadian": 0.0,
        "lock": "default",
        "place": None,
    }
    if complete is None:
        content = ""
    else:
        content = complete(packet_messages(packet, text))
    st = state if state is not None else store
    rec = apply_once(st, account_id, person_id, text, {"last_register": register})
    out = deliver(content, signed_url)
    out.update(
        {
            "register": register,
            "receipt": rec["idempotency_key"],
            "schema_version": "1",
        }
    )
    if signed_url and ("CLOUDFLARE_R2_SECRET" in signed_url or "AKIA" in signed_url):
        raise RuntimeError("r2 key leaked to client")
    if "reasoning" in out:
        raise RuntimeError("reasoning leaked")
    return out
