import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hades_runtime.store import FileStore  # noqa: E402
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

    def test_filestore_persists_register(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = FileStore(tmp)
            handle_turn("acct", "p", "hi", is_partner=True, state=st)
            st2 = FileStore(tmp)
            self.assertEqual(st2.read("acct", "p", "last_register"), "partner")
            self.assertIsNone(st2.read("acct", "sister", "last_register"))

    def test_signed_url_not_a_key(self):
        out = handle_turn(
            "a",
            "p4",
            "x",
            complete=lambda _m: "Sit.\n\n[IMG: door]",
            signed_url="https://signed.example/sfw/door.png?X-Amz-Signature=abc",
        )
        self.assertEqual(out["image_url"].startswith("https://"), True)
        self.assertNotIn("SECRET", out["image_url"])
