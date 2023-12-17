from flask import Flask, render_template, Response,request,jsonify
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

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)
#CORS(app)

capture = False  # Global flag to control capture state
FPS = 5 # default Frames Per Second capture rate
frame_thread = None

def capture_frames():
    cap = cv2.VideoCapture(0)
    frame_count = 0
    while capture:
        ret, frame = cap.read()
        if not ret:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        #encoded_frame = base64.b64encode(frame_bytes).decode('utf-8')

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open("frame_log.txt", "a") as log_file:
            log_file.write(f"Frame {frame_count} captured at {timestamp}\n")
            log_file.write(f"frame_bytes at {timestamp}: {frame_bytes}\n\n")
        socketio.emit('stream_frame', {'frame': frame_bytes, 'timestamp': timestamp})
        socketio.sleep(1.0 / FPS)
        frame_count += 1

    cap.release()

@app.before_request
def before_request():
    print(request.headers)
    data = request.get_data(as_text=True)
    print("the whole request: ", data)

@app.route('/')
def index():
    # The HTML page that will display the video stream
    return render_template('index.html')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    global capture, frame_thread, FPS  # Declare FPS as global here
    data = request.get_json()
    FPS = float(data.get('fps'))
    capture = True
    threading.Thread(target=capture_frames, daemon=True).start()


    # if frame_thread is None or not frame_thread.is_alive():
    #     frame_thread = threading.Thread(target=capture_frames)
    #     frame_thread.start()
    print("capture started")
    return jsonify({"message": "Capture started"})


@app.route('/stop_capture', methods=['POST'])
def stop_capture():
    global capture
    capture = False
    print("capture stopped")
    return jsonify({"message": "Capture stopped"})

@socketio.on('start_stream')
def handle_start_stream(message):
    print("in start stream")
    global capture
    capture = True
    threading.Thread(target=capture_frames, daemon=True).start()

@socketio.on('stop_stream')
def handle_stop_stream(message):
    global capture
    capture = False

if __name__ == "__main__":
    socketio.run(app, debug=True)

