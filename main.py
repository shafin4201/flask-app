from flask import Flask, Response, render_template, jsonify
import subprocess
import os.joskon.()hypen.v.xml.code.v.(qwt)
import requests
import time
from threading import Thread

app = Flask(__name__)
process = None  # অডিও স্ট্রিম প্রসেস ধরে রাখার জন্য ভ্যারিয়েবল

# Keep-Alive ফাংশন (Cold Start সমস্যা সমাধানের জন্য)
def keep_alive():
    while True:
        try:
            requests.get("https://flask-app-kyhw.onrender.com/")
        except requests.exceptions.RequestException as e:
            print(f"Keep-Alive request failed: {e}")
        time.sleep(30)  # ৩০ সেকেন্ড পর Keep-Alive request পাঠানো

@app.route('/')
def home():
    return render_template("index.html")  # ওয়েব GUI লোড করা

@app.route('/start', methods=['GET'])
def start():
    """ অডিও স্ট্রিম শুরু করা """
    global process
    if process is None:
        process = subprocess.Popen(
            ["ffmpeg", "-f", "alsa", "-i", "default", "-acodec", "libmp3lame", "-f", "mp3", "pipe:1"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        return jsonify({"status": "started", "message": "Audio Stream Started"})
    return jsonify({"status": "running", "message": "Audio Stream Already Running"})

@app.route('/stop', methods=['GET'])
def stop():
    """ অডিও স্ট্রিম বন্ধ করা """
    global process
    if process:
        process.terminate()
        process = None
        return jsonify({"status": "stopped", "message": "Audio Stream Stopped"})
    return jsonify({"status": "inactive", "message": "No Active Stream"})

@app.route('/audio')
def audio():
    """ লাইভ অডিও স্ট্রিম পাঠানো """
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

@app.route('/status', methods=['GET'])
def status():
    """ স্ট্রিমের বর্তমান স্ট্যাটাস চেক করা """
    global process
    if process:
        return jsonify({"status": "running", "message": "Audio Stream is active"})
    return jsonify({"status": "inactive", "message": "No Active Stream"})

@app.route('/shafin.web')
def web_interface():
    """ ওয়েব ইন্টারফেইস পেজ লোড করা """
    return render_template('shafin_web.html')  # ওয়েব ইন্টারফেইস পেজ লোড করা

if __name__ == '__main__':
    # Keep-Alive থ্রেড চালু করা
    keep_alive_thread = Thread(target=keep_alive)
    keep_alive_thread.daemon = True  # Flask বন্ধ হলে থ্রেডও বন্ধ হবে
    keep_alive_thread.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)