#!/usr/bin/env bash
# 1. start the bot in the background
python src/main.py &

# 2. start the web server in the foreground (so Render sees the port)
exec gunicorn app:app -b 0.0.0.0:$PORT
