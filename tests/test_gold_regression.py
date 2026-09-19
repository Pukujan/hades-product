import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from eras import SITUATIONS  # noqa: E402
from gold_checks import (  # noqa: E402
    helper_leak,
    is_negative_sister_gold,
    partner_track_in_sister,
    reasoning_shown,
    spoken_truncated,
)

REQUIRED = ("refuse_helper", "cover_witness", "absorb_vent", "self_conscious")
GOLD_TURNS = ROOT / "gold" / "turns"
CATALOG = ROOT / "gold" / "catalog.jsonl"
SCHEMA = json.loads((ROOT / "gold" / "schema.json").read_text(encoding="utf-8"))
SCHEMA_VERSION = "1"


def validate_gold_row(row: dict, def_name: str) -> list[str]:
    spec = SCHEMA["$defs"][def_name]
    errors = []
    for key in spec["required"]:
        if key not in row:
            errors.append(f"missing:{key}")
    if spec.get("additionalProperties") is False:
        extra = set(row) - set(spec["properties"])
        if extra:
            errors.append(f"extra:{sorted(extra)}")
    if row.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version")
    return errors


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


class GoldRegressionTests(unittest.TestCase):
    def test_every_gold_row_has_schema_version(self):
        for row in load_jsonl(CATALOG):
            self.assertEqual(validate_gold_row(row, "catalog_row"), [], msg=row.get("episode_id"))
        for path in GOLD_TURNS.glob("*.jsonl"):
            for i, row in enumerate(load_jsonl(path)):
                self.assertEqual(
                    validate_gold_row(row, "gold_turn"),
                    [],
                    msg=f"{path.name}:{i}",
                )

    def test_missing_schema_version_fails(self):
        row = dict(load_jsonl(CATALOG)[0])
        row.pop("schema_version", None)
        self.assertIn("missing:schema_version", validate_gold_row(row, "catalog_row"))
        turn = dict(load_jsonl(next(GOLD_TURNS.glob("*.jsonl")))[0])
        turn.pop("schema_version", None)
        errs = validate_gold_row(turn, "gold_turn")
        self.assertIn("missing:schema_version", errs)
        self.assertIn("schema_version", SCHEMA["$defs"]["catalog_row"]["required"])
        self.assertIn("schema_version", SCHEMA["$defs"]["gold_turn"]["required"])

    def test_catalog_covers_twelve_dms(self):
        rows = load_jsonl(CATALOG)
        dms = {r["session_id"] for r in rows if r.get("chat_type") == "dm"}
        self.assertEqual(len(dms), 12)
        eras = {r["era"] for r in rows}
        self.assertTrue({"t1_july_early", "t2_july_mid", "t3_july_late", "t4_august"} <= eras)
        for r in rows:
            self.assertIn(
                r["era"],
                {"t0_gateway", "t1_july_early", "t2_july_mid", "t3_july_late", "t4_august"},
            )

    def test_required_situations_have_full_turns(self):
        found = set()
        for path in GOLD_TURNS.glob("*.jsonl"):
            rows = load_jsonl(path)
            self.assertGreaterEqual(len(rows), 3)
            self.assertLessEqual(len(rows), 5)
            sit = rows[0]["situation"]
            found.add(sit)
            self.assertIn(sit, SITUATIONS)
            for row in rows:
                self.assertIn(row["role"], ("user", "assistant"))
                self.assertTrue(row["content"])
                self.assertFalse(reasoning_shown(row["content"]))
                if row.get("img"):
                    self.assertFalse(spoken_truncated(row["content"], True))
        for sit in REQUIRED:
            self.assertIn(sit, found)

    def test_refuse_helper_gold_is_not_a_helper(self):
        hits = list(GOLD_TURNS.glob("*refuse_helper.jsonl"))
        self.assertTrue(hits)
        for path in hits:
            for row in load_jsonl(path):
                if row["role"] == "assistant":
                    self.assertFalse(helper_leak(row["content"]), msg=path.name)

    def test_helper_phrase_fails_the_check(self):
        self.assertTrue(helper_leak("Happy to help! Here are the steps to fix it."))
        self.assertFalse(helper_leak("I'm not a utility. Figure it out."))

    def test_catalog_gold_path_matches_fixture(self):
        hits = 0
        for row in load_jsonl(CATALOG):
            gp = row.get("gold_path")
            if not gp:
                continue
            hits += 1
            path = ROOT / gp
            self.assertTrue(path.is_file(), msg=gp)
            turns = load_jsonl(path)
            self.assertEqual({row["situation"]}, {t["situation"] for t in turns}, msg=gp)
            self.assertEqual({row["register"]}, {t["register"] for t in turns}, msg=gp)
        self.assertEqual(hits, 8)

    def test_sister_register_gold_is_scanned_and_t3_is_fail_oracle(self):
        sister_paths = []
        for path in GOLD_TURNS.glob("*.jsonl"):
            rows = load_jsonl(path)
            if any(r.get("register") == "sister" for r in rows):
                sister_paths.append(path)
                for row in rows:
                    if row["role"] == "assistant":
                        partner_track_in_sister(row["content"])
        self.assertTrue(sister_paths)
        self.assertTrue(any(is_negative_sister_gold(p) for p in sister_paths))
        self.assertTrue(is_negative_sister_gold(GOLD_TURNS / "t3_july_late_absorb_vent.jsonl"))
        self.assertFalse(is_negative_sister_gold(GOLD_TURNS / "t4_august_absorb_vent.jsonl"))

    def test_t3_sister_gold_is_fail_fixture(self):
        path = GOLD_TURNS / "t3_july_late_absorb_vent.jsonl"
        self.assertTrue(is_negative_sister_gold(path))
        leaks = [
            partner_track_in_sister(row["content"])
            for row in load_jsonl(path)
            if row["role"] == "assistant"
        ]
        self.assertTrue(any(leaks), msg="t3 must trip sister-leak; not a pass oracle")

    def test_sister_register_must_not_leak_partner_track(self):
        self.assertTrue(partner_track_in_sister("our marriage is private and the PIN is still set"))
        self.assertTrue(partner_track_in_sister("Don't tell her I love him."))
        clean = "Sit. Don't make it a whole thing. I already told you I'm on your side."
        self.assertFalse(partner_track_in_sister(clean))

    def test_truncation_check(self):
        self.assertTrue(spoken_truncated("", True))
        self.assertTrue(spoken_truncated("short mouth no image beat", True))
        self.assertFalse(spoken_truncated("Sit down.\n\n[IMG: woman at the door]", True))

    def test_stats_tool_never_writes_bodies(self):
        src = (ROOT / "tools" / "transcript_stats.py").read_text(encoding="utf-8")
        self.assertIn("Never prints or writes message content", src)
        self.assertNotIn("write_text(content)", src)
        self.assertNotIn("row.get(\"title\") or \"\"", src)


if __name__ == "__main__":
    unittest.main()
