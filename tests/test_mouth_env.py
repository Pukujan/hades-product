import sys
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from mouth import ENV_PATH, load_env, mouth_config  # noqa: E402


class MouthEnvTests(unittest.TestCase):
    def test_env_is_gitignored(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".env", gitignore)
        r = subprocess.run(
            ["git", "check-ignore", "-q", ".env"],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(r.returncode, 0)

    def test_example_has_no_secret(self):
        text = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("HADES_MOUTH_API_KEY=", text)
        self.assertNotIn("yolo-", text.lower())
        self.assertIn("qwen3.8-flash", text)

    def test_config_loads_without_exposing_key_in_source(self):
        src = (ROOT / "tools" / "mouth.py").read_text(encoding="utf-8")
        self.assertNotIn("yolo-auto.com", src)
        if not ENV_PATH.is_file():
            self.skipTest("no local .env")
        cfg = mouth_config()
        self.assertTrue(cfg["url"].startswith("https://"))
        self.assertEqual(cfg["model"], "qwen3.8-flash")
        self.assertGreater(len(cfg["key"]), 8)
