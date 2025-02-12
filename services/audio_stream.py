import subprocess

def start_audio_stream():
    return subprocess.Popen(
        ["ffmpeg", "-f", "alsa", "-i", "default", "-acodec", "libmp3lame", "-f", "mp3", "pipe:1"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )

def stop_audio_stream(process):
    if process:
        process.terminate()