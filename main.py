
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is Running!"

@app.route('/start')
def start():
    return "Start Command Received"

@app.route('/stop')
def stop():
    return "Stop Command Received"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
