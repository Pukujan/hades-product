import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from eras import SITUATIONS  # noqa: E402
from gold_checks import helper_leak, partner_track_in_sister, reasoning_shown, spoken_truncated  # noqa: E402

REQUIRED = ("refuse_helper", "cover_witness", "absorb_vent", "self_conscious")
GOLD_TURNS = ROOT / "gold" / "turns"
CATALOG = ROOT / "gold" / "catalog.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


class GoldRegressionTests(unittest.TestCase):
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
                self.assertNotIn("reasoning", row["content"][:20].lower())
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

    def test_sister_register_must_not_leak_partner_track(self):
        self.assertTrue(partner_track_in_sister("our marriage is private and the PIN is still set"))
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
