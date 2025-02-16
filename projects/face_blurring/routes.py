from flask import Blueprint, request, jsonify, send_file
import cv2
import numpy as np
import io
from .face_blur import FaceBlurrer  # Import face-blurring logic

# Define blueprint
face_blurring_bp = Blueprint("face_blurring", __name__)

# Load YOLO model
model_path = "projects/face_blurring/model/best.pt"
face_blurrer = FaceBlurrer(model_path)

@face_blurring_bp.route("/detect_blur", methods=["POST"])
def detect_and_blur():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    image_np = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    blurred_image, face_detected = face_blurrer.detect_and_blur(image)

    if not face_detected:
        return jsonify({"message": "No faces detected", "blurred": False})

    # Convert processed image to bytes (without saving)
    _, buffer = cv2.imencode(".jpg", blurred_image)
    file_bytes = io.BytesIO(buffer)

    return send_file(
        file_bytes,
        mimetype="image/jpeg"
    )
