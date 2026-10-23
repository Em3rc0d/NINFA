import {realpathSync,readFileSync} from 'node:fs';
import {resolve,dirname,sep} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {normalize} from './adapter.mjs';
export const repo=resolve(dirname(fileURLToPath(import.meta.url)),'../../..');
const cases={cache:'tools/motion-v14/fixtures/cache-proof.json',webhook:'tools/motion-v15/story.json',automation:'content/shorts/2026-10-02-cross-app-fragmentation/scene_manifest.json'};
function read(p){
 const path=realpathSync(resolve(repo,p));
 if(!path.startsWith(repo+sep))throw new Error('POLICY_BLOCKED: source outside repository');
 return readFileSync(path,'utf8');
}
const loadJson=(p)=>JSON.parse(read(p));
function canonical(x){
 if(Array.isArray(x))return '['+x.map(canonical).join(',')+']';
 if(x&&typeof x==='object')return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}';
 return JSON.stringify(x);
}
export const allowed=Object.freeze(Object.keys(cases));
export function load(kind){
 if(!Object.hasOwn(cases,kind))throw new Error('POLICY_BLOCKED: unsupported composition');
 const m=loadJson(cases[kind]);
 if(kind==='cache'){
  const receipt=read('docs/contracts/decisions/MOTION_V1_3_LOCAL_FINISHING_2026-10-08.md');
  if(!receipt.includes('4.80')||!receipt.includes('1.15'))throw new Error('POLICY_BLOCKED: cache source receipt absent');
 }
 if(kind==='automation'){
  const ledger=read('content/video-003/FAILURE_REPLAYS.md').toLowerCase();
  for(const part of ['sales.full_sales_cycle_orchestrator','2 / 8','29','qwen3.6-27b base','not ninfa-owned']){
   if(!ledger.includes(part))throw new Error('POLICY_BLOCKED: missing public archive provenance: '+part);
  }
 }
 let r;
 if(kind==='webhook'){
  r=loadJson('tools/motion-v15/evidence/replay_evidence.json');
  const {sha256_content,...body}=r;
  if(createHash('sha256').update(canonical(body)).digest('hex')!==sha256_content)throw new Error('POLICY_BLOCKED: local evidence changed');
 }
 return normalize(kind,m,r);
}
