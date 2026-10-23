import test from 'node:test';
import assert from 'node:assert/strict';
import {buildRenderCommand} from '../scripts/render-command.mjs';
const input={
  app:'C:\\Users\\test user\\NINFA\\tools\\remotion-poc',
  composition:'CacheRace',
  output:'C:\\Users\\test user\\NINFA-Review\\cache.mp4',
  propsFile:'C:\\Temp\\name with spaces\\props.json',
  port:62484,
};
test('Node launches Remotion CLI directly without a Windows shell',()=>{
  const cmd=buildRenderCommand(input);
  assert.equal(cmd.executable,process.execPath);
  assert.equal(cmd.options.shell,false);
  assert.match(cmd.args[0],/remotion-cli\.js$/);
  assert.equal(cmd.args[4],input.output);
  assert.ok(cmd.args.includes('--props='+input.propsFile));
  assert.ok(cmd.args.includes('--port=62484'));
});
test('reject unknown Remotion composition',()=>assert.throws(
 ()=>buildRenderCommand({...input,composition:'UntrustedCode'}),/POLICY_BLOCKED/
));
test('reject invalid Remotion port',()=>assert.throws(
 ()=>buildRenderCommand({...input,port:0}),/POLICY_BLOCKED/
));
