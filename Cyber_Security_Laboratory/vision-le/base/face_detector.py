"""
Base face recognition module for the Cyber Security Laboratory.
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional

class FaceDetector:
    def __init__(self, model_path: str = "models/face_detection_model.xml"):
        """Initialize the face detector."""
        self.face_cascade = cv2.CascadeClassifier(model_path)
        
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in the image.
        Returns list of (x, y, w, h) coordinates for each face.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces.tolist()
    
    def draw_faces(self, image: np.ndarray, faces: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """Draw rectangles around detected faces."""
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return image
    
    def process_video_stream(self, source: int = 0) -> None:
        """Process video stream and detect faces in real-time."""
        cap = cv2.VideoCapture(source)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            faces = self.detect_faces(frame)
            frame = self.draw_faces(frame, faces)
            
            cv2.imshow('Face Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()