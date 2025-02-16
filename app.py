from flask import Flask
from flask_cors import CORS
from projects.face_blurring.routes import face_blurring_bp

app = Flask(__name__)
CORS(app)  # Allow frontend to access API

# Register routes
app.register_blueprint(face_blurring_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)  # Ensures API is accessible
