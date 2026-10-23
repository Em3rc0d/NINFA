"""No-inference regression tests for the opt-in Kokoro voice audition."""
import importlib.util
import pathlib
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ninfa_voice_ab_kokoro", HERE / "voice_ab_kokoro.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class VoiceABTests(unittest.TestCase):
    def test_dry_run_needs_no_tts_installation(self):
        with tempfile.TemporaryDirectory() as tmp:
            candidate = pathlib.Path(tmp) / "sample"
            receipt = mod.preview(candidate, True)
            self.assertFalse(candidate.exists())
            self.assertEqual(receipt["status"], "PREFLIGHT_ONLY")
            self.assertEqual(len(receipt["voices"]), 2)
            self.assertFalse(receipt["requires_reference_voice"])
            self.assertEqual(receipt["publish_authority"], "NONE")

    def test_refuse_out_directory_inside_repository(self):
        with self.assertRaisesRegex(ValueError, "POLICY_BLOCKED"):
            mod.preview(mod.REPO_ROOT / "private-narration", True)

    def test_refuse_existing_directory_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "POLICY_BLOCKED"):
                mod.preview(pathlib.Path(tmp), True)

    def test_voice_contract_does_not_misclaim_evidence(self):
        self.assertIn("synthetic", mod.AUDITION_SCRIPT)
        self.assertIn("Concurrency was not tested", mod.AUDITION_SCRIPT)
        self.assertEqual(mod.VOICES, ("am_michael", "af_heart"))

if __name__ == "__main__":
    unittest.main()
