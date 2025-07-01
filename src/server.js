const express = require('express');
const bodyParser = require('body-parser');
const osc = require('osc');
const path = require('path');

const app = express();
const port = 3000;
const TD_OSC_PORT = 8000;
const TD_OSC_HOST = '127.0.0.1';

// Middleware
app.use(bodyParser.json());
app.use(express.static(__dirname)); // Serve files from current directory

// Serve index.html for root path
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// OSC setup
const udpPort = new osc.UDPPort({
  localAddress: "0.0.0.0",
  localPort: 57121,
  remoteAddress: TD_OSC_HOST,
  remotePort: TD_OSC_PORT
});
udpPort.open();

// Handle POST requests from browser
app.post('/send', (req, res) => {
  const { topic, value } = req.body;
  console.log(`Received: ${topic} = ${value}`);
  udpPort.send({ address: topic, args: [parseFloat(value)] });
  res.sendStatus(200);
});

// Start server
app.listen(port, () => {
  console.log(`Web UI running at http://localhost:${port}`);
});
