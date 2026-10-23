import {load} from './sources.mjs';
import {resolve,dirname,join,sep,isAbsolute} from 'node:path';
import {fileURLToPath} from 'node:url';
import {existsSync,mkdirSync,mkdtempSync,rmSync,readFileSync,writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {performance} from 'node:perf_hooks';
import {chooseAvailablePort} from './render-port.mjs';
import {buildRenderCommand} from './render-command.mjs';
import {validateWebhookStoryboard} from './validate-webhook-storyboard.mjs';

const app=resolve(dirname(fileURLToPath(import.meta.url)),'..'),root=resolve(app,'../..');
const [kind,outArg]=process.argv.slice(2);
const compositions={cache:'CacheRace',webhook:'WebhookReplay',automation:'AutomationFailure','cache-v2':'CacheRaceV2','webhook-v2':'WebhookReplayV2','automation-v2':'AutomationFailureV2','webhook-v3':'WebhookReplayV3'};
if(!Object.hasOwn(compositions,kind)||!outArg||!isAbsolute(outArg)||!outArg.toLowerCase().endsWith('.mp4')){
 throw new Error('Usage: node scripts/render.mjs cache|webhook|automation|cache-v2|webhook-v2|automation-v2|webhook-v3 /absolute/private/output.mp4');
}
const out=resolve(outArg);
if(out.startsWith(root+sep))throw new Error('POLICY_BLOCKED: media output inside Git repository');
if(existsSync(out))throw new Error('POLICY_BLOCKED: output already exists; choose a fresh name');
const sourceKind=kind.endsWith('-v2')||kind.endsWith('-v3')?kind.slice(0,-3):kind;
const props=load(sourceKind);
let v3Plan=null;
if(kind==='webhook-v3'){
 v3Plan=JSON.parse(readFileSync(join(app,'storyboards','webhook-v3.json'),'utf8'));
 const receipt=JSON.parse(readFileSync(join(root,'tools','motion-v15','evidence','replay_evidence.json'),'utf8'));
 validateWebhookStoryboard(v3Plan,props,receipt);
}
if(props.releaseState!=='BLOCKED'||props.reviewOnly!==true)throw new Error('POLICY_BLOCKED: release authority');
const cliEntry=join(app,'node_modules','@remotion','cli','remotion-cli.js');
if(!existsSync(cliEntry))throw new Error('Remotion CLI not installed locally. Run npm install in tools/remotion-poc.');
mkdirSync(dirname(out),{recursive:true});
const tmp=mkdtempSync(join(tmpdir(),'ninfa-remotion-'));
try{
 const propFile=join(tmp,'props.json');writeFileSync(propFile,JSON.stringify(props));
 const started=performance.now();
 const renderPort=await chooseAvailablePort();
 // Explicitly isolate the rendering server from a running Remotion Studio (usually :3000).
 // This port is allocated by the OS; never assume Studio is stopped or 3001 is free.
 console.log('NINFA Remotion: selected separate render port '+renderPort+' (Studio may remain open).');
 const command=buildRenderCommand({app,composition:compositions[kind],output:out,propsFile:propFile,port:renderPort});
 const render=spawnSync(command.executable,command.args,command.options);
 if(render.error||render.status!==0)throw new Error('RENDER_FAILED: '+(render.error?.message||render.status));
 const elapsed_ms=Math.round(performance.now()-started);
 const probe=spawnSync('ffprobe',['-v','error','-count_frames','-show_entries','stream=codec_type,codec_name,width,height,nb_read_frames,r_frame_rate','-of','json',out],{encoding:'utf8'});
 if(probe.error||probe.status!==0)throw new Error('FFPROBE_FAILED');
 const streams=JSON.parse(probe.stdout).streams||[];
 const v=streams.find(s=>s.codec_type==='video');
 const expected=sourceKind==='webhook'?720:180;
 if(!v||v.codec_name!=='h264'||v.width!==1080||v.height!==1920||Number(v.nb_read_frames)!==expected||v.r_frame_rate!=='30/1'||streams.some(s=>s.codec_type==='audio')){
  throw new Error('POLICY_BLOCKED: unexpected frames, codec, fps or audio');
 }
 const sha=(v)=>createHash('sha256').update(v).digest('hex');
 const receipt={
  experiment:kind,frames:expected,fps:30,width:1080,height:1920,elapsed_ms,
  ...(v3Plan?{storyboard_sha256:sha(readFileSync(join(app,'storyboards','webhook-v3.json'))),shot_count:v3Plan.shots.length}:{}),
  video_sha256:sha(readFileSync(out)),props_sha256:sha(JSON.stringify(props)),
  release_state:'BLOCKED',publish_authority:'NONE',
  benchmark_note:'No same-host baseline was executed by this command'
 };
 writeFileSync(out+'.review.json',JSON.stringify(receipt,null,2)+'\n');
 console.log(JSON.stringify(receipt,null,2));
}finally{rmSync(tmp,{force:true,recursive:true})}
