import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('local_lab',ROOT/'replay_lab.py');lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)
spec=importlib.util.spec_from_file_location('studio',ROOT/'studio.py');studio=importlib.util.module_from_spec(spec);spec.loader.exec_module(studio)
STORY=json.loads((ROOT/'story.json').read_text())
PROOF=json.loads((ROOT/'evidence/replay_evidence.json').read_text())

class EvidenceTests(unittest.TestCase):
    def test_valid_proof(self):self.assertEqual(studio.check_proof(copy.deepcopy(PROOF))['guarded']['new_actions'],1)
    def test_local_replay_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=lab.generate(Path(tmp)/'a');b=lab.generate(Path(tmp)/'b')
            self.assertEqual(a['sha256_content'],b['sha256_content'])
            self.assertEqual(a['sha256_content'],PROOF['sha256_content'])
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'same.sqlite';lab.run_case(path,False)
            with self.assertRaises(ValueError):lab.run_case(path,False)
    def test_naive_two_actions(self):self.assertEqual(PROOF['naive']['new_actions'],2)
    def test_guarded_one_action(self):self.assertEqual(PROOF['guarded']['inserted'],[True,False])
    def bad_proof(self,mutate,rehash=False):
        p=copy.deepcopy(PROOF);mutate(p)
        if rehash:
            import hashlib
            q=dict(p);q.pop('sha256_content');p['sha256_content']=hashlib.sha256(studio.canonical(q).encode()).hexdigest()
        with self.assertRaises(ValueError):studio.check_proof(p)
    def test_tampered_counts(self):self.bad_proof(lambda p:p['guarded'].update(new_actions=7))
    def test_forged_rehashed_count(self):self.bad_proof(lambda p:p['guarded'].update(new_actions=7),True)
    def test_forged_external_claim(self):self.bad_proof(lambda p:p.update(experimental_mode='LIVE_WEBHOOK'),True)
    def test_forged_paid_api(self):self.bad_proof(lambda p:p.update(api_spend_usd=1),True)
    def test_forged_published(self):self.bad_proof(lambda p:p.update(published=True),True)

class StoryTests(unittest.TestCase):
    def test_story_valid(self):self.assertIsNotNone(studio.check_story(copy.deepcopy(STORY),PROOF))
    def bad(self,mutate):
        s=copy.deepcopy(STORY);mutate(s)
        with self.assertRaises(ValueError):studio.check_story(s,PROOF)
    def test_language_gate(self):self.bad(lambda s:s.update(language='es'))
    def test_brand_gate(self):self.bad(lambda s:s.update(brand='EMERCOD'))
    def test_paid_api_gate(self):self.bad(lambda s:s['rules'].update(paid_api_usd=1))
    def test_actions_gate(self):self.bad(lambda s:s['rules'].update(media_actions=True))
    def test_publish_gate(self):self.bad(lambda s:s['rules'].update(publish_authority='YES'))
    def test_public_voice_gate(self):self.bad(lambda s:s['rules'].update(raw_voice_in_git=True))
    def test_wrong_evidence(self):self.bad(lambda s:s.update(evidence_sha256='0'*64))
    def test_unknown_key(self):self.bad(lambda s:s.update(remote_text='unsafe'))
    def test_oversized_headline(self):self.bad(lambda s:s['headlines'].__setitem__(0,'X'*39))
    def test_caption_overlap(self):self.bad(lambda s:s['caption_plan'][2].update(start_frame=50))
    def test_caption_injection(self):self.bad(lambda s:s['caption_plan'][0].update(text=r'{\\pos(0,0)}evil'))
    def test_empty_voice_script(self):self.bad(lambda s:s.update(voice_script=''))
    def test_wrong_frame_count(self):self.bad(lambda s:s['format'].update(frames=300))
    def test_temporal_variation(self):
        xs=[studio.frame(STORY,PROOF,i).resize((90,160)).tobytes() for i in (0,60,180,360,540,719)]
        self.assertEqual(len(set(xs)),len(xs))

if __name__=='__main__':unittest.main()
