import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {normalize} from '../scripts/adapter.mjs';
import {load,allowed,repo} from '../scripts/sources.mjs';
const json=(p)=>JSON.parse(readFileSync(resolve(repo,p),'utf8'));
for(const kind of allowed)test(kind+' stays review-only with canonical source',()=>{
 const p=load(kind);assert.equal(p.releaseState,'BLOCKED');assert.equal(p.reviewOnly,true);assert.ok(p.disclosure);
});
test('reject unknown family',()=>assert.throws(()=>load('injected'),/POLICY_BLOCKED/));
test('reject cache falsification',()=>{
 const m=json('tools/motion-v14/fixtures/cache-proof.json');
 m.evidence.measurements.cached_s=0.001;
 assert.throws(()=>normalize('cache',m),/POLICY_BLOCKED/);
});
test('reject paid APIs',()=>{
 const m=json('tools/motion-v14/fixtures/cache-proof.json');
 m.policy.paid_api_usd=100;
 assert.throws(()=>normalize('cache',m),/POLICY_BLOCKED/);
});
test('reject webhook without concurrency disclaimer',()=>{
 const m=json('tools/motion-v15/story.json'),r=json('tools/motion-v15/evidence/replay_evidence.json');
 m.headlines=m.headlines.filter(x=>x!=='CONCURRENCY NOT TESTED');
 assert.throws(()=>normalize('webhook',m,r),/POLICY_BLOCKED/);
});
test('reject source receipt spoofing',()=>{
 const m=json('tools/motion-v15/story.json'),r=json('tools/motion-v15/evidence/replay_evidence.json');
 r.sha256_content='spoofed';
 assert.throws(()=>normalize('webhook',m,r),/POLICY_BLOCKED/);
});
test('reject forged public result',()=>{
 const m=json('content/shorts/2026-10-02-cross-app-fragmentation/scene_manifest.json');
 m.evidence.assertions_passed=8;
 assert.throws(()=>normalize('automation',m),/POLICY_BLOCKED/);
});
