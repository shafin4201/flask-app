from flask import Flask, Response
import subprocess
import os

app = Flask(__name__)
process = None  # অডিও স্ট্রিম প্রসেস ধরে রাখার জন্য ভ্যারিয়েবল

@app.route('/')
def home():
    return "Server is Running!"

@app.route('/start')
def start():
    global process
    if process is None:
        process = subprocess.Popen(
            ["ffmpeg", "-f", "avfoundation", "-i", ":0", "-acodec", "libmp3lame", "-f", "mp3", "pipe:1"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        return "Audio Stream Started"
    return "Audio Stream Already Running"

@app.route('/stop')
def stop():
    global process
    if process:
        process.terminate()
        process = None
        return "Audio Stream Stopped"
    return "No Active Stream"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
