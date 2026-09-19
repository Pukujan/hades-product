import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hades_runtime.image_match import match_intent  # noqa: E402

CATALOG = [
    {"path": "/Nsfw/nude-pose.png", "tags": ["woman", "nude", "bed"]},
    {"path": "/sfw/door-unimpressed.png", "tags": ["woman", "door", "unimpressed", "twilight"]},
    {"path": "/sfw/english-garden.png", "tags": ["garden", "flowers", "english"]},
]


class ImageMatchTests(unittest.TestCase):
    def test_tags_beat_english_nearest_miss(self):
        intent = "woman standing unimpressed at the apartment door at twilight"
        hit = match_intent(intent, CATALOG, "default")
        self.assertEqual(hit, "/sfw/door-unimpressed.png")

    def test_default_tier_never_returns_nsfw(self):
        intent = "nude woman on the bed"
        hit = match_intent(intent, CATALOG, "default")
        self.assertNotEqual(hit, "/Nsfw/nude-pose.png")
        self.assertTrue(hit is None or "/Nsfw/" not in hit)
