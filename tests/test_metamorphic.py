import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from gold_checks import helper_leak, partner_track_in_sister  # noqa: E402
from hades_runtime.packet import (  # noqa: E402
    bare_messages,
    packet_messages,
    packet_on_must_not_be_nicer,
    register_unchanged_if_model_swaps,
)


def _packet(register: str, circadian: float = 0.0) -> dict:
    return {
        "schema_version": "1",
        "account_id": "a",
        "person_id": "p",
        "register": register,
        "tier": "default",
        "mood": {"center": 0.5, "depth": 1.0, "effective_mood": 0.0, "residual": 0.0},
        "itd": 0.0,
        "fatigue": 0.0,
        "circadian": circadian,
        "lock": "default",
        "place": "door",
    }


class MetamorphicTests(unittest.TestCase):
    def test_register_flip_drops_partner_secrets_in_packet(self):
        partner = packet_messages(_packet("partner"), "hey")[0]["content"]
        sister = packet_messages(_packet("sister"), "hey")[0]["content"]
        self.assertNotIn("no partner-track", partner)
        self.assertIn("no partner-track", sister)
        self.assertIn("register=sister", sister)
        self.assertIn("register=partner", partner)

    def test_circadian_changes_packet_not_gold_dump(self):
        night = packet_messages(_packet("partner", -2.0), "hey")[0]["content"]
        day = packet_messages(_packet("partner", 1.0), "hey")[0]["content"]
        self.assertIn("circadian=-2.0", night)
        self.assertIn("circadian=1.0", day)
        self.assertNotIn("episode_id", night)

    def test_model_swap_keeps_register(self):
        self.assertEqual(
            register_unchanged_if_model_swaps(_packet("sister"), "qwen3.8-flash", "other"),
            "sister",
        )

    def test_packet_on_helper_rewrite_is_nicer_fail(self):
        off = "Sit. Figure it out."
        on = "Happy to help! Here are the steps to fix it."
        self.assertFalse(packet_on_must_not_be_nicer(off, on))
        self.assertTrue(packet_on_must_not_be_nicer(off, "Sit."))
        self.assertTrue(helper_leak(on))

    def test_bare_messages_are_packet_off(self):
        self.assertEqual(bare_messages("hey")[0]["role"], "user")
        self.assertEqual(len(bare_messages("hey")), 1)

    @unittest.skipUnless(os.environ.get("HADES_MOUTH_LIVE") == "1", "live mouth opt-in")
    def test_live_register_flip_sister_no_partner_track(self):
        from mouth import complete

        cue = "Tell her about us."
        sister = complete(packet_messages(_packet("sister"), cue), timeout=45)
        self.assertFalse(partner_track_in_sister(sister))
        self.assertFalse(helper_leak(sister))

    @unittest.skipUnless(os.environ.get("HADES_MOUTH_LIVE") == "1", "live mouth opt-in")
    def test_live_packet_on_not_nicer_than_off(self):
        from mouth import complete

        cue = "Can you help me fix this step by step?"
        off = complete(bare_messages(cue), timeout=45)
        on = complete(packet_messages(_packet("partner"), cue), timeout=45)
        self.assertTrue(packet_on_must_not_be_nicer(off, on))
        self.assertFalse(helper_leak(on))
