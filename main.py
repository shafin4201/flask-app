from flask import Flask, render_template, jsonify
from flask_sockets import Sockets
import pyaudio
import threading
import time

app = Flask(__name__)
sockets = Sockets(app)

# PyAudio সেটআপ
audio = pyaudio.PyAudio()
streaming = False

def record_audio(ws):
    global streaming
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    
    while streaming:
        data = stream.read(1024)
        ws.send(data)
    
    stream.stop_stream()
    stream.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_stream")
def start_stream():
    global streaming
    streaming = True
    return jsonify({"status": "streaming"})

@app.route("/stop_stream")
def stop_stream():
    global streaming
    streaming = False
    return jsonify({"status": "stopped"})

@sockets.route('/audio')
def audio_socket(ws):
    global streaming
    if streaming:
        thread = threading.Thread(target=record_audio, args=(ws,))
        thread.start()