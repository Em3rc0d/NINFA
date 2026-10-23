import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import plan from '../storyboards/webhook-v3.json';
import type {Props} from './Scenes';

/**
 * Single Webhook V3 vertical slice. Storyboard is a non-overlapping, frame-
 * exact, 7-shot contract. On-screen state mutations are schematic recreations
 * of the *sequential synthetic* NINFA Motion v1.5 SQLite receipts.
 */
const P = {
 bg:'#0a131a', panel:'#142530',ink:'#f4f9fc',muted:'#b8cbd5',faint:'#617e8f',
 cyan:'#48d1f7',green:'#85e5c9',red:'#ff8b82',line:'#3c5d6d',yellow:'#ffcd75'
};
const font = 'Arial, Helvetica, sans-serif';
const mono = 'Consolas, "Courier New", monospace';
const clamp = (x:number) => Math.max(0,Math.min(1,x));
const smooth = (x:number) => {const n=clamp(x);return n*n*(3-2*n);};
const progress = (f:number,start:number,duration:number) => smooth((f-start)/duration);
const X = (n:number) => Math.round(n);
type FrameShotProps={t:number;props:Props};
const Head:React.FC<{kicker:string;title:string;detail?:string}>=({kicker,title,detail})=>
 <div style={{position:'absolute',top:0,left:0,right:0}}>
  <div style={{fontFamily:mono,color:P.cyan,fontSize:29,fontWeight:700,letterSpacing:2}}>{kicker}</div>
  <div style={{marginTop:24,color:P.ink,fontWeight:900,fontSize:73,lineHeight:1.06,letterSpacing:-2,whiteSpace:'pre-line'}}>{title}</div>
  {detail&&<div style={{color:P.muted,fontSize:32,marginTop:20,lineHeight:1.25}}>{detail}</div>}
 </div>;
const Status:React.FC<{label:string;color:string}>=({label,color})=>
 <div style={{display:'inline-flex',padding:'11px 22px',border:'2px solid '+color,borderRadius:11,color,fontFamily:mono,fontSize:27,fontWeight:800,letterSpacing:1.1}}>{label}</div>;
const EventToken:React.FC<{x:number;y:number;index:number;accent:string;opacity?:number}>=({x,y,index,accent,opacity=1})=>
 <g opacity={opacity} transform={'translate('+x+','+y+')'}>
  <circle r="45" fill={P.panel} stroke={accent} strokeWidth="7"/>
  <circle r="15" fill={accent}/>
  <text x="0" y="77" fill={P.ink} fontSize="32" fontFamily={mono} textAnchor="middle">{'DELIVERY '+index}</text>
 </g>;
