import importlib.util,json,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('scene_review',BASE/'run_review.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
scene=json.loads((BASE/'fixtures/parallel-voice-demo.json').read_text())
finish=json.loads((BASE/'fixtures/finishing/parallel-v13-finish.review.json').read_text())
class Integration(unittest.TestCase):
 def test_valid(self):self.assertIsNone(mod.check_story(scene,finish))
 def test_frame_mismatch(self):
  altered=json.loads(json.dumps(finish));altered['duration_frames']=600
  with self.assertRaises(ValueError):mod.check_story(scene,altered)
 def test_language_mismatch(self):
  altered=json.loads(json.dumps(finish));altered['language']='es'
  with self.assertRaises(ValueError):mod.check_story(scene,altered)
 def test_publish_mismatch(self):
  altered=json.loads(json.dumps(finish));altered['publish_authority']='PUBLIC'
  with self.assertRaises(ValueError):mod.check_story(scene,altered)
if __name__=='__main__':unittest.main()
