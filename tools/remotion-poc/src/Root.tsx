import React from 'react';
import {Composition} from 'remotion';
import {Scene,type Props} from './Scenes';
import {SceneV2} from './ScenesV2';
import {WebhookV3} from './WebhookV3';
const base={channel:'DoesItAutomate',language:'en',reviewOnly:true,releaseState:'BLOCKED',safeZone:{top:220,bottom:350,side:85}} as const;
const samples={
 cache:{...base,kind:'cache',title:'THE CACHE TEST',subtitle:'ONE LOCAL HOST',source:'NINFA Motion v1.3 receipt',disclosure:'4.80s versus 1.15s measured once; not universal',metrics:['4.80s','1.15s'],labels:['FRESH','CACHED']},
 webhook:{...base,kind:'webhook',title:'DUPLICATE WEBHOOK',subtitle:'SYNTHETIC SQLITE REPLAY',source:'NINFA Motion v1.5 replay',disclosure:'Sequential synthetic test; no concurrency claim',metrics:['2 ACTIONS','1 ACTION'],labels:['NO UNIQUE KEY','WITH UNIQUE KEY']},
 automation:{...base,kind:'automation',title:'TOOL CALL ≠ WORKFLOW',subtitle:'ARCHIVED THIRD-PARTY BENCHMARK',source:'AutomationBench / Qwen3.6-27B base',disclosure:'Public third-party run; not a NINFA run',metrics:['2 / 8','29'],labels:['CHECKS PASSED','TOOL CALLS']}
} satisfies Record<string,Props>;
export const Root:React.FC=()=> <>{([
 ['CacheRace',samples.cache,180],
 ['WebhookReplay',samples.webhook,720],
 ['AutomationFailure',samples.automation,180],
 ['CacheRaceV2',samples.cache,180],
 ['WebhookReplayV2',samples.webhook,720],
 ['AutomationFailureV2',samples.automation,180],
 ['WebhookReplayV3',samples.webhook,720]
] as const).map(([id,props,frames])=><Composition key={id} id={id} component={id==='WebhookReplayV3'?WebhookV3:id.endsWith('V2')?SceneV2:Scene} width={1080} height={1920} fps={30} durationInFrames={frames} defaultProps={props}/>)}</>;
