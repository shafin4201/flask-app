import asyncio
import json
import pyaudio
from aiortc import RTCPeerConnection, MediaStreamTrack
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
pcs = set()

class AudioStreamTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self):
        super().__init__()
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    async def recv(self):
        frame = self.stream.read(1024)
        return frame

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/offer", methods=["POST"])
async def offer():
    params = await request.get_json()
    pc = RTCPeerConnection()
    pcs.add(pc)
    pc.addTrack(AudioStreamTrack())

    await pc.setRemoteDescription(params["offer"])
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return jsonify({"answer": pc.localDescription})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)