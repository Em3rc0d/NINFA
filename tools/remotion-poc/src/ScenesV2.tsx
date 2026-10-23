import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import type {Props} from './Scenes';

/**
 * Motion study V2. Each shot explains an observable input, change, or result.
 * Data/claims still come exclusively from the vetted NINFA adapter.
 */
const C={bg:'#0c151b',surface:'#172733',surface2:'#223a4a',white:'#f5f9fc',muted:'#b6cbd5',cyan:'#44d2fb',green:'#81e5d1',red:'#ff837d',line:'#355566'};
const clamp=(n:number)=>Math.min(1,Math.max(0,n));
const ease=(n:number)=>{const x=clamp(n);return x*x*(3-2*x)};
const rise=(f:number,start:number,length=12)=>ease((f-start)/length);
const exposure=(f:number,start:number,end:number,fade=12)=>clamp(Math.min(rise(f,start,fade),1-ease((f-(end-fade))/fade)));
const pulse=(f:number)=>0.5+0.5*Math.sin(f*0.12);
const mono='Consolas, "Courier New", monospace';
const Stage:React.FC<{f:number;start:number;end:number;children:React.ReactNode}>=({f,start,end,children})=>
 <div style={{position:'absolute',inset:0,opacity:exposure(f,start,end),pointerEvents:'none',transform:'translateY('+(1-exposure(f,start,end))*20+'px)'}}>{children}</div>;
const Tag:React.FC<{children:React.ReactNode;color?:string}>=({children,color=C.cyan})=>
 <div style={{fontSize:27,color,letterSpacing:3,fontWeight:800,textTransform:'uppercase'}}>{children}</div>;
const Head:React.FC<{children:React.ReactNode}>=({children})=>
 <div style={{fontSize:81,lineHeight:1.03,fontWeight:900,letterSpacing:-3,marginTop:20,maxWidth:900}}>{children}</div>;
const Label:React.FC<{children:React.ReactNode}>=({children})=>
 <div style={{fontFamily:mono,fontSize:30,letterSpacing:1.2,color:C.muted}}>{children}</div>;
const Big:React.FC<{children:React.ReactNode;color?:string}>=({children,color=C.white})=>
 <div style={{fontSize:112,fontWeight:900,letterSpacing:-3,lineHeight:1.1,color}}>{children}</div>;
const Panel:React.FC<{children:React.ReactNode;accent?:string;style?:React.CSSProperties}>=({children,accent=C.line,style})=>
 <div style={{background:'linear-gradient(150deg,'+C.surface2+','+C.surface+')',border:'2px solid '+accent,borderRadius:25,padding:33,...style}}>{children}</div>;
const AnimatedLink:React.FC<{f:number;start:number;fromX:number;toX:number;y:number;color?:string;dashed?:boolean}>=({f,start,fromX,toX,y,color=C.cyan,dashed=false})=>{
 const progress=rise(f,start,18);
 return <svg width="100%" height="100%" viewBox="0 0 910 600" style={{position:'absolute',inset:0,pointerEvents:'none'}}>
  <line x1={fromX} x2={fromX+(toX-fromX)*progress} y1={y} y2={y} stroke={color} strokeWidth="9" strokeDasharray={dashed?'18 17':'none'}/>
  <circle cx={fromX+(toX-fromX)*progress} cy={y} r={11+3*pulse(f)} fill={color}/>
 </svg>;
};
const PipelineNode:React.FC<{x:number;y:number;name:string;detail:string;color?:string;opacity?:number}>=({x,y,name,detail,color=C.cyan,opacity=1})=>
 <div style={{position:'absolute',left:x,top:y,width:240,height:148,opacity,borderRadius:20,border:'2px solid '+color,background:C.surface,padding:22,boxSizing:'border-box'}}>
  <Tag color={color}>{name}</Tag><div style={{marginTop:25,fontSize:26,color:C.muted}}>{detail}</div>
 </div>;

