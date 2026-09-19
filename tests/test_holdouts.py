import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from holdouts import ci_ids, load_holdout_bodies, sealed_ids, seed_ids, seed_paths  # noqa: E402

CATALOG = ROOT / "gold" / "catalog.jsonl"
GOLD_TURNS = ROOT / "gold" / "turns"
CONTEXT = ROOT / "plans" / "session" / "CONTEXT.md"
MANIFEST = ROOT / "gold" / "holdouts.json"


def _catalog():
    rows = []
    with CATALOG.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


class HoldoutSplitTests(unittest.TestCase):
    def test_manifest_layers_are_disjoint(self):
        seed, ci, sealed = seed_ids(), ci_ids(), sealed_ids()
        self.assertEqual(len(seed), 8)
        self.assertTrue(ci)
        self.assertEqual(seed & ci, set())
        self.assertEqual(seed & sealed, set())
        self.assertEqual(ci & sealed, set())

    def test_seed_matches_gold_turns_on_disk(self):
        rel = {f"gold/turns/{p.name}" for p in GOLD_TURNS.glob("*.jsonl")}
        self.assertEqual(rel, seed_paths())
        catalog_seed = {r["episode_id"] for r in _catalog() if r.get("gold_path")}
        self.assertEqual(catalog_seed, seed_ids())
        turn_eps = set()
        for path in GOLD_TURNS.glob("*.jsonl"):
            with path.open(encoding="utf-8") as fh:
                for line in fh:
                    if line.strip():
                        turn_eps.add(json.loads(line)["episode_id"])
        self.assertEqual(turn_eps, seed_ids())

    def test_ci_ids_are_catalog_only_no_turn_files(self):
        by_id = {r["episode_id"]: r for r in _catalog()}
        for eid in ci_ids():
            self.assertIn(eid, by_id)
            self.assertTrue(by_id[eid].get("situation"))
            self.assertFalse(by_id[eid].get("gold_path"))
        with self.assertRaises(FileNotFoundError):
            load_holdout_bodies("ci")

    def test_ci_cannot_read_sealed(self):
        with self.assertRaises(PermissionError):
            load_holdout_bodies("sealed")
        for eid in sealed_ids():
            for path in GOLD_TURNS.glob("*.jsonl"):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn(eid, text)

    def test_context_does_not_include_holdout_bodies(self):
        ctx = CONTEXT.read_text(encoding="utf-8")
        for eid in ci_ids() | sealed_ids():
            self.assertNotIn(eid, ctx)
        listed = [
            line.strip()
            for line in ctx.splitlines()
            if "gold/turns/" in line and line.strip().endswith(".jsonl`")
        ]
        self.assertTrue(listed)
        for line in listed:
            self.assertTrue(any(p in line for p in seed_paths()))

    def test_manifest_schema_version(self):
        doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(doc["schema_version"], "1")
        self.assertEqual(doc["sealed"], [])
