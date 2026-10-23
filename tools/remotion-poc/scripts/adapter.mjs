/** Constrained NINFA manifest adapter: all results must remain REVIEW_ONLY. */
export const normalize = function(kind,m,r){
 const requireGate=(x,msg)=>{if(!x)throw new Error("POLICY_BLOCKED: "+msg)};
 requireGate(["cache","webhook","automation"].includes(kind),"unknown scene");
 const base={kind,channel:"DoesItAutomate",language:"en",reviewOnly:true,releaseState:"BLOCKED",safeZone:{top:220,bottom:350,side:85}};
 if(kind==="cache"){
  requireGate(m.schema==="ninfa-scene-v1.4.0"&&m.mode==="EVIDENCE_BACKED"&&m.family==="cache_race"&&m.brand==="DoesItAutomate"&&m.language==="en","cache identity");
  requireGate(m.format?.width===1080&&m.format?.height===1920&&m.format?.fps===30&&m.format?.frames===180,"cache media");
  requireGate(m.policy?.paid_api_usd===0&&m.policy?.github_actions===false&&m.policy?.publish_authority==="NONE"&&m.policy?.allow_raw_voice===false,"cache authority");
  requireGate(m.evidence?.source==="NINFA/docs/contracts/decisions/MOTION_V1_3_LOCAL_FINISHING_2026-10-08.md"&&m.evidence?.measurements?.fresh_s===4.8&&m.evidence?.measurements?.cached_s===1.15,"cache factual integrity");
  return {...base,title:"THE CACHE TEST",subtitle:"ONE LOCAL HOST",source:"NINFA Motion v1.3 receipt",disclosure:"4.80s versus 1.15s measured once; not universal",metrics:["4.80s","1.15s"],labels:["FRESH","CACHED"]};
 }
 if(kind==="webhook"){
  requireGate(m.schema==="ninfa-motion-v1.5"&&m.family==="event_replay"&&m.status==="EVIDENCE_BACKED_LOCAL"&&m.brand==="DoesItAutomate"&&m.language==="en","webhook identity");
  requireGate(m.format?.width===1080&&m.format?.height===1920&&m.format?.fps===30&&m.format?.frames===720,"webhook media");
  requireGate(m.rules?.paid_api_usd===0&&m.rules?.media_actions===false&&m.rules?.publish_authority==="NONE"&&m.rules?.raw_voice_in_git===false,"webhook authority");
  requireGate(r?.schema==="local-replay-v1"&&r.experimental_mode==="LOCAL_SYNTHETIC_SEQUENTIAL"&&r.sha256_content===m.evidence_sha256,"webhook evidence");
  requireGate(r.naive?.attempts===2&&r.naive?.new_actions===2&&r.guarded?.attempts===2&&r.guarded?.new_actions===1&&r.limitations?.includes("no concurrent delivery"),"webhook measured limits");
  requireGate(m.headlines?.includes("CONCURRENCY NOT TESTED"),"must disclose no concurrency");
  return {...base,title:"DUPLICATE WEBHOOK",subtitle:"SYNTHETIC SQLITE REPLAY",source:"NINFA Motion v1.5 replay",disclosure:"Sequential synthetic test; no concurrency claim",metrics:["2 ACTIONS","1 ACTION"],labels:["NO UNIQUE KEY","WITH UNIQUE KEY"]};
 }
 requireGate(m.id==="short-2026-10-02-cross-app-fragmentation"&&m.evidence?.benchmark==="AutomationBench public archived run"&&m.evidence?.task==="sales.full_sales_cycle_orchestrator"&&m.evidence?.model_run==="Qwen3.6-27B base","archived benchmark lineage");
 requireGate(m.evidence?.score===0.25&&m.evidence?.assertions_passed===2&&m.evidence?.assertions_total===8&&m.evidence?.tool_calls===29&&m.evidence?.steps===11,"archived results");
 requireGate(m.format?.width===1080&&m.format?.height===1920&&m.audio?.language==="en-us"&&m.brand?.canonical_logo_only===true,"archived media");
 return {...base,title:"TOOL CALL ≠ WORKFLOW",subtitle:"ARCHIVED THIRD-PARTY BENCHMARK",source:"AutomationBench / Qwen3.6-27B base",disclosure:"Public third-party run; not a NINFA run",metrics:["2 / 8","29"],labels:["CHECKS PASSED","TOOL CALLS"]};
};
