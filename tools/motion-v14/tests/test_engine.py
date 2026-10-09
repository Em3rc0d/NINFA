import copy,unittest,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import engine
P=Path(__file__).resolve().parents[1]/'fixtures'
base=json.loads((P/'cache-proof.json').read_text())
demo=json.loads((P/'breaker-demo.json').read_text())

class Contract(unittest.TestCase):
 def check_bad(self,fun,template=None):
  m=copy.deepcopy(template or base);fun(m)
  with self.assertRaises(ValueError):engine.validate(m)
 def test_all_three_valid(self):
  for p in P.glob('*.json'):
   with self.subTest(p=p.name):engine.validate(json.loads(p.read_text()))
 def test_brand(self):self.check_bad(lambda x:x.update(brand='EMERCOD'))
 def test_spanish(self):self.check_bad(lambda x:x.update(language='es'))
 def test_paid_api(self):self.check_bad(lambda x:x['policy'].update(paid_api_usd=1))
 def test_booleans_dont_pass_as_costs(self):self.check_bad(lambda x:x['policy'].update(paid_api_usd=False))
 def test_actions(self):self.check_bad(lambda x:x['policy'].update(github_actions=True))
 def test_publish(self):self.check_bad(lambda x:x['policy'].update(publish_authority='YES'))
 def test_raw_voice(self):self.check_bad(lambda x:x['policy'].update(allow_raw_voice=True))
 def test_other_module(self):self.check_bad(lambda x:x.update(family='arbitrary_js'))
 def test_unknown_key(self):self.check_bad(lambda x:x.update(external_url='https://bad.example'))
 def test_larger_video(self):self.check_bad(lambda x:x['format'].update(frames=400))
 def test_missing_provenance(self):self.check_bad(lambda x:x['evidence'].update(source=None))
 def test_fake_metric(self):self.check_bad(lambda x:x['evidence'].update(measurements={'fresh_s':0.2,'cached_s':0.1}))
 def test_false_evidence_promotion(self):self.check_bad(lambda x:x.update(mode='EVIDENCE_BACKED'),demo)
 def test_missing_demo_label(self):self.check_bad(lambda x:x['evidence'].update(disclosure='Illustration'),demo)
 def test_html_injection(self):self.check_bad(lambda x:x.update(message='<script>alert(1)</script>'))
 def test_frame_samples_vary(self):
  m=base;pixels=[engine.create_frame(m,i).resize((96,170)).tobytes() for i in [0,60,120,179]]
  self.assertEqual(len(set(pixels)),4)
 def test_module_outputs_are_distinct(self):
  s=[engine.create_frame(json.loads(p.read_text()),90).resize((96,170)).tobytes() for p in sorted(P.glob('*.json'))]
  self.assertEqual(len(set(s)),3)

if __name__=='__main__':unittest.main()
