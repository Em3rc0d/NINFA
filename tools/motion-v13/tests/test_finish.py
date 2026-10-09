import copy
import importlib.util
import json
import tempfile
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
        self.changed(lambda x: x['captions'][1].update(text=r'{\\pos(20,30)}HACK'))

    def test_reject_bad_framerate(self):
        self.changed(lambda x: x.update(fps=29))

    def test_reject_oversized_duration(self):
        self.changed(lambda x: x.update(duration_frames=1801))

    def test_manifest_hash_changes_with_subtitles(self):
        a = copy.deepcopy(BASE)
        b = copy.deepcopy(BASE)
        b['captions'][0]['text'] += ' different'
        self.assertNotEqual(MOD.manifest_digest(a), MOD.manifest_digest(b))

    def test_cache_requires_exact_source_hashes(self):
        with tempfile.TemporaryDirectory() as dirname:
            out = pathlib.Path(dirname)
            video = out / (BASE['id'] + '.mp4')
            video.write_bytes(b'synthetic bytes for cache unit test')
            plan = {'visual_sha256': 'a', 'voice_sha256': 'b',
                    'manifest_sha256': MOD.manifest_digest(BASE), 'frames': BASE['duration_frames']}
            receipt = {**plan, 'status': 'TECHNICAL_PASS_REVIEW_ONLY', 'release_state': 'BLOCKED',
                       'output_sha256': MOD.digest(video)}
            (out / 'receipt.json').write_text(json.dumps(receipt))
            self.assertTrue(MOD.cache_hit(out, BASE['id'], plan)['cache_hit'])
            self.assertIsNone(MOD.cache_hit(out, BASE['id'], {**plan, 'voice_sha256': 'changed'}))
            self.assertIsNone(MOD.cache_hit(out, BASE['id'], {**plan, 'manifest_sha256': 'changed'}))
            video.write_bytes(b'tampered file')
            self.assertIsNone(MOD.cache_hit(out, BASE['id'], plan))

    def test_ass_rounding(self):
        self.assertEqual(MOD.ass_stamp(30), '0:00:01.00')

if __name__ == '__main__':
    unittest.main()
