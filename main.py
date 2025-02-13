from flask import Flask, Response, render_template
import subprocess
import os
import threading
import time
import requests

app = Flask(__name__, template_folder="templates")
process = None  # অডিও স্ট্রিম প্রসেস ধরার জন্য ভ্যারিয়েবল

@app.route('/')
def home():
    return render_template("index.html")  # GUI ইন্টারফেস লোড করবে

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

# === Keep Alive Function ===
def keep_server_awake():
    server_url = "https://flask-app-kyhw.onrender.com"  # আপনার Render সার্ভারের URL
    while True:
        try:
            response = requests.get(server_url)
            print(f"Keep-alive request sent to: {server_url}, Status Code: {response.status_code}")
        except Exception as e:
            print(f"Keep-alive request failed: {e}")
        time.sleep(30)  # ৩০ সেকেন্ড পর পর রিকোয়েস্ট পাঠাবে

# === Thread চালু করা হবে Keep Alive এর জন্য ===
threading.Thread(target=keep_server_awake, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)