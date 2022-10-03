// create server
const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);
const path = require('path');
const fs = require('fs');
const mqtt = require('mqtt');
const client = mqtt.connect('mqtt://broker.mqttdashboard.com');

// set static folder
app.use(express.static(path.join(__dirname, 'static')));

// create socketio receive data mqtt_message
io.on('connection', (socket) => {
    console.log('connected');
    socket.on('disconnect', () => {
        console.log('disconnect');
    });
});

// create mqtt client
client.on('connect', () => {
    console.log('mqtt connected');
    client.subscribe('tankdata');
}
);

client.on('message', (topic, message) => {
    console.log('mqtt message');
    console.log(message.toString());
    // temp = JSON.parse(message);
    // send data to socketio
    io.emit('mqtt_message', message.toString());
}
);

// route 
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index1.html'));
});

// create server
server.listen(3000, () => {
    console.log('server running on port 3000');
}
);