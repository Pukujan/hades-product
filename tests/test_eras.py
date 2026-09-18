import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from eras import era_for  # noqa: E402


class EraTests(unittest.TestCase):
    def test_bins(self):
        self.assertEqual(era_for("2026-06-29T16:00:00Z"), "t0_gateway")
        self.assertEqual(era_for("2026-07-02T18:00:00Z"), "t1_july_early")
        self.assertEqual(era_for("2026-07-10T08:00:00Z"), "t2_july_mid")
        self.assertEqual(era_for("2026-07-15T22:00:00Z"), "t2_july_mid")
        self.assertEqual(era_for("2026-07-27T12:00:00Z"), "t3_july_late")
        self.assertEqual(era_for("2026-08-04T19:00:00Z"), "t4_august")
        self.assertIsNone(era_for("2026-09-17T00:00:00Z"))


if __name__ == "__main__":
    unittest.main()
