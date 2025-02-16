#!/bin/bash
# apt-get update && apt-get install -y libgl1-mesa-glx
gunicorn app:app --bind 0.0.0.0:$PORT
