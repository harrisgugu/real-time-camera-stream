import socketio
import logging
import os

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Create a SocketIO client instance
sio = socketio.Client(logger=True, engineio_logger=True)
frame_count = 0

@sio.event
def connect():
    print("Connected to the server.")
    print("My SID is", sio.sid)

@sio.event
def disconnect():
    print("Disconnected from the server.")

@sio.event
def message(data):
    print('Received a message:', data)

@sio.on('stream_frame')
def handle_stream_frame(data):
    global frame_count
    print("Received a stream frame")
    if not os.path.exists('frames_client_side'):
        os.makedirs('frames_client_side')
    frame_filename = f"frames_client_side/frame_{frame_count}.jpg"
    with open(frame_filename, "wb") as frame_file:
        frame_file.write(data['frame'])
    with open("client_side_frame_log.txt", "a") as log_file:
        log_file.write(f"Frame {frame_count} received at {data['timestamp']}\n")
        log_file.write(f"Frame: {data['frame']}\n\n")
    frame_count += 1

# Connect to the server
sio.connect('http://127.0.0.1:5000')

# Keep the script running to maintain the connection
try:
    sio.wait()
except KeyboardInterrupt:
    print("Interrupted by user, disconnecting...")
    sio.disconnect()
