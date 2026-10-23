/**
 * FFmpeg 5.1+ uses -fps_mode (per-output), not legacy -vsync.
 * vfr prevents the image2 muxer from duplicating selected source frames.
 * Input frame numbers remain source zero-based indices.
 */
export function buildFrameExtractionCommand(video,pattern,frames){
 if(typeof video!=='string'||!video||typeof pattern!=='string'||!pattern||!Array.isArray(frames)||frames.length!==19)throw new Error('POLICY_BLOCKED: invalid frame extraction inputs');
 if(frames.some((n,i)=>!Number.isInteger(n)||n<0||n>=720||(i>0&&n<=frames[i-1])))throw new Error('POLICY_BLOCKED: invalid or unordered frame indices');
 const expr='select='+frames.map(n=>'eq(n\\,'+n+')').join('+');
 return {
  executable:'ffmpeg',
  args:['-hide_banner','-loglevel','error','-i',video,'-vf',expr,
   '-fps_mode','vfr','-start_number','0','-frames:v',String(frames.length),pattern],
 };
}