const CacheV2:React.FC<{p:Props;f:number}>=({p,f})=><>
 <Stage f={f} start={-12} end={54}>
  <Tag>Measured on one local host</Tag>
  <Head>ONE VIDEO.<br/>TWO RENDERS.</Head>
  <div style={{display:'flex',gap:24,marginTop:88}}>
   <Panel style={{flex:1}} accent={C.cyan}><Label>FIRST RUN</Label><Big>4.80<span style={{fontSize:49}}>s</span></Big></Panel>
   <Panel style={{flex:1}} accent={C.green}><Label>CACHE HIT</Label><Big color={C.green}>1.15<span style={{fontSize:49}}>s</span></Big></Panel>
  </div>
  <div style={{marginTop:60,fontSize:36}}>Same clean visual. Different work.</div>
 </Stage>
 <Stage f={f} start={45} end={105}>
  <Tag>What happened · fresh run</Tag><Head>BUILD THE<br/>VIDEO.</Head>
  <div style={{height:300,position:'relative',marginTop:95}}>
   <PipelineNode x={0} y={105} name="INPUT" detail="Clean source"/>
   <PipelineNode x={330} y={105} name="ENCODE" detail="Fresh output"/>
   <PipelineNode x={665} y={105} name="MP4" detail="Saved result" color={C.green}/>
   <AnimatedLink f={f} start={58} fromX={240} toX={330} y={180}/>
   <AnimatedLink f={f} start={76} fromX={570} toX={665} y={180} color={C.green}/>
  </div>
  <div style={{fontSize:41,fontWeight:700,color:C.cyan}}>FIRST PASS → ENCODE</div>
 </Stage>
 <Stage f={f} start={97} end={152}>
  <Tag>What happened · identical input</Tag><Head>DON'T ENCODE<br/>AGAIN.</Head>
  <div style={{height:300,position:'relative',marginTop:90}}>
   <PipelineNode x={0} y={85} name="INPUT" detail="Same digest"/>
   <PipelineNode x={330} y={85} name="CACHE" detail="Hash matched" color={C.green}/>
   <PipelineNode x={665} y={85} name="MP4" detail="Reused" color={C.green}/>
   <AnimatedLink f={f} start={108} fromX={240} toX={330} y={160} color={C.green}/>
   <AnimatedLink f={f} start={124} fromX={570} toX={665} y={160} color={C.green}/>
  </div>
  <div style={{fontSize:41,fontWeight:800,color:C.green}}>CACHE HIT → REUSE</div>
 </Stage>
 <Stage f={f} start={144} end={195}>
  <Tag>Actual measured result · no general claim</Tag>
  <Head>THE CACHE<br/>SKIPS WORK.</Head>
  <div style={{marginTop:75}}>
   <Label>FRESH · {p.metrics[0]}</Label><div style={{height:60,width:800*rise(f,151,12),background:C.cyan,borderRadius:10,margin:'15px 0 45px'}}/>
   <Label>CACHED · {p.metrics[1]}</Label><div style={{height:60,width:800*(1.15/4.8)*rise(f,161,12),background:C.green,borderRadius:10,marginTop:15}}/>
  </div>
  <div style={{fontSize:41,marginTop:65}}>One host. Same input. Measured locally.</div>
 </Stage>
 </>;

const EventChip:React.FC<{x:number;y:number;id:string;accent:string;show?:number}>=({x,y,id,accent,show=1})=>
 <div style={{position:'absolute',left:x,top:y,width:304,height:115,opacity:show,borderRadius:18,border:'3px solid '+accent,background:C.surface,padding:25,boxSizing:'border-box'}}>
  <div style={{fontSize:27,color:C.muted}}>EVENT</div><div style={{fontFamily:mono,fontWeight:700,fontSize:29,marginTop:11}}>{id}</div>
 </div>;
