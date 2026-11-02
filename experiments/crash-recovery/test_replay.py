import importlib.util,json,subprocess,sys,tempfile,unittest
from pathlib import Path
P=Path(__file__).with_name('replay.py')
spec=importlib.util.spec_from_file_location('ninfa_s03',P)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class CrashRecoveryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.e=mod.evaluate(Path(self.tmp.name))
 def test_subprocess_really_crashed(self):
  self.assertEqual(self.e['modes']['naive']['first_process_exit_code'],27)
  self.assertEqual(self.e['modes']['checkpoint']['first_process_exit_code'],27)
 def test_after_restart_succeeds(self):
  self.assertEqual(self.e['modes']['naive']['second_process_exit_code'],0)
  self.assertEqual(self.e['modes']['checkpoint']['second_process_exit_code'],0)
 def test_naive_replays_first_two(self):
  self.assertEqual([x['step'] for x in self.e['modes']['naive']['actions']],['READ','VALIDATE','READ','VALIDATE','TRANSFORM','STORE'])
 def test_checkpoint_resumes_remaining(self):
  self.assertEqual([x['step'] for x in self.e['modes']['checkpoint']['actions']],list(mod.STEPS))
 def test_counts(self):
  self.assertEqual((self.e['modes']['naive']['action_count'],self.e['modes']['checkpoint']['action_count']),(6,4))
 def test_naive_has_two_repeated_actions(self):
  self.assertEqual(self.e['modes']['naive']['repeated_action_count'],2)
 def test_checkpoint_none_repeated(self):
  self.assertEqual(self.e['modes']['checkpoint']['repeated_action_count'],0)
 def test_local_guarantee_disclosed(self):
  self.assertTrue(self.e['boundary']['no_ai_model_tested'])
  self.assertTrue(self.e['boundary']['no_external_api_or_provider'])
 def test_no_publication_approval(self):
  self.assertFalse(self.e['publish_approved'])
 def test_canonical_digest_independent_of_disk(self):
  with tempfile.TemporaryDirectory() as other:
   x=mod.evaluate(other)
   self.assertEqual(x['sha256_canonical_core'],self.e['sha256_canonical_core'])
 def test_tamper_evidence_detected(self):
  orig=self.e['sha256_canonical_core'];tampered=json.loads(json.dumps(self.e));tampered['modes']['checkpoint']['action_count']=5
  import hashlib
  checksum=tampered.pop('sha256_canonical_core');self.assertNotEqual(hashlib.sha256(json.dumps(tampered,sort_keys=True,separators=(',',':')).encode()).hexdigest(),checksum)
 def test_worker_invalid_mode_rejected(self):
  p=subprocess.run([sys.executable,str(P),'worker','--db','foo','--mode','fabricated','--phase','1'],capture_output=True)
  self.assertNotEqual(p.returncode,0)
if __name__=='__main__':unittest.main()
