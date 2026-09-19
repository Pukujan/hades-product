import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = json.loads((ROOT / "gold" / "packet.schema.json").read_text(encoding="utf-8"))
PYPROJECT = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
DOCS04 = (ROOT / "docs" / "04-product-architecture.md").read_text(encoding="utf-8")


class PacketSchemaTests(unittest.TestCase):
    def test_packet_in_has_required_fields(self):
        req = PACKET["$defs"]["packet_in"]["required"]
        for key in (
            "schema_version",
            "account_id",
            "person_id",
            "register",
            "tier",
            "mood",
            "itd",
            "fatigue",
            "circadian",
            "lock",
            "place",
        ):
            self.assertIn(key, req)

    def test_mouth_out_has_no_reasoning_field(self):
        props = PACKET["$defs"]["mouth_out"]["properties"]
        self.assertIn("content", props)
        self.assertNotIn("reasoning", props)
        self.assertFalse(PACKET["$defs"]["mouth_out"].get("additionalProperties", True))

    def test_pyproject_has_no_mouth_llm(self):
        low = PYPROJECT.lower()
        self.assertNotIn("fastapi", low)
        self.assertNotIn("qwen", low)
        self.assertNotIn("openai", low)
        self.assertIn('name = "hades-product"', PYPROJECT)

    def test_runtime_sha_pinned(self):
        self.assertIn("a783d91a3ba1e847371e0f3aaef2a65b5cf50507", DOCS04)
        self.assertIn("2c62ff1266c5047cd9d26a6cb306f9f6022fbddf", DOCS04)
