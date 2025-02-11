from flask import Flask, Response, render_template
import subprocess
import os
import requests
import time
from threading import Thread

app = Flask(__name__)
process = None  # অডিও স্ট্রিম প্রসেস ধরে রাখার জন্য ভ্যারিয়েবল

def keep_alive():
    while True:
        try:
            requests.get("https://flask-app-kyhw.onrender.com/")
        except requests.exceptions.RequestException as e:
            print(f"Keep-Alive request failed: {e}")
        time.sleep(30)  # ৩০ সেকেন্ড পর Keep-Alive request পাঠানো

@app.route('/')
def home():
    return render_template("index.html")  # GUI ইন্টারফেস লোড করা

@app.route('/start')
def start():
    global process
    if process is None:
        process = subprocess.Popen(
            ["ffmpeg", "-f", "alsa", "-i", "default", "-acodec", "libmp3lame", "-f", "mp3", "pipe:1"],
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

@app.route('/audio')
def audio():
    def generate():
        global process
        if process:
            while True:
                data = process.stdout.read(1024)
                if not data:
                    break
                yield data
        else:
            yield b''

    return Response(generate(), mimetype="audio/mpeg")

if __name__ == '__main__':
    # Keep-Alive থ্রেড শুরু করা
    keep_alive_thread = Thread(target=keep_alive)
    keep_alive_thread.daemon = True  # থ্রেডটি অ্যাপ বন্ধ হলে বন্ধ হয়ে যাবে
    keep_alive_thread.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
