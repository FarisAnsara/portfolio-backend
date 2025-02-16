export CUDA_VISIBLE_DEVICES=""
gunicorn app:app --bind 0.0.0.0:$PORT