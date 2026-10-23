import {join} from 'node:path';

const compositions = new Set(['CacheRace', 'WebhookReplay', 'AutomationFailure', 'CacheRaceV2', 'WebhookReplayV2', 'AutomationFailureV2', 'WebhookReplayV3']);

/** Execute the installed Remotion CLI directly with Node, never through a shell. */
export function buildRenderCommand({app, composition, output, propsFile, port}) {
  if (!compositions.has(composition)) throw new Error('POLICY_BLOCKED: unsupported composition');
  if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('POLICY_BLOCKED: invalid render port');
  if (![app, output, propsFile].every((p) => typeof p === 'string' && p.length > 0)) {
    throw new Error('POLICY_BLOCKED: invalid path');
  }
  const cliEntry = join(app, 'node_modules', '@remotion', 'cli', 'remotion-cli.js');
  return {
    executable: process.execPath,
    args: [cliEntry, 'render', join(app, 'src', 'index.ts'), composition, output,
      '--props=' + propsFile, '--codec=h264', '--concurrency=2', '--port=' + port],
    options: {cwd: app, stdio: 'inherit', timeout: 900000, shell: false},
  };
}
