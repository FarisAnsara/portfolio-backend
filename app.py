from flask import Flask
from flask_cors import CORS
from projects.face_blurring.routes import face_blurring_bp
import os

STATIC_FOLDER = "static"
os.makedirs(STATIC_FOLDER, exist_ok=True) 

app = Flask(__name__)
CORS(app)

app.register_blueprint(face_blurring_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
