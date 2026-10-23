import {createServer} from 'node:net';

/**
 * Ask the local OS for an unused TCP port, then release it for the Remotion
 * render command. The brief release/rebind window is unavoidable with CLI
 * invocation, but avoids deterministic collisions with Studio on port 3000.
 */
export function chooseAvailablePort() {
 return new Promise((resolve, reject) => {
  const server = createServer();
  server.once('error', reject);
  server.listen(0, '127.0.0.1', () => {
   const addr = server.address();
   if (!addr || typeof addr === 'string') {
    server.close();
    reject(new Error('RENDER_PORT_UNAVAILABLE: TCP address not assigned'));
    return;
   }
   const port = addr.port;
   server.close((error) => error ? reject(error) : resolve(port));
  });
 });
}
