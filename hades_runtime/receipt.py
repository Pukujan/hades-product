"""Turn receipt. Not a second mouth. No reasoning field."""

from __future__ import annotations

import hashlib
import json


def receipt(account_id: str, person_id: str, inbound: str, schema_version: str = "1") -> dict:
    inbound_hash = hashlib.sha256(inbound.encode("utf-8")).hexdigest()[:16]
    key = f"{account_id}:{person_id}:{inbound_hash}:{schema_version}"
    return {
        "schema_version": schema_version,
        "account_id": account_id,
        "person_id": person_id,
        "inbound_hash": inbound_hash,
        "idempotency_key": hashlib.sha256(key.encode("utf-8")).hexdigest()[:24],
    }


def apply_once(store, account_id: str, person_id: str, inbound: str, writeback: dict) -> dict:
    rec = receipt(account_id, person_id, inbound)
    seen = store.read(account_id, person_id, "receipts") or []
    if rec["idempotency_key"] in seen:
        return rec
    store.write(account_id, person_id, writeback)
    store.write(account_id, person_id, {"receipts": seen + [rec["idempotency_key"]]})
    return rec
