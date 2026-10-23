import {load} from './sources.mjs';
import {resolve,dirname,join,sep,isAbsolute} from 'node:path';
import {fileURLToPath} from 'node:url';
import {existsSync,mkdirSync,mkdtempSync,rmSync,readFileSync,writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {performance} from 'node:perf_hooks';

const app=resolve(dirname(fileURLToPath(import.meta.url)),'..'),root=resolve(app,'../..');
const [kind,outArg]=process.argv.slice(2);
const compositions={cache:'CacheRace',webhook:'WebhookReplay',automation:'AutomationFailure'};
if(!Object.hasOwn(compositions,kind)||!outArg||!isAbsolute(outArg)||!outArg.toLowerCase().endsWith('.mp4')){
 throw new Error('Usage: node scripts/render.mjs cache|webhook|automation /absolute/private/output.mp4');
}
const out=resolve(outArg);
if(out.startsWith(root+sep))throw new Error('POLICY_BLOCKED: media output inside Git repository');
if(existsSync(out))throw new Error('POLICY_BLOCKED: output already exists; choose a fresh name');
const props=load(kind);
if(props.releaseState!=='BLOCKED'||props.reviewOnly!==true)throw new Error('POLICY_BLOCKED: release authority');
const binary=join(app,'node_modules','.bin',process.platform==='win32'?'remotion.cmd':'remotion');
if(!existsSync(binary))throw new Error('Remotion packages not installed locally. Run npm install in tools/remotion-poc.');
mkdirSync(dirname(out),{recursive:true});
const tmp=mkdtempSync(join(tmpdir(),'ninfa-remotion-'));
try{
 const propFile=join(tmp,'props.json');writeFileSync(propFile,JSON.stringify(props));
 const started=performance.now();
 const render=spawnSync(binary,['render',join(app,'src/index.ts'),compositions[kind],out,'--props='+propFile,'--codec=h264','--concurrency=2'],{cwd:app,stdio:'inherit',timeout:900000,shell:process.platform==='win32'});
 if(render.error||render.status!==0)throw new Error('RENDER_FAILED: '+(render.error?.message||render.status));
 const elapsed_ms=Math.round(performance.now()-started);
 const probe=spawnSync('ffprobe',['-v','error','-count_frames','-show_entries','stream=codec_type,codec_name,width,height,nb_read_frames,r_frame_rate','-of','json',out],{encoding:'utf8'});
 if(probe.error||probe.status!==0)throw new Error('FFPROBE_FAILED');
 const streams=JSON.parse(probe.stdout).streams||[];
 const v=streams.find(s=>s.codec_type==='video');
 const expected=kind==='webhook'?720:180;
 if(!v||v.codec_name!=='h264'||v.width!==1080||v.height!==1920||Number(v.nb_read_frames)!==expected||v.r_frame_rate!=='30/1'||streams.some(s=>s.codec_type==='audio')){
  throw new Error('POLICY_BLOCKED: unexpected frames, codec, fps or audio');
 }
 const sha=(v)=>createHash('sha256').update(v).digest('hex');
 const receipt={
  experiment:kind,frames:expected,fps:30,width:1080,height:1920,elapsed_ms,
  video_sha256:sha(readFileSync(out)),props_sha256:sha(JSON.stringify(props)),
  release_state:'BLOCKED',publish_authority:'NONE',
  benchmark_note:'No same-host baseline was executed by this command'
 };
 writeFileSync(out+'.review.json',JSON.stringify(receipt,null,2)+'\n');
 console.log(JSON.stringify(receipt,null,2));
}finally{rmSync(tmp,{force:true,recursive:true})}
