# Real-Time Camera Feed

## Overview
This project provides a real-time camera feed through a Flask server using Socket.IO to stream camera frames to clients.

## Installation
Ensure that Flask-SocketIO and python-socketio are installed with the required versions:
```bash
pip install Flask-SocketIO==5.0.2 python-socketio==5.0.2
```

## Running the Server
To start the server, run:
```bash
python3 app.py
```
Make sure port `5000` is available or modify the port in the `app.py` script.

## Mock Client
A mock client is provided to demonstrate how to connect and receive streamed frames.

## Stream Format
Clients will receive data in the following format:
```json
{
  "frame": "bytearray of the frame",
  "timestamp": "date time of the frame recorded"
}
```

## Adjusting FPS
Users can adjust the frame rate from the UI, which will affect the server's frame capture rate.

## Usage
Clients can listen for `stream_frame` events to receive frames and `start_stream` or `stop_stream` to control streaming.

## Development Notes
- The server is configured for development. Use a production WSGI server for deployment.
- The UI and server endpoints are minimal and designed for demonstration.

