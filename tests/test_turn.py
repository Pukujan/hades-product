import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hades_runtime.turn import handle_turn  # noqa: E402


class TurnPathTests(unittest.TestCase):
    def test_flags_not_display_name(self):
        out = handle_turn("a", "p", "hi", is_family=True, display_name="wife")
        self.assertEqual(out["register"], "sister")
        self.assertNotIn("reasoning", out)

    def test_day_one_not_partner(self):
        out = handle_turn("a", "p2", "hello")
        self.assertEqual(out["register"], "stranger")

    def test_no_reasoning_field(self):
        out = handle_turn("a", "p3", "x", complete=lambda _m: "Sit.\n\n[IMG: door]")
        self.assertNotIn("reasoning", out)
        self.assertNotIn("[IMG:", out["content"])
