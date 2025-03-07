from flask import Flask, render_template, jsonify, Response
from flask_sockets import Sockets
import pyaudio
import threading

app = Flask(__name__)
sockets = Sockets(app)

# স্ট্রিম স্ট্যাটাস ট্র্যাক করা
streaming = False

# PyAudio সেটআপ
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

audio = pyaudio.PyAudio()

def generate_audio():
    """ মাইক্রোফোন থেকে অডিও ক্যাপচার করা """
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    while streaming:
        data = stream.read(CHUNK)
        yield data
    stream.stop_stream()
    stream.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_stream():
    global streaming
    streaming = True
    return jsonify({"message": "Streaming started"})

@app.route('/stop', methods=['GET'])
def stop_stream():
    global streaming
    streaming = False
    return jsonify({"message": "Streaming stopped"})

@app.route('/status', methods=['GET'])
def check_status():
    status = "running" if streaming else "stopped"
    return jsonify({"message": status, "status": status})

@sockets.route('/audio')
def audio_stream(ws):
    """ WebSocket দিয়ে লাইভ অডিও স্ট্রিম করা """
    while not ws.closed and streaming:
        audio_data = next(generate_audio())
        ws.send(audio_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)