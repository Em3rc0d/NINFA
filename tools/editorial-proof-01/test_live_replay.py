"""Checks the live captured operations and their canonical receipt (stdlib only)."""
from contextlib import closing, redirect_stdout
import importlib.util
import io
from pathlib import Path
import sqlite3
import tempfile
import unittest

SOURCE = Path(__file__).with_name("live_replay.py")
spec = importlib.util.spec_from_file_location("ninfa_editorial_live_replay", SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class LiveReplayTests(unittest.TestCase):
    def test_real_inserts_match_source_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            with redirect_stdout(io.StringIO()) as output:
                proof = mod.run_live(Path(directory) / "shot", 0)
            self.assertEqual(proof["sha256_content"], mod.CANONICAL_SHA)
            self.assertEqual(proof["naive"]["new_actions"], 2)
            self.assertEqual(proof["guarded"]["new_actions"], 1)
            self.assertIn("DUPLICATE SKIPPED", output.getvalue())
            for label, expected in (("naive", 2), ("guarded", 1)):
                path = Path(directory) / "shot" / (label + ".sqlite")
                with closing(sqlite3.connect(path)) as con:
                    count = con.execute("SELECT COUNT(*) FROM actions").fetchone()[0]
                self.assertEqual(count, expected)

    def test_no_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "POLICY_BLOCKED"):
                mod.run_live(Path(directory), 0)

    def test_invalid_pause_rejected_before_creating_output(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "shot"
            with self.assertRaisesRegex(ValueError, "POLICY_BLOCKED"):
                mod.run_live(path, 6)
            self.assertFalse(path.exists())

    def test_disclaims_provider_and_concurrency(self):
        with tempfile.TemporaryDirectory() as directory:
            with redirect_stdout(io.StringIO()) as output:
                receipt = mod.run_live(Path(directory) / "shot", 0)
            self.assertIn("Concurrency NOT tested", output.getvalue())
            self.assertIn("no concurrent delivery", receipt["limitations"])
            self.assertFalse(receipt["published"])
            self.assertEqual(receipt["api_spend_usd"], 0)

if __name__ == "__main__":
    unittest.main()
