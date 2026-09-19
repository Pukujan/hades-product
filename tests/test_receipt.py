import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hades_runtime.receipt import apply_once, receipt  # noqa: E402
from hades_runtime.store import Store  # noqa: E402


class ReceiptTests(unittest.TestCase):
    def test_no_reasoning_field(self):
        rec = receipt("a", "p", "hi")
        self.assertNotIn("reasoning", rec)
        self.assertNotIn("content", rec)

    def test_duplicate_inbound_does_not_double_write(self):
        store = Store()
        apply_once(store, "a", "p", "hi", {"mood": 1})
        apply_once(store, "a", "p", "hi", {"mood": 2})
        self.assertEqual(store.read("a", "p", "mood"), 1)
        self.assertEqual(len(store.read("a", "p", "receipts")), 1)
