#!/usr/bin/env node
/**
 * NINFA audience-learning: offline, manual YouTube Studio snapshots only.
 * No YouTube API, upload, publishing, billing or network request.
 */
import {readFileSync} from "node:fs";
import {resolve} from "node:path";
import {fileURLToPath} from "node:url";

export function validateMetrics(doc){
 const errors=[];
 if(!doc||doc.schema_version!=="1.0"||!Array.isArray(doc.videos))return {ok:false,errors:["Invalid analytics document"]};
 const ids=new Set();
 for(const [i,v] of doc.videos.entries()){
  const p=`videos[${i}]`;
  if(typeof v.local_key!=="string"||!v.local_key.trim()||ids.has(v.local_key))errors.push(`${p}: missing/duplicate local_key`);
  ids.add(v.local_key);
  if(!["SINCE_PUBLISHED","FIRST_48_HOURS","LAST_28_DAYS"].includes(v.window))errors.push(`${p}: invalid window`);
  if(v.source!=="MANUAL_YOUTUBE_STUDIO")errors.push(`${p}: unsupported provenance`);
  for(const k of ["views","engaged_views","unique_viewers","shown_in_feed","subscribers_gained"]){
   if(v[k]!==null && (!Number.isInteger(v[k])||v[k]<0))errors.push(`${p}: ${k} must be nonnegative integer or null`);
  }
  for(const k of ["stayed_to_watch_pct","shorts_feed_pct","youtube_search_pct","average_percentage_viewed"]){
   if(v[k]!==null && (typeof v[k]!=="number"||!Number.isFinite(v[k])||v[k]<0||v[k]>100))errors.push(`${p}: ${k} must be 0..100 or null`);
  }
  for(const k of ["duration_sec","average_view_duration_sec"]){
   if(v[k]!==null && (typeof v[k]!=="number"||!Number.isFinite(v[k])||v[k]<0))errors.push(`${p}: ${k} must be nonnegative or null`);
  }
  if(v.duration_sec===0)errors.push(`${p}: video duration must be positive`);
  if(Number.isInteger(v.views)&&Number.isInteger(v.engaged_views)&&v.engaged_views>v.views)errors.push(`${p}: engaged views exceed views`);
  if(typeof v.title!=="string"||!v.title.trim())errors.push(`${p}: missing title`);
 }
 return {ok:errors.length===0,errors};
}
export function analyzeMetrics(doc){
 const check=validateMetrics(doc);if(!check.ok)throw new Error(check.errors.join("\n"));
 return {as_of:doc.as_of,scope:"Observational; no causal ranking, no cross-window equivalence",videos:doc.videos.map(v=>{
  const hasRatio=v.duration_sec>0 && v.average_view_duration_sec!==null;
  const ratio=hasRatio?Math.round(v.average_view_duration_sec/v.duration_sec*1000)/10:null;
  return {local_key:v.local_key,title:v.title,window:v.window,views:v.views,engaged_views:v.engaged_views,stayed_to_watch_pct:v.stayed_to_watch_pct,estimated_conditional_duration_pct:ratio,shorts_feed_pct:v.shorts_feed_pct,alerts:[...(v.shown_in_feed===null?["MISSING_SHOWN_IN_FEED"]:[]),...(v.stayed_to_watch_pct===null?["MISSING_STAYED_TO_WATCH"]:[]),...(v.stayed_to_watch_pct!==null&&v.stayed_to_watch_pct<25?["LOW_INITIAL_HOLD_EXPERIMENTAL_THRESHOLD"]:[])],interpretation:"Descriptive observation only. Distribution cause unverified."};
 })};
}
export function validateBatch(doc){
 const errors=[];if(!doc||doc.schema_version!=="1.0"||!Array.isArray(doc.candidates))return {ok:false,errors:["Invalid batch"]};
 if(doc.candidates.length!==6)errors.push("Batch must have exactly six experiments");
 const ids=new Set(),angles=new Set(),incidents=new Set();
 const previous=new Set(doc.history_incident_keys||[]);
 for(const [i,c] of doc.candidates.entries()){
  const p=`candidates[${i}]`;
  for(const field of ["id","title","hook","angle_key","incident_key","pillar","experiment_plan","evidence_to_capture"]){
   if(typeof c[field]!=="string"||!c[field].trim())errors.push(`${p}: missing ${field}`);
  }
  if(ids.has(c.id)||angles.has(c.angle_key)||incidents.has(c.incident_key))errors.push(`${p}: duplicate ID/angle/incident`);
  ids.add(c.id);angles.add(c.angle_key);incidents.add(c.incident_key);
  if(previous.has(c.incident_key))errors.push(`${p}: previously published/planned incident collision`);
  if(!["BUILD_AUTOMATE","EXPERIMENT_STRESS","COMPARE_DECIDE","BUSINESS_ECONOMICS"].includes(c.pillar))errors.push(`${p}: invalid pillar`);
  if(!["NOT_RUN","VERIFIED_LOCAL","VERIFIED_EXTERNAL"].includes(c.evidence_state))errors.push(`${p}: invalid evidence_state`);
  if(!Array.isArray(c.result_claims)||!Array.isArray(c.evidence_refs))errors.push(`${p}: result_claims/evidence_refs must be arrays`);
  else {
   if(c.evidence_state==="NOT_RUN"&&(c.result_claims.length||c.evidence_refs.length))errors.push(`${p}: unrun experiment cannot claim results/evidence`);
   if(c.evidence_state!=="NOT_RUN"&&!c.evidence_refs.length)errors.push(`${p}: verified experiment requires evidence`);
  }
  if(c.release_status!=="BLOCKED_PENDING_EVIDENCE_AND_HUMAN_QA")errors.push(`${p}: cannot unlock publication`);
 }
 return {ok:errors.length===0,errors};
}

if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{
  const metricsPath=process.argv[2]||"experiments/audience-learning/studio-2026-10-30.json";
  const batchPath=process.argv[3]||"content/shorts/2026-10-30-learning-batch.json";
  const metrics=JSON.parse(readFileSync(resolve(metricsPath),"utf8"));
  const batch=JSON.parse(readFileSync(resolve(batchPath),"utf8"));
  const checked=validateBatch(batch);
  if(!checked.ok)throw new Error(checked.errors.join("\n"));
  process.stdout.write(JSON.stringify({analytics:analyzeMetrics(metrics),candidate_count:batch.candidates.length,editorial_gate:"ALL_BLOCKED_PENDING_EVIDENCE_AND_HUMAN_QA",candidate_ids:batch.candidates.map(c=>c.id)},null,2)+"\n");
 }catch(e){process.stderr.write(String(e)+"\n");process.exitCode=1}
}
