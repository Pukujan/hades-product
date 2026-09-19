"""Memory keyed account_id+person_id. No global secrets file."""

from __future__ import annotations


class Store:
    def __init__(self) -> None:
        self._data: dict[tuple[str, str], dict] = {}

    def write(self, account_id: str, person_id: str, payload: dict) -> None:
        key = (account_id, person_id)
        row = dict(self._data.get(key) or {})
        row.update(payload)
        self._data[key] = row

    def read(self, account_id: str, person_id: str, field: str | None = None):
        row = self._data.get((account_id, person_id)) or {}
        if field is None:
            return dict(row)
        return row.get(field)
