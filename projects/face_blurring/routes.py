from flask import Blueprint, request, jsonify, send_from_directory
import cv2
import numpy as np
import os
from .face_blur import FaceBlurrer  # Import face-blurring logic

# Define blueprint
face_blurring_bp = Blueprint("face_blurring", __name__)

# Load YOLO model
model_path = os.path.join("projects", "face_blurring", "model", "best.pt")
face_blurrer = FaceBlurrer(model_path)

# Ensure static folder exists to store output images
STATIC_FOLDER = "static"
os.makedirs(STATIC_FOLDER, exist_ok=True)

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

    # Generate unique output filename
    output_filename = f"blurred_{file.filename}"
    output_path = os.path.join(STATIC_FOLDER, output_filename)
    cv2.imwrite(output_path, blurred_image)

    return jsonify({
        "message": "Faces blurred successfully",
        "blurred": True,
        "image_url": f"/api/static/{output_filename}"
    })

@face_blurring_bp.route("/static/<filename>")
def serve_static(filename):
    return send_from_directory(STATIC_FOLDER, filename)
