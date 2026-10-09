import copy
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('motion_v13', ROOT / 'finish.py')
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
BASE = json.loads((ROOT / 'fixtures' / 'dia01.review.json').read_text('utf-8'))

class ContractTests(unittest.TestCase):
    def changed(self, func):
        x = copy.deepcopy(BASE)
        func(x)
        with self.assertRaises(ValueError):
            MOD.check_input(x)

    def test_approved_manifest(self):
        self.assertEqual(MOD.check_input(copy.deepcopy(BASE))['id'], 'dia01-review-v13')

    def test_ass_rounding(self):
        self.assertEqual(MOD.ass_stamp(30), '0:00:01.00')

    def test_reject_other_language(self):
        self.changed(lambda x: x.update(language='es'))

    def test_reject_other_brand(self):
        self.changed(lambda x: x.update(channel='EMERCOD'))

    def test_reject_paid_api(self):
        self.changed(lambda x: x.update(paid_api_usd=1))

    def test_reject_actions(self):
        self.changed(lambda x: x.update(github_actions_for_media=True))

    def test_reject_publishing(self):
        self.changed(lambda x: x.update(publish_authority='ALLOW'))

    def test_reject_unknown_fields(self):
        self.changed(lambda x: x.update(secret_audio_url='http://example.com'))

    def test_reject_unsupported_tts(self):
        self.changed(lambda x: x.update(narration_source='PIPER'))

    def test_reject_evidence_mode_not_implemented(self):
        self.changed(lambda x: x.update(mode='EVIDENCE_BACKED'))

    def test_reject_caption_overlap(self):
        self.changed(lambda x: x['captions'][1].update(start_frame=20))

    def test_reject_caption_injection(self):
        self.changed(lambda x: x['captions'][1].update(text=r'{\pos(20,30)}HACK'))

    def test_reject_bad_framerate(self):
        self.changed(lambda x: x.update(fps=29))

    def test_reject_oversized_duration(self):
        self.changed(lambda x: x.update(duration_frames=1801))

if __name__ == '__main__':
    unittest.main()
