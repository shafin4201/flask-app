#!/bin/bash
apt-get update && apt-get install -y ffmpeg
gunicorn main:app
