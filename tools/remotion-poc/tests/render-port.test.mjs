import test from 'node:test';
import assert from 'node:assert/strict';
import {createServer} from 'node:net';
import {chooseAvailablePort} from '../scripts/render-port.mjs';

test('render server uses an available port rather than Studio 3000', async () => {
 const port = await chooseAvailablePort();
 assert.ok(Number.isInteger(port) && port > 1024 && port <= 65535);
 assert.notEqual(port, 3000);
 // The allocated port must be released so Remotion CLI can bind to it.
 const server = createServer();
 await new Promise((resolve, reject) => {
  server.once('error', reject);
  server.listen(port, '127.0.0.1', resolve);
 });
 await new Promise(resolve => server.close(resolve));
});
