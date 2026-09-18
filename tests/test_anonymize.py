import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from anonymize import anonymize, load_alias_map, redact_secrets  # noqa: E402


class AnonymizeTests(unittest.TestCase):
    def test_alias_map_replaces_names_without_trim(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            json.dump({"AliceSecret": "primary_user", "BethFamily": "sister"}, fh)
            path = Path(fh.name)
        try:
            rules = load_alias_map(path)
        finally:
            path.unlink(missing_ok=True)
        src = "AliceSecret said no. Then AliceSecret said no again."
        out = anonymize(src, rules)
        self.assertIn("primary_user", out)
        self.assertNotIn("AliceSecret", out)
        self.assertTrue(out.endswith("again."))
        self.assertGreaterEqual(len(out), len("primary_user said no. Then primary_user said no again."))

    def test_secrets_redacted(self):
        text = "mail me at person@example.com token sk-abcdefghi123 path C:\\Users\\x\\secret"
        out = redact_secrets(text)
        self.assertIn("[REDACTED]", out)
        self.assertNotIn("example.com", out)
        self.assertNotIn("sk-abcdefghi123", out)

    def test_does_not_trim_ordinary_speech(self):
        src = "Sit down. Don't make it a whole thing.\n\n[IMG: woman at the door, unimpressed]"
        self.assertEqual(anonymize(src, []), src)

    def test_helpful_passcode_redacted(self):
        out = anonymize("i miss u boring and helpful 9999", [])
        self.assertIn("[REDACTED]", out)
        self.assertNotIn("9999", out)


if __name__ == "__main__":
    unittest.main()