const EventLane:React.FC<{t:number;guarded:boolean}>=({t,guarded})=>{
 const one=progress(t,9,47),two=progress(t,74,47);
 const acceptedEnd=635;
 const duplicateEnd=guarded?510:635;
 const dbX=620;
 const y1=175,y2=360;
 return <div style={{position:'absolute',top:282,left:0,width:910,height:660}}>
  <svg width="910" height="515" viewBox="0 0 910 515" aria-label="Illustrative sequential event flow">
   <line x1="95" x2="665" y1={y1} y2={y1} stroke={P.line} strokeWidth="5" strokeDasharray="11 13"/>
   <line x1="95" x2="665" y1={y2} y2={y2} stroke={P.line} strokeWidth="5" strokeDasharray="11 13"/>
   {guarded&&<g>
    <rect x="465" y="103" width="130" height="332" rx="25" fill={P.panel} stroke={P.cyan} strokeWidth="4"/>
    <text x="530" y="80" fill={P.cyan} textAnchor="middle" fontSize="28" fontFamily={mono}>UNIQUE</text>
    <text x="530" y="252" fill={P.green} textAnchor="middle" fontSize="43" fontWeight="bold">✓</text>
    <text x="530" y="425" fill={P.red} textAnchor="middle" fontSize="43" fontWeight="bold" opacity={progress(t,119,9)}>×</text>
   </g>}
   {one<1&&<EventToken x={X(95+(acceptedEnd-95)*one)} y={y1} index={1} accent={P.cyan} opacity={progress(t,0,12)}/>}
   {two<1&&<EventToken x={X(95+(duplicateEnd-95)*two)} y={y2} index={2} accent={guarded?P.red:P.cyan} opacity={progress(t,65,12)}/>}
   {one>=1&&<g><circle cx={630} cy={y1} r="32" fill={P.green}/><text x={guarded?510:630} y={y1+12} textAnchor="middle" fill={P.bg} fontWeight="bold" fontSize="41">✓</text></g>}
   {two>=1&&<g><circle cx={guarded?510:630} cy={y2} r="32" fill={guarded?P.red:P.green}/><text x={guarded?510:630} y={y2+12} textAnchor="middle" fill={P.bg} fontWeight="bold" fontSize="41">{guarded?'×':'✓'}</text></g>}
   <text x="90" y="485" fill={P.muted} fontFamily={mono} fontSize="26">SAME KEY · TWO SEQUENTIAL CONNECTIONS</text>
  </svg>
  <div style={{position:'absolute',left:622,top:72,width:270,height:398,padding:23,background:P.panel,borderRadius:20,border:'2px solid '+P.line,boxSizing:'border-box'}}>
   <div style={{color:P.muted,fontSize:28,fontFamily:mono}}>SQLite rows</div>
   <div style={{marginTop:21,fontSize:26,fontFamily:mono,color:P.faint}}>event_key</div>
   {(one>=1)&&<div style={{marginTop:23,padding:'13px 10px',background:'#25463c',borderLeft:'7px solid '+P.green,fontSize:29,fontFamily:mono}}>evt_local_001</div>}
   {(two>=1&&!guarded)&&<div style={{marginTop:15,padding:'13px 10px',background:'#52322e',borderLeft:'7px solid '+P.red,fontSize:29,fontFamily:mono}}>evt_local_001</div>}
   {(two>=1&&guarded)&&<div style={{marginTop:15,fontSize:25,fontWeight:800,color:P.red}}>DUPLICATE<br/>IGNORED</div>}
  </div>
 </div>;
};
const Hook:React.FC<FrameShotProps>=({t})=>{
 const a=progress(t,8,33),b=progress(t,34,33);
 return <>
  <Head kicker="01 / EVENT REPLAY" title={'ONE EVENT.\nTWO DELIVERIES.'} detail="The same synthetic key arrives twice."/>
  <div style={{position:'absolute',top:330,left:0,right:0,height:480}}>
   <svg viewBox="0 0 910 480" width="910" height="480">
    <path d="M 105 145 L 805 145 M 105 325 L 805 325" stroke={P.line} strokeWidth="6" strokeDasharray="11 12"/>
    <EventToken x={X(105+670*a)} y={145} index={1} accent={P.cyan}/>
    <EventToken x={X(105+670*b)} y={325} index={2} accent={P.cyan} opacity={progress(t,27,9)}/>
   </svg>
  </div>
  <div style={{position:'absolute',top:885,left:0}}><Status label="event_key = evt_local_001" color={P.cyan}/></div>
 </>;
};
const Naive:React.FC<FrameShotProps>=({t})=><>
 <Head kicker="02 / WITHOUT DATABASE GUARD" title={'BOTH WRITES\nSUCCEED.'} detail="Two successive deliveries. Two saved rows."/>
 <EventLane t={t} guarded={false}/>
 </>;
const NaiveResult:React.FC<FrameShotProps>=({t,props})=><>
 <Head kicker="03 / UNGUARDED RESULT" title={'ONE KEY.\nTWO ACTIONS.'} detail="No unique constraint in this local test."/>
 <div style={{position:'absolute',top:345,left:40,width:830}}>
  <div style={{color:P.red,fontSize:177,fontWeight:900,lineHeight:1,letterSpacing:-8}}>{props.metrics[0].slice(0,1)}</div>
  <div style={{height:9,width:750,background:P.red,marginTop:24,transform:'scaleX('+progress(t,9,22)+')',transformOrigin:'left'}}/>
  {[1,2].map((n)=> <div key={n} style={{marginTop:31,padding:'22px 33px',background:P.panel,borderLeft:'9px solid '+P.red,opacity:progress(t,10+n*17,8),fontSize:36,fontFamily:mono}}>{'row '+n+'  ·  evt_local_001'}</div>)}
 </div>
 </>;
const Constraint:React.FC<FrameShotProps>=({t})=>{
 const reveal=progress(t,5,30),scan=progress(t,32,45);
 return <>
  <Head kicker="04 / DATABASE CONSTRAINT" title={'ADD A\nUNIQUE KEY.'} detail="Only one row can use this event key."/>
  <div style={{position:'absolute',top:360,width:910}}>
   <div style={{background:P.panel,border:'2px solid '+P.cyan,borderRadius:28,padding:'55px 35px',fontFamily:mono}}>
    <div style={{color:P.muted,fontSize:30}}>SQLITE / UNIQUE INDEX</div>
    <div style={{fontSize:59,fontWeight:900,letterSpacing:-2,marginTop:29,opacity:reveal,color:P.cyan}}>UNIQUE(event_key)</div>
    <div style={{height:8,width:'100%',background:P.line,marginTop:40}}><div style={{width:scan*100+'%',height:8,background:P.green}}/></div>
   </div>
   <div style={{marginTop:45,fontSize:37,color:P.green,opacity:scan}}>The database now rejects duplicate keys.</div>
  </div>
 </>;
};
const Guarded:React.FC<FrameShotProps>=({t})=><>
 <Head kicker="05 / WITH UNIQUE(event_key)" title={'FIRST IN.\nSECOND STOPPED.'} detail="Same event replayed sequentially."/>
 <EventLane t={t} guarded/>
 </>;
