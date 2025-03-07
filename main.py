import asyncio
import json
from aiortc import RTCPeerConnection, MediaStreamTrack
from aiortc.mediastreams import AudioFrame
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
pcs = set()

class AudioStreamTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self):
        super().__init__()

    async def recv(self):
        return AudioFrame.from_ndarray(b'\x00' * 1024)  # Dummy audio frame (to prevent errors)

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