const WebhookV2:React.FC<{p:Props;f:number}>=({p,f})=><>
 <Stage f={f} start={-12} end={110}>
  <Tag>Local SQLite experiment · synthetic</Tag><Head>SAME EVENT.<br/>TWICE.</Head>
  <div style={{position:'relative',height:490,marginTop:75}}>
   <EventChip x={45} y={66} id="evt_local_001" accent={C.cyan} show={rise(f,9,25)}/>
   <EventChip x={455} y={215} id="evt_local_001" accent={C.cyan} show={rise(f,48,25)}/>
   <div style={{position:'absolute',top:378,fontSize:53,fontWeight:800,color:C.red,opacity:rise(f,70,20)}}>TWO DELIVERIES →</div>
  </div>
  <Label>Two sequential connections. No real provider.</Label>
 </Stage>
 <Stage f={f} start={98} end={248}>
  <Tag>Step 1 · no uniqueness constraint</Tag><Head>BOTH EVENTS<br/>WRITE.</Head>
  <div style={{display:'flex',gap:28,marginTop:85}}>
   {[0,1].map(i=><Panel key={i} accent={C.red} style={{flex:1,opacity:rise(f,118+i*43,18)}}>
     <Label>DELIVERY {i+1}</Label><Big color={C.red}>+1</Big><Label>Stored action</Label>
    </Panel>)}
  </div>
  <div style={{fontSize:53,fontWeight:900,color:C.red,marginTop:85,opacity:rise(f,209,20)}}>RESULT: 2 ACTIONS</div>
 </Stage>
 <Stage f={f} start={238} end={397}>
  <Tag>Step 2 · add a database guard</Tag><Head>UNIQUE<br/>(event_key)</Head>
  <Panel accent={C.cyan} style={{marginTop:95,background:'#102531'}}>
   <Label>SQL CONSTRAINT</Label>
   <div style={{fontFamily:mono,fontSize:53,fontWeight:800,color:C.cyan,marginTop:30}}>UNIQUE(event_key)</div>
   <div style={{fontSize:33,marginTop:46,color:C.muted}}>One stored row per event key.</div>
  </Panel>
  <div style={{marginTop:60,fontSize:38,color:C.white}}>Replay the same synthetic event.</div>
 </Stage>
 <Stage f={f} start={383} end={541}>
  <Tag>Step 3 · sequential replay</Tag><Head>THE SECOND<br/>WRITE STOPS.</Head>
  <div style={{display:'flex',gap:26,marginTop:88}}>
   <Panel accent={C.green} style={{flex:1,opacity:rise(f,400,18)}}><Label>FIRST DELIVERY</Label><Big color={C.green}>+1</Big><Label>Inserted</Label></Panel>
   <Panel accent={C.red} style={{flex:1,opacity:rise(f,447,18)}}><Label>DUPLICATE</Label><Big color={C.red}>0</Big><Label>Ignored</Label></Panel>
  </div>
  <div style={{fontSize:48,fontWeight:900,color:C.green,marginTop:75,opacity:rise(f,500,18)}}>RESULT: 1 ACTION</div>
 </Stage>
 <Stage f={f} start={525} end={663}>
  <Tag>Same input · two local cases</Tag><Head>2 ACTIONS<br/>BECOME 1.</Head>
  <div style={{display:'flex',gap:24,marginTop:90}}>
   <Panel accent={C.red} style={{flex:1}}><Label>NAIVE</Label><Big color={C.red}>2</Big><Label>stored</Label></Panel>
   <Panel accent={C.green} style={{flex:1}}><Label>GUARDED</Label><Big color={C.green}>1</Big><Label>stored</Label></Panel>
  </div>
  <div style={{fontSize:36,color:C.muted,marginTop:65}}>Local replay with two separate connections.</div>
 </Stage>
 <Stage f={f} start={646} end={750}>
  <Tag color={C.red}>Scope limitation</Tag><Head>CONCURRENCY<br/>NOT TESTED.</Head>
  <Panel accent={C.red} style={{marginTop:90}}>
   <div style={{fontSize:42,fontWeight:800}}>Sequential SQLite simulation only.</div>
   <div style={{fontSize:32,color:C.muted,marginTop:30}}>No external webhook, live business action or production reliability claim.</div>
  </Panel>
 </Stage>
 </>;

