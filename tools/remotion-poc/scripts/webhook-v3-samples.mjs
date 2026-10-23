/** Canonical frame sampling to inspect every shot and both sides of every cut. */
export const SHOT_MIDPOINTS=Object.freeze([39,144,252,346,475,594,678]);
export const CUT_BOUNDARIES=Object.freeze([78,210,294,399,552,636]);
export function sampleFrames(){
 const frames=[...SHOT_MIDPOINTS];
 for(const cut of CUT_BOUNDARIES)frames.push(cut-1,cut);
 return frames.sort((a,b)=>a-b);
}
