import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hades_runtime.signed_url import signed_get_url  # noqa: E402
from hades_runtime.store import FileStore  # noqa: E402


class PersistAndSignTests(unittest.TestCase):
    def test_file_store_roundtrip_and_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = FileStore(tmp)
            a.write("acct-a", "partner", {"secret": "partner-track"})
            b = FileStore(tmp)
            self.assertEqual(b.read("acct-a", "partner", "secret"), "partner-track")
            self.assertIsNone(b.read("acct-a", "sister", "secret"))
            self.assertIsNone(b.read("acct-b", "partner", "secret"))

    def test_signed_url_has_no_secret(self):
        secret = "supersecret-r2-key"
        url = signed_get_url(
            "sfw/door.png",
            endpoint="https://example.r2.cloudflarestorage.com",
            bucket="vault",
            access_key="AKIAEXAMPLE",
            secret_key=secret,
        )
        self.assertTrue(url.startswith("https://"))
        self.assertNotIn(secret, url)
        self.assertIn("X-Amz-Signature=", url)
        self.assertNotIn("supersecret", url)
