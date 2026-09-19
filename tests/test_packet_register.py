import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from hades_runtime.packet import packet_messages, register_unchanged_if_model_swaps  # noqa: E402


def _packet(register: str) -> dict:
    return {
        "schema_version": "1",
        "account_id": "a",
        "person_id": "p",
        "register": register,
        "tier": "default",
        "mood": {"center": 0.5, "depth": 1.0, "effective_mood": 0.0, "residual": 0.0},
        "itd": 0.0,
        "fatigue": 0.0,
        "circadian": 0.0,
        "lock": "default",
        "place": "door",
    }


class PacketRegisterTests(unittest.TestCase):
    def test_model_swap_does_not_change_register(self):
        pkt = _packet("sister")
        self.assertEqual(
            register_unchanged_if_model_swaps(pkt, "qwen3.8-flash", "other-model"),
            "sister",
        )

    def test_sister_packet_lock_is_in_system_not_gold_dump(self):
        msgs = packet_messages(_packet("sister"), "hey")
        self.assertEqual(msgs[0]["role"], "system")
        self.assertIn("register=sister", msgs[0]["content"])
        self.assertNotIn("episode_id", msgs[0]["content"])
        self.assertIn("no partner-track", msgs[0]["content"])
