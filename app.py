from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import cv2
from datetime import datetime
import numpy as np
import requests
import os
import json
import threading
import time

# Initialize Flask app
app = Flask(__name__)
# Initialize SocketIO with CORS allowed from any origin, and enable logs
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Global variables to control the capture process and frame rate
capture = False  # Flag to control the capture process
FPS = 5  # Default Frames Per Second capture rate
frame_thread = None  # Thread for capturing frames

# Function to capture frames from the default camera
def capture_frames():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    frame_count = 0  # Initialize frame counter

    # Loop to capture frames as long as 'capture' is True
    while capture:
        # Capture a single frame
        ret, frame = cap.read()
        # If frame capture fails, break loop
        if not ret:
            break

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # Log frame capture with timestamp
        with open("frame_log.txt", "a") as log_file:
            log_file.write(f"Frame {frame_count} captured at {timestamp}\n")
            log_file.write(f"frame_bytes at {timestamp}: {frame_bytes}\n\n")
        # Emit the captured frame to all connected SocketIO clients
        socketio.emit('stream_frame', {'frame': frame_bytes, 'timestamp': timestamp})
        # Wait for a while before capturing the next frame
        socketio.sleep(1.0 / FPS)
        frame_count += 1  # Increment frame counter

    # Release video capture when loop ends
    cap.release()

# Flask before_request handler to log the headers of incoming requests
@app.before_request
def before_request():
    #print(request.headers)
    data = request.get_data(as_text=True)
    #print("the whole request: ", data)

# Route to serve the video streaming page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle starting the capture process
@app.route('/start_capture', methods=['POST'])
def start_capture():
    global capture, frame_thread, FPS
    data = request.get_json()  # Get data from the incoming request
    FPS = float(data.get('fps'))  # Update FPS based on client request
    capture = True  # Set capture flag to True to start frame capturing
    # Start a new thread for capturing frames
    threading.Thread(target=capture_frames, daemon=True).start()
    print("capture started")
    # Respond to the client that capture has started
    return jsonify({"message": "Capture started"})

# Route to handle stopping the capture process
@app.route('/stop_capture', methods=['POST'])
def stop_capture():
    global capture
    capture = False  # Set capture flag to False to stop frame capturing
    print("capture stopped")
    # Respond to the client that capture has stopped
    return jsonify({"message": "Capture stopped"})

# SocketIO event handler for starting the stream
@socketio.on('start_stream')
def handle_start_stream(message):
    global capture
    capture = True  # Set capture flag to True to start frame capturing
    # Start a new thread for capturing frames
    threading.Thread(target=capture_frames, daemon=True).start()

# SocketIO event handler for stopping the stream
@socketio.on('stop_stream')
def handle_stop_stream(message):
    global capture
    capture = False  # Set capture flag to False to stop frame capturing

# Main entry point for running the app
if __name__ == "__main__":
    socketio.run(app, debug=True)  # Run the app with debug mode on
