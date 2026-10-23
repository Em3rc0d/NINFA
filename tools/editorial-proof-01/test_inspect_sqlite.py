"""Evidence authenticity and regression checks. No external dependencies."""
import unittest
import tempfile
import importlib.util
from pathlib import Path
import sys
import json
import sqlite3
import io
from contextlib import redirect_stdout
import subprocess

SCRIPT = Path(__file__).with_name("inspect_sqlite.py")
spec = importlib.util.spec_from_file_location("ninfa_editorial_inspector", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class InspectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)
        replay = Path(__file__).resolve().parents[1] / "motion-v15" / "replay_lab.py"
        subprocess.run([sys.executable, str(replay), "--out", str(self.folder)], check=True, capture_output=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_actual_content_hashed_receipt_and_readonly_db(self):
        report = mod.verify_receipt(self.folder)
        self.assertEqual(report["guarded"]["new_actions"], 1)
        self.assertEqual(len(mod.inspect_db(self.folder / "naive.sqlite", False)[0]), 2)
        self.assertEqual(len(mod.inspect_db(self.folder / "guarded.sqlite", True)[0]), 1)
        with redirect_stdout(io.StringIO()) as out:
            mod.capture(self.folder, 0)
        self.assertIn("NOT recording of the original INSERT", out.getvalue())
        self.assertIn("concurrency NOT tested", out.getvalue())

    def test_refuse_receipt_tampering(self):
        p = self.folder / "replay_evidence.json"
        r = json.loads(p.read_text())
        r["guarded"]["new_actions"] = 2
        p.write_text(json.dumps(r))
        with self.assertRaisesRegex(ValueError, "POLICY_BLOCKED"):
            mod.verify_receipt(self.folder)

    def test_refuse_mutated_sqlite_db(self):
        with sqlite3.connect(self.folder / "guarded.sqlite") as con:
            con.execute("DELETE FROM actions")
        with self.assertRaisesRegex(ValueError, "POLICY_BLOCKED"):
            mod.inspect_db(self.folder / "guarded.sqlite", True)

    def test_refuse_removed_unique_index(self):
        with sqlite3.connect(self.folder / "guarded.sqlite") as con:
            con.execute("DROP INDEX idx_actions_event_key")
        with self.assertRaisesRegex(ValueError, "POLICY_BLOCKED"):
            mod.inspect_db(self.folder / "guarded.sqlite", True)

if __name__ == "__main__":
    unittest.main()
