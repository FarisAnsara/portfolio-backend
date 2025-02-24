import os
import cv2
import numpy as np
from ultralytics import YOLO

class FaceBlurrer:
    def __init__(self, model_path, conf=0.325):
        """
        Initializes the FaceBlurrer class.

        Args:
            model_path (str): Path to the YOLO model weights.
            conf (float): Confidence threshold for detection.
            device (int): Device to use for inference (0 for GPU, -1 for CPU).
        """
        if not os.path.exists(model_path):
            raise ValueError(f"Model file not found at {model_path}")

        self.device = 'cpu'
        self.model = YOLO(model_path).to(self.device)
        self.conf = conf
        self.device = 'cpu'

    def detect_and_blur(self, image):
        """
        Detects faces in an image and applies blurring.

        Args:
            image (numpy.ndarray): Input image.

        Returns:
            tuple: (blurred_image, boolean indicating if faces were detected)
        """
        results = self.model.predict(image, conf=self.conf, device=self.device)
        detections = results[0].boxes.data.cpu().numpy()

        if len(detections) == 0:
            return image, False  # No faces detected

        for detection in detections:
            x_min, y_min, x_max, y_max = map(int, detection[:4])
            face_region = image[y_min:y_max, x_min:x_max]
            blurred_face = cv2.GaussianBlur(face_region, (99, 99), 0)
            image[y_min:y_max, x_min:x_max] = blurred_face

        return image, True  # Faces were detected and blurred
