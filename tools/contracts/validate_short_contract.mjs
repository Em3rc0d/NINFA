#!/usr/bin/env node
/**
 * Does It Automate? Shorts contract v1 semantic validator.
 * Node builtins only, zero network / paid APIs / Actions required.
 * Usage: node tools/contracts/validate_short_contract.mjs docs/contracts/fixtures/pv-poc-006.reference.json
 * Companion schema: docs/contracts/shorts-motion-v1.schema.json
 * This validator cannot prove visual claims, English pronunciation, media rights or platform UI overlays.
 */
import { readFileSync } from "node:fs";

export function validate(m) {
  const errors=[];
  const require=(ok,msg)=>{if(!ok)errors.push(msg)};
  const isObj=x=>x!==null && typeof x==="object" && !Array.isArray(x);
  require(isObj(m),"manifest must be an object");
  if(!isObj(m))return errors;
  require(m.schema_version==="1.0.0","schema_version must be 1.0.0");
  require(m.channel==="DoesItAutomate","channel must be DoesItAutomate");
  require(typeof m.artifact_id==="string" && m.artifact_id.length>=3,"artifact_id missing");
  const content=isObj(m.content)?m.content:{};
  require(["ILLUSTRATIVE_POC","EVIDENCE_BACKED","MIXED_LABELED"].includes(content.mode),"invalid content mode");
  require(content.language==="en","content must be English");
  require(typeof content.headline==="string"&&content.headline.trim().length>0,"headline missing");
  require(Array.isArray(content.evidence_refs),"evidence_refs must be an array");
  if(content.mode!=="ILLUSTRATIVE_POC")require(Array.isArray(content.evidence_refs)&&content.evidence_refs.length>0,"real/mixed content needs at least one evidence reference");
  if(content.mode==="MIXED_LABELED"||content.mode==="ILLUSTRATIVE_POC")require(typeof content.mock_disclosure==="string"&&content.mock_disclosure.trim().length>0,"illustrative material requires explicit DEMO disclosure");
  const visual=isObj(m.visual)?m.visual:{};
  require(visual.style_profile==="DIA_DARK_TECH_V1","style profile mismatch");
  require(typeof visual.direction_accepted==="boolean","visual direction accepted must be explicit");
  require(["NOT_EMBEDDED","CANONICAL_OWNER_ASSET_VERIFIED","UNVERIFIED"].includes(visual.logo_state),"logo_state invalid");
  const fmt=isObj(m.format)?m.format:{};
  for(const k of ["width","height","fps","duration_frames"])require(Number.isInteger(fmt[k])&&fmt[k]>0,`invalid format.${k}`);
  if(Number.isInteger(fmt.width)&&Number.isInteger(fmt.height))require(fmt.width<=fmt.height && fmt.width>=720,"short portrait canvas must be >=720 wide");
  if(Number.isInteger(fmt.fps))require(fmt.fps>=24 && fmt.fps<=60,"fps must be 24..60");
  require(fmt.video_codec==="h264","video codec must be h264");
  require(["aac","none"].includes(fmt.audio_codec),"audio codec invalid");
  const N=Number.isInteger(fmt.duration_frames)?fmt.duration_frames:0;
  const beats=Array.isArray(visual.beats)?visual.beats:[];
  require(beats.length>=3,"requires >=3 meaningful beats");
  let prior=0, distinct=[];
  for(let i=0;i<beats.length;i++){
    const b=beats[i];
    if(!isObj(b)){errors.push(`beat ${i} malformed`);continue}
    require(Number.isInteger(b.start_frame)&&Number.isInteger(b.end_frame)&&b.start_frame===prior&&b.end_frame>b.start_frame&&b.end_frame<=N,`beat ${i} frame ordering/bounds mismatch`);
    require(typeof b.from_state==="string"&&b.from_state.trim().length>0&&typeof b.to_state==="string"&&b.to_state.trim().length>0&&b.from_state!==b.to_state,`beat ${i} must change state`);
    require(typeof b.purpose==="string"&&b.purpose.trim().length>=5,`beat ${i} must state its purpose`);
    prior=b.end_frame;
    distinct.push(b.to_state);
  }
  require(prior===N,"beats must cover exact duration");
  require(new Set(distinct).size>=3,"beats must show at least three different output states");
  const narration=isObj(m.narration)?m.narration:{};
  require(["OWNER_HUMAN","LOCAL_CHATTERBOX","LOCAL_KOKORO","NONE"].includes(narration.source),"unsupported narration source");
  require(narration.language==="en","narration language must be English");
  require(narration.reference_storage==="PRIVATE_LOCAL","narration references must remain private/local");
  require(narration.owner_permission===true,"owner consent/permission must be explicit");
  if(narration.source==="NONE")require(narration.audio_embedded===false && fmt.audio_codec==="none","silent format must not embed audio");
  else require(narration.audio_embedded===true && fmt.audio_codec==="aac","narrated formats require AAC audio");
  const captions=isObj(m.captions)?m.captions:{};
  require(captions.language==="en","captions must be English");
  require(["POC_UNVERIFIED","MEASURED_FOR_DESTINATION"].includes(captions.safe_zone_profile),"safe-area status invalid");
  const marg=isObj(captions.margins_px)?captions.margins_px:{};
  for(const k of ["top","bottom","left","right"])require(Number.isInteger(marg[k])&&marg[k]>=0,`invalid margin.${k}`);
  if(Number.isInteger(fmt.width)&&Number.isInteger(fmt.height)&&Object.values(marg).every(Number.isInteger))
    require(marg.left+marg.right<fmt.width&&marg.top+marg.bottom<fmt.height,"safe-area margins must leave content space");
  const cap=Array.isArray(captions.intervals)?captions.intervals:[];
  if(narration.source!=="NONE")require(cap.length>0,"narrated video needs captions");
  let previousCaptionEnd=0;
  for(let i=0;i<cap.length;i++){
    const v=cap[i];
    if(!isObj(v)){errors.push(`caption ${i} malformed`);continue;}
    require(Number.isInteger(v.start_frame)&&Number.isInteger(v.end_frame)&&v.start_frame>=previousCaptionEnd&&v.end_frame>v.start_frame&&v.end_frame<=N,`caption ${i} timing invalid`);
    require(typeof v.text==="string"&&v.text.trim().length>0&&v.text.split("\n").length<=2,`caption ${i} text missing or too many lines`);
    previousCaptionEnd=v.end_frame;
  }
  const budget=isObj(m.budget)?m.budget:{};
  require(budget.paid_api_usd===0,"paid API budget forbidden");
  require(budget.github_actions_for_media===false,"GitHub Actions media production forbidden");
  const qa=isObj(m.qa)?m.qa:{};
  for(const k of ["technical","human_editorial","brand","platform_safe_area","rights","audio_captions"])require(["PASS","PENDING","FAIL"].includes(qa[k]),`invalid QA gate ${k}`);
  const dist=isObj(m.distribution)?m.distribution:{};
  require(["BLOCKED","READY_FOR_HUMAN_REVIEW","APPROVED_FOR_EXPORT"].includes(dist.approval_state),"invalid distribution approval state");
  require(dist.publish_authority==="NONE","renderer has no publishing authority");
  require(dist.provider_receipt===null,"provider receipt belongs to a separate workflow");
  require(dist.human_release_approval_ref===null || (typeof dist.human_release_approval_ref==="string" && dist.human_release_approval_ref.trim().length>0),"invalid human release receipt");
  if(typeof m.output_sha256!=="undefined"&&m.output_sha256!==null)require(typeof m.output_sha256==="string"&&/^[0-9a-f]{64}$/.test(m.output_sha256),"output hash malformed");
  if(qa.technical==="PASS")require(typeof m.output_sha256==="string"&&/^[0-9a-f]{64}$/.test(m.output_sha256),"technical PASS needs an output hash");
  if(content.mode==="ILLUSTRATIVE_POC")require(dist.approval_state==="BLOCKED","illustrative POC must stay blocked from export");
  if(dist.approval_state==="APPROVED_FOR_EXPORT"){
    require(content.mode!=="ILLUSTRATIVE_POC","POC is not publishable");
    require(visual.direction_accepted===true,"creative direction not approved");
    require(visual.logo_state!=="UNVERIFIED","logo must be canonical/verified or omitted");
    require(captions.safe_zone_profile==="MEASURED_FOR_DESTINATION","platform safe zone not verified");
    for(const k of ["technical","human_editorial","brand","platform_safe_area","rights","audio_captions"])require(qa[k]==="PASS",`release blocked by QA gate ${k}`);
    require(typeof dist.human_release_approval_ref==="string" && dist.human_release_approval_ref.trim().length>0,"export requires human release approval reference");
  }
  return errors;
}

if (process.argv[1] && /validate_short_contract\.mjs$/.test(process.argv[1])) {
  const path=process.argv[2];
  if (!path) { console.error("Usage: node validate_short_contract.mjs <manifest.json>"); process.exit(2); }
  try {
    const manifest=JSON.parse(readFileSync(path,"utf8"));
    const errors=validate(manifest);
    if(errors.length) { console.error(JSON.stringify({status:"BLOCKED",errors},null,2)); process.exit(1); }
    console.log(JSON.stringify({status:"CONTRACT_VALID",release:manifest.distribution.approval_state,human_qa:manifest.qa.human_editorial},null,2));
  }catch(err){console.error(JSON.stringify({status:"BLOCKED",error:String(err.message)},null,2));process.exit(1);}
}