const Compare:React.FC<FrameShotProps>=({t,props})=><>
 <Head kicker="06 / RECORDED LOCAL COUNTS" title={'SAME EVENT.\nDIFFERENT RESULT.'}/>
 <div style={{position:'absolute',top:375,left:0,right:0,display:'flex',justifyContent:'space-between',alignItems:'center'}}>
  <div style={{width:350,opacity:progress(t,5,12)}}>
   <div style={{fontSize:31,color:P.muted,fontFamily:mono}}>NO UNIQUE KEY</div>
   <div style={{fontSize:164,color:P.red,fontWeight:900}}>{props.metrics[0].charAt(0)}</div>
   <div style={{fontSize:35,color:P.muted}}>new actions</div>
   <div style={{height:19,width:300,background:P.red,marginTop:20,borderRadius:9}}/>
  </div>
  <div style={{fontSize:82,color:P.cyan,opacity:progress(t,23,10)}}>→</div>
  <div style={{width:350,opacity:progress(t,28,12)}}>
   <div style={{fontSize:31,color:P.muted,fontFamily:mono}}>WITH UNIQUE KEY</div>
   <div style={{fontSize:164,color:P.green,fontWeight:900}}>{props.metrics[1].charAt(0)}</div>
   <div style={{fontSize:35,color:P.muted}}>new action</div>
   <div style={{height:19,width:150,background:P.green,marginTop:20,borderRadius:9}}/>
  </div>
 </div>
 <div style={{position:'absolute',top:930,fontSize:35,color:P.ink}}>Synthetic sequential SQLite result.</div>
 </>;
const Limitation:React.FC<FrameShotProps>=({t})=><>
 <Head kicker="07 / EXPERIMENT LIMIT" title={'CONCURRENCY\nNOT TESTED.'} detail="This demonstrates sequential SQLite behavior only."/>
 <div style={{position:'absolute',top:405,left:0,right:0}}>
  <div style={{height:12,background:P.red,width:850*progress(t,3,12),marginBottom:65}}/>
  <div style={{fontSize:44,fontWeight:900,color:P.yellow}}>NOT A LIVE WEBHOOK TEST.</div>
  <div style={{fontSize:37,lineHeight:1.45,color:P.muted,marginTop:28}}>No provider network. No money movement.<br/>No production reliability claim.</div>
 </div>
 </>;

const shotComponents:Record<string,React.FC<FrameShotProps>>={
 hook:Hook,naive:Naive,'naive-result':NaiveResult,constraint:Constraint,
 guarded:Guarded,compare:Compare,limitation:Limitation
};
export const WebhookV3:React.FC<Props>=(props)=>{
 const frame=useCurrentFrame();
 // Half-open ranges are mutually exclusive by contract: no stacked title crossfades.
 const shot=plan.shots.find(s=>frame>=s.start&&frame<s.end);
 if(!shot)throw new Error('POLICY_BLOCKED: storyboard does not cover frame '+frame);
 const Content=shotComponents[shot.id];
 if(!Content)throw new Error('POLICY_BLOCKED: unknown storyboard shot '+shot.id);
 return <AbsoluteFill style={{background:P.bg,fontFamily:font,color:P.ink}}>
  <AbsoluteFill style={{backgroundImage:'linear-gradient(90deg,rgba(72,209,247,0.055) 1px,transparent 1px),linear-gradient(rgba(72,209,247,0.05) 1px,transparent 1px)',backgroundSize:'104px 104px',opacity:0.4}}/>
  <div style={{position:'absolute',top:224,left:85,right:85,display:'flex',justifyContent:'space-between',fontFamily:mono,fontSize:26,color:P.cyan,fontWeight:800}}>
   <div>LOCAL SQLITE / SYNTHETIC REPLAY</div><div>{String(shot.id).toUpperCase()}</div>
  </div>
  <div style={{position:'absolute',top:343,left:85,width:910,height:1010}}>
   <Content t={frame-shot.start} props={props}/>
  </div>
  <div style={{position:'absolute',left:85,top:1304,right:85,borderTop:'2px solid '+P.line,paddingTop:21}}>
   <div style={{fontSize:30,fontWeight:700,color:P.muted}}>NINFA Motion v1.5 · sequential local SQLite evidence</div>
   <div style={{fontSize:26,color:P.muted,marginTop:12}}>{props.disclosure}</div>
   <div style={{fontSize:25,color:P.cyan,marginTop:14,fontFamily:mono}}>ILLUSTRATIVE REPLAY · REVIEW ONLY · NO OFFICIAL LOGO</div>
  </div>
  <div style={{position:'absolute',left:85,top:1490,right:85,height:65,border:'1px dashed '+P.line,borderRadius:10,opacity:0.26}}>
   <div style={{fontSize:23,marginTop:12,textAlign:'center',color:P.muted}}>CAPTIONS RESERVED (not timed to audio)</div>
  </div>
 </AbsoluteFill>;
};
