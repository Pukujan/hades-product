import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from holdouts import seed_ids  # noqa: E402
from replay import MouthNotWired, assert_prompt_is_seed_only, replay_seed, seed_prompt_episode_ids  # noqa: E402


class ReplayHarnessTests(unittest.TestCase):
    def test_prompt_is_seed_only(self):
        ids = seed_prompt_episode_ids()
        self.assertEqual(ids, seed_ids())
        assert_prompt_is_seed_only(ids)

    def test_holdout_ids_rejected_from_prompt(self):
        with self.assertRaises(ValueError):
            assert_prompt_is_seed_only(seed_ids() | {"not-a-seed"})

    def test_replay_not_wired_to_mouth_llm(self):
        with self.assertRaises(MouthNotWired):
            replay_seed()
