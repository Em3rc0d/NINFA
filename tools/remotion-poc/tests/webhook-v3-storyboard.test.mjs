import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {load,repo} from '../scripts/sources.mjs';
import {REQUIRED_SHOTS,validateWebhookStoryboard} from '../scripts/validate-webhook-storyboard.mjs';
const plan=JSON.parse(readFileSync(resolve(repo,'tools/remotion-poc/storyboards/webhook-v3.json'),'utf8'));
const receipt=JSON.parse(readFileSync(resolve(repo,'tools/motion-v15/evidence/replay_evidence.json'),'utf8'));
const props=load('webhook');
const clone=(obj)=>JSON.parse(JSON.stringify(obj));
test('V3 evidence and 7 precise 720-frame shots are accepted',()=>{
 const r=validateWebhookStoryboard(plan,props,receipt);
 assert.equal(r.frames,720);assert.equal(r.shotCount,7);
 assert.deepEqual(plan.shots.map(s=>s.id),REQUIRED_SHOTS);
});
test('every V3 frame belongs to precisely one visible shot',()=>{
 for(let f=0;f<720;f++){
  const active=plan.shots.filter(s=>f>=s.start&&f<s.end);
  assert.equal(active.length,1,'frame '+f);
 }
 for(let i=1;i<plan.shots.length;i++)assert.equal(plan.shots[i-1].end,plan.shots[i].start);
});
test('reject storyboard with overlapping titles/shots',()=>{
 const altered=clone(plan);altered.shots[2].start-=1;
 assert.throws(()=>validateWebhookStoryboard(altered,props,receipt),/POLICY_BLOCKED/);
});
test('reject removing concurrency disclaimer',()=>{
 const altered=clone(plan);altered.shots[6].headline='SAFE IN PRODUCTION.';
 assert.throws(()=>validateWebhookStoryboard(altered,props,receipt),/POLICY_BLOCKED/);
});
test('reject false concurrent evidence',()=>{
 const altered=clone(plan);altered.evidence.concurrencyTested=true;
 assert.throws(()=>validateWebhookStoryboard(altered,props,receipt),/POLICY_BLOCKED/);
});
test('reject escalation to export or cloud API',()=>{
 const altered=clone(plan);altered.authority.publishAuthority='AUTO';altered.authority.paidApisUsd=1;
 assert.throws(()=>validateWebhookStoryboard(altered,props,receipt),/POLICY_BLOCKED/);
});
test('reject receipts that do not match SQL results',()=>{
 const fake=clone(receipt);fake.guarded.new_actions=2;
 assert.throws(()=>validateWebhookStoryboard(plan,props,fake),/POLICY_BLOCKED/);
});
test('V3 CLI and component are present, V1/V2 remain in source',()=>{
 const root=readFileSync(resolve(repo,'tools/remotion-poc/src/Root.tsx'),'utf8');
 const scene=readFileSync(resolve(repo,'tools/remotion-poc/src/WebhookV3.tsx'),'utf8');
 assert.match(root,/WebhookReplayV3/);assert.match(root,/WebhookReplayV2/);
 assert.match(scene,/plan\.shots\.find\(/);
 assert.doesNotMatch(scene,/<Stage /);
});

import {sampleFrames,CUT_BOUNDARIES,SHOT_MIDPOINTS} from '../scripts/webhook-v3-samples.mjs';
test('visual QA samples seven beats plus both sides of all six cuts',()=>{
 const frames=sampleFrames();
 assert.equal(frames.length,19);
 assert.deepEqual(frames,[...new Set(frames)].sort((a,b)=>a-b));
 for(const n of SHOT_MIDPOINTS)assert.ok(frames.includes(n));
 for(const n of CUT_BOUNDARIES){assert.ok(frames.includes(n-1));assert.ok(frames.includes(n));}
});
test('the guarded visual makes a real DB write then blocks only the duplicate',()=>{
 const source=readFileSync(resolve(repo,'tools/remotion-poc/src/WebhookV3.tsx'),'utf8');
 assert.match(source,/const acceptedEnd=635/);
 assert.match(source,/const duplicateEnd=guarded\?510:635/);
 assert.match(source,/guarded\?P\.red:P\.cyan/);
});
