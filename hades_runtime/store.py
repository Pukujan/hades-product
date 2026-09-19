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


class FileStore(Store):
    def __init__(self, root) -> None:
        super().__init__()
        from pathlib import Path
        import json

        self._root = Path(root)
        self._root.mkdir(parents=True, exist_ok=True)
        self._json = json
        self._load()

    def _path(self, account_id: str, person_id: str):
        safe = f"{account_id}__{person_id}.json".replace("/", "_")
        return self._root / safe

    def _load(self) -> None:
        for path in self._root.glob("*.json"):
            row = self._json.loads(path.read_text(encoding="utf-8"))
            acc, person = row["account_id"], row["person_id"]
            data = dict(row)
            data.pop("account_id", None)
            data.pop("person_id", None)
            self._data[(acc, person)] = data

    def write(self, account_id: str, person_id: str, payload: dict) -> None:
        super().write(account_id, person_id, payload)
        row = {"account_id": account_id, "person_id": person_id, **self._data[(account_id, person_id)]}
        self._path(account_id, person_id).write_text(
            self._json.dumps(row), encoding="utf-8"
        )
