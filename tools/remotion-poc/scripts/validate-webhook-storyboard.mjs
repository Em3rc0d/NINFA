/** Strict local evidence/storyboard contract gate. This is not a media quality test. */
export const REQUIRED_SHOTS=['hook','naive','naive-result','constraint','guarded','compare','limitation'];
const reject=(valid,reason)=>{if(!valid)throw new Error('POLICY_BLOCKED: '+reason);};
export function validateWebhookStoryboard(plan,props,receipt){
 reject(plan?.schema==='ninfa-motion-grammar-v1'&&plan.id==='webhook-v3-single-slice'&&plan.kind==='webhook','schema');
 reject(plan.video?.width===1080&&plan.video?.height===1920&&plan.video?.fps===30&&plan.video?.frames===720&&plan.video?.audio==='SILENT_REVIEW_ONLY','media');
 reject(plan.authority?.releaseState==='BLOCKED'&&plan.authority?.publishAuthority==='NONE'&&plan.authority?.reviewOnly===true&&plan.authority?.paidApisUsd===0&&plan.authority?.githubMediaActions===false&&plan.authority?.logo==='CANONICAL_BYTES_NOT_AVAILABLE_OMIT','authority');
 reject(props?.releaseState==='BLOCKED'&&props?.reviewOnly===true&&props?.kind==='webhook'&&props?.metrics?.[0]==='2 ACTIONS'&&props?.metrics?.[1]==='1 ACTION','adapter');
 reject(receipt?.schema==='local-replay-v1'&&receipt.experimental_mode==='LOCAL_SYNTHETIC_SEQUENTIAL'&&receipt.naive?.new_actions===2&&receipt.guarded?.new_actions===1&&receipt.naive?.attempts===2&&receipt.guarded?.attempts===2&&receipt.guarded?.inserted?.[0]===true&&receipt.guarded?.inserted?.[1]===false,'receipt');
 reject(plan.evidence?.sourceManifest==='tools/motion-v15/story.json'&&plan.evidence?.receipt==='tools/motion-v15/evidence/replay_evidence.json'&&plan.evidence?.receiptExperimentalMode==='LOCAL_SYNTHETIC_SEQUENTIAL','provenance');
 reject(plan.evidence?.eventKey===receipt.inputs?.event_key&&plan.evidence?.attemptsPerCase===2&&plan.evidence?.naiveActions===receipt.naive.new_actions&&plan.evidence?.guardedActions===receipt.guarded.new_actions&&plan.evidence?.concurrencyTested===false,'bounded measurements');
 reject(plan.layout?.safeTop>=220&&plan.layout?.safeBottom>=350&&plan.layout?.safeSide>=85&&plan.layout?.captionReserveTop===1460&&plan.layout?.captionReserveBottom===1570,'safe zones');
 reject(Array.isArray(plan.shots)&&plan.shots.length===REQUIRED_SHOTS.length,'shot count');
 for(let i=0;i<REQUIRED_SHOTS.length;i++){
  const s=plan.shots[i];
  reject(s?.id===REQUIRED_SHOTS[i]&&s.start===(i?plan.shots[i-1].end:0)&&Number.isInteger(s.start)&&Number.isInteger(s.end)&&s.end>s.start&&s.end<=720,'shot order/coverage');
  reject(typeof s.headline==='string'&&s.headline.length>6&&typeof s.action==='string'&&s.action.length>15&&typeof s.narration==='string'&&s.narration.length>10,'shot content');
 }
 reject(plan.shots[plan.shots.length-1].end===720&&plan.shots[plan.shots.length-1].headline==='CONCURRENCY NOT TESTED.','final caveat');
 const words=plan.shots.reduce((sum,s)=>sum+s.narration.split(/\s+/).length,0);
 reject(words<=65,'impossible draft voice pacing');
 return {frames:720,shotCount:plan.shots.length,narrationWords:words,reviewOnly:true};
}
