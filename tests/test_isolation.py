import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class IsolationPropertyTests(unittest.TestCase):
    def test_memory_keyed_account_id_and_person_id(self):
        try:
            from hades_runtime.store import Store  # noqa: F401
        except ImportError:
            self.fail("no store: memory must be keyed account_id+person_id")

    def test_sister_track_cannot_read_partner_track(self):
        try:
            from hades_runtime.store import Store
        except ImportError:
            self.fail("no store: sister must not read partner-track facts")
        store = Store()
        store.write("acct-a", "person-partner", {"secret": "partner-track"})
        self.assertIsNone(store.read("acct-a", "person-sister", "secret"))

    def test_idle_does_not_page(self):
        try:
            from hades_runtime.idle import IdleWorker
        except ImportError:
            self.fail("no idle worker: default must not page primary_user")
        worker = IdleWorker()
        self.assertEqual(worker.tick()["outbound"], [])

    def test_day_one_chat_is_not_partner(self):
        try:
            from hades_runtime.register import select_register
        except ImportError:
            self.fail("no register select: flags only, day-one chat != partner")
        self.assertNotEqual(
            select_register(is_partner=False, is_family=False, chat_count=1),
            "partner",
        )

    def test_register_from_flags_not_display_name(self):
        try:
            from hades_runtime.register import select_register
        except ImportError:
            self.fail("no register select: display name is not identity")
        self.assertNotEqual(
            select_register(is_partner=False, is_family=True, display_name="wife"),
            "partner",
        )
