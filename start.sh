#!/bin/bash
apt-get update && apt-get install -y libgl1-mesa-glx
export CUDA_VISIBLE_DEVICES=""
gunicorn app:app --bind 0.0.0.0:$PORT