const NetworkNode:React.FC<{label:string;status:'PASS'|'FAIL';x:number;y:number;f:number;start:number}>=({label,status,x,y,f,start})=>{
 const p=rise(f,start,12),color=status==='PASS'?C.green:C.red;
 return <div style={{position:'absolute',left:x,top:y,width:375,height:125,opacity:p,transform:'scale('+(0.90+p*0.1)+')',background:C.surface,borderRadius:19,border:'2px solid '+color,padding:21,boxSizing:'border-box'}}>
  <div style={{fontSize:29,color:C.muted}}>{label}</div>
  <div style={{fontSize:43,fontWeight:900,color,marginTop:8}}>{status}</div>
 </div>;
};
const AutomationV2:React.FC<{p:Props;f:number}>=({p,f})=><>
 <Stage f={f} start={-12} end={58}>
  <Tag>Published third-party benchmark</Tag>
  <Head>29 CALLS.<br/>ONE WORKFLOW.</Head>
  <div style={{marginTop:83,fontSize:130,fontWeight:950,lineHeight:1,color:C.cyan}}>29</div>
  <div style={{fontSize:43,fontWeight:800,marginTop:14}}>TOOL CALLS</div>
  <div style={{height:11,width:800,marginTop:66,background:C.surface2,borderRadius:5}}>
   <div style={{width:800*rise(f,8,36),height:'100%',background:C.cyan,borderRadius:5}}/>
  </div>
 </Stage>
 <Stage f={f} start={49} end={133}>
  <Tag>Illustrative systems · not trace order</Tag>
  <Head>TWO WORKED.<br/>FOUR BROKE.</Head>
  <div style={{position:'relative',height:495,marginTop:50}}>
   <NetworkNode label="Salesforce" status="PASS" x={0} y={15} f={f} start={57}/>
   <NetworkNode label="Calendar" status="PASS" x={425} y={15} f={f} start={66}/>
   <NetworkNode label="Calendly" status="FAIL" x={0} y={180} f={f} start={81}/>
   <NetworkNode label="Zoom" status="FAIL" x={425} y={180} f={f} start={89}/>
   <NetworkNode label="DocuSign" status="FAIL" x={0} y={345} f={f} start={102}/>
   <NetworkNode label="Proposal" status="FAIL" x={425} y={345} f={f} start={110}/>
  </div>
 </Stage>
 <Stage f={f} start={122} end={195}>
  <Tag>Qwen3.6-27B base · public run</Tag>
  <Head>TOOL USE<br/>≠ SUCCESS.</Head>
  <div style={{fontSize:157,fontWeight:950,marginTop:54,color:C.red,letterSpacing:-8}}>{p.metrics[0]}</div>
  <div style={{fontSize:47,fontWeight:800,color:C.white}}>SCORING CHECKS PASSED</div>
  <div style={{fontSize:36,marginTop:54,color:C.muted}}>A completed tool call is not a completed workflow.</div>
 </Stage>
 </>;

export const SceneV2:React.FC<Props>=(p)=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{background:C.bg,color:C.white,fontFamily:'Arial, sans-serif'}}>
  <AbsoluteFill style={{backgroundImage:'linear-gradient(90deg,transparent 96%,rgba(68,210,251,0.07) 100%),linear-gradient(transparent 96%,rgba(68,210,251,0.06) 100%)',backgroundSize:'90px 90px',opacity:0.28}}/>
  <div style={{position:'absolute',top:214,left:85,right:85,fontSize:26,letterSpacing:3,color:C.cyan,fontWeight:900}}>DOES IT AUTOMATE? / EXPERIMENT RECONSTRUCTION</div>
  <div style={{position:'absolute',top:290,left:85,right:85,height:1030}}>
   {p.kind==='cache'?<CacheV2 p={p} f={f}/>:p.kind==='webhook'?<WebhookV2 p={p} f={f}/>:<AutomationV2 p={p} f={f}/>}
  </div>
  <div style={{position:'absolute',left:85,right:85,top:1400,borderTop:'2px solid '+C.line,paddingTop:20}}>
   <div style={{fontSize:27,color:C.muted,fontWeight:800}}>{p.source}</div>
   <div style={{fontSize:25,color:C.muted,marginTop:10}}>{p.disclosure}</div>
   <div style={{fontFamily:mono,fontSize:23,color:C.cyan,marginTop:14}}>REVIEW ONLY · SILENT VIDEO · CANONICAL LOGO OMITTED</div>
  </div>
 </AbsoluteFill>;
};
