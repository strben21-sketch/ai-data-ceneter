import express from 'express';
import { createServer } from 'http';
import { join } from 'path';
import { scramjetPath } from '@mercuryworkshop/scramjet/path';
import { wispServer } from '@mercuryworkshop/wisp-js/server';

const app = express();
const server = createServer();
const PORT = process.env.PORT || 8080;

// Serve public static assets (our HTML interface)
app.use(express.static('public'));

// Dynamically expose the Scramjet service worker script distribution
app.use('/scram/', express.static(scramjetPath));

// Route requests back to index if needed
app.get('/', (req, res) => {
    res.sendFile(join(process.cwd(), 'public', 'index.html'));
});

// Bind HTTP app and capture WebSocket upgrade requests for the Wisp transport protocol
server.on('request', app);
server.on('upgrade', (req, socket, head) => {
    // Routes websocket requests starting with /wisp/ straight into the proxy backend
    if (req.url.startsWith('/wisp/')) {
        wispServer(req, socket, head);
    } else {
        socket.destroy();
    }
});

server.listen(PORT, () => {
    console.log(`🚀 Scramjet Proxy running on port ${PORT}`);
    console.log(`🔗 Local Address: http://localhost:${PORT}`);
});
