#!/usr/bin/env node
/** Offline contract QA. No cloud services or third-party dependencies. */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { validate } from "./validate_short_contract.mjs";

const baseline = JSON.parse(readFileSync(new URL("../../docs/contracts/fixtures/pv-poc-006.reference.json", import.meta.url), "utf8"));
const clone = () => structuredClone(baseline);
const cases = [
  ["baseline: illustrative demo remains blocked", null, true],
  ["reject Spanish speech", m=>{m.narration.language="es"}, false],
  ["reject Spanish captions", m=>{m.captions.language="es"}, false],
  ["reject other channel", m=>{m.channel="ContentSeller"}, false],
  ["reject paid API use", m=>{m.budget.paid_api_usd=1}, false],
  ["reject Actions for media render", m=>{m.budget.github_actions_for_media=true}, false],
  ["reject public raw voice reference", m=>{m.narration.reference_storage="PUBLIC_GITHUB"}, false],
  ["reject missing owner consent", m=>{m.narration.owner_permission=false}, false],
  ["reject unsupported TTS voice engine", m=>{m.narration.source="PIPER"}, false],
  ["reject overlapping beats", m=>{m.visual.beats[1].start_frame=35}, false],
  ["reject static fake state transition", m=>{m.visual.beats[2].to_state=m.visual.beats[2].from_state}, false],
  ["reject out-of-range captions", m=>{m.captions.intervals.at(-1).end_frame=500}, false],
  ["reject illusory result approved for export", m=>{m.distribution.approval_state="APPROVED_FOR_EXPORT"}, false],
  ["reject missing real evidence", m=>{m.content.mode="EVIDENCE_BACKED";m.content.mock_disclosure=null;m.distribution.approval_state="READY_FOR_HUMAN_REVIEW"}, false],
  ["reject exporter with pending QA", m=>{m.content.mode="EVIDENCE_BACKED";m.content.evidence_refs=["evidence://verified-test"];m.content.mock_disclosure=null;m.distribution.approval_state="APPROVED_FOR_EXPORT"}, false],
  ["reject spoofed provider receipt", m=>{m.distribution.provider_receipt="posted!"}, false],
  ["allow fully approved evidence-backed export (still no publishing authority)", m=>{
    m.content.mode="EVIDENCE_BACKED";
    m.content.evidence_refs=["evidence://verified-test"];
    m.content.mock_disclosure=null;
    m.distribution.approval_state="APPROVED_FOR_EXPORT";
    m.distribution.human_release_approval_ref="approval://human-review-001";
    m.captions.safe_zone_profile="MEASURED_FOR_DESTINATION";
    for(const k of Object.keys(m.qa))m.qa[k]="PASS";
  }, true],
];
let passed=0;
for(const [name,mutate,expected] of cases){
  const m=clone();
  if(mutate)mutate(m);
  const errors=validate(m);
  assert.equal(errors.length===0,expected, name+": "+errors.join("; "));
  passed++;
  console.log("PASS "+name);
}
console.log("PASS total "+passed+"/"+cases.length+"; no GitHub Actions used");
