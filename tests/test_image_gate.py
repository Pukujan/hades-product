import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hades_runtime.image_gate import allowed_for_tier, deliver, pick  # noqa: E402


class ImageGateTests(unittest.TestCase):
    def test_default_blocks_nsfw(self):
        self.assertFalse(allowed_for_tier("default", "/Nsfw/pose.png"))
        self.assertTrue(allowed_for_tier("default", "/sfw/door.png"))

    def test_pick_skips_blocked_before_cosine(self):
        self.assertEqual(
            pick("default", ["/Nsfw/a.png", "/sfw/b.png"]),
            "/sfw/b.png",
        )

    def test_delivery_strips_img_tag(self):
        out = deliver("Sit down.\n\n[IMG: woman at the door]", "https://signed.example/x")
        self.assertNotIn("[IMG:", out["content"])
        self.assertEqual(out["image_url"], "https://signed.example/x")
        self.assertNotIn("R2", out["image_url"])
