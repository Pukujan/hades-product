"""Idle tick. Default: mutate state, do not page."""

from __future__ import annotations

from hades_runtime.store import Store


class IdleWorker:
    def __init__(self, store: Store | None = None) -> None:
        self.store = store or Store()
        self.ticks = 0

    def tick(self, account_id: str = "acct", person_id: str = "self") -> dict:
        self.ticks += 1
        mood = self.store.read(account_id, person_id, "mood") or 0.0
        self.store.write(account_id, person_id, {"mood": float(mood) + 0.01, "idle_ticks": self.ticks})
        return {"outbound": [], "ticks": self.ticks}
