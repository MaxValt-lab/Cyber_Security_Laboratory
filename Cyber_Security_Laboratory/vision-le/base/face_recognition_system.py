"""
Advanced Face Recognition Module for Cyber_Security_Laboratory
Author: MaxValt-lab
Copyright (c) 2025
"""

from ..common.src.code_protector import CodeProtector
from ..common.src.module_protection import protection_system
import cv2
import numpy as np
from typing import List, Tuple, Dict, Any
import tensorflow as tf
from pathlib import Path
import json
import logging

class FaceRecognitionSystem:
    def __init__(self, model_path: str = None):
        # Инициализируем защиту
        self._protector = CodeProtector()
        protection_system.register_module(__file__, ['code_protector', 'module_protection'])
        
        # Защищенный код инициализации
        init_code = """
self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
self.model = self._load_model(model_path) if model_path else None
self.face_embeddings = {}
self.threshold = 0.6
self.min_face_size = (30, 30)
self.logger = logging.getLogger(__name__)
"""
        # Внедряем защищенный код
        exec(self._protector.protect_code_section('init', init_code))
        
    def _load_model(self, model_path: str) -> tf.keras.Model:
        """Загружает модель распознавания лиц."""
        protected_code = """
try:
    model = tf.keras.models.load_model(model_path)
    self.logger.info(f"Model loaded successfully from {model_path}")
    return model
except Exception as e:
    self.logger.error(f"Failed to load model: {str(e)}")
    raise
"""
        return exec(self._protector.protect_code_section('load_model', protected_code))
        
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Обнаруживает лица на изображении."""
        protected_code = """
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = self.face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=self.min_face_size
)
return faces.tolist() if len(faces) > 0 else []
"""
        return exec(self._protector.protect_code_section('detect_faces', protected_code))
        
    def extract_face_embedding(self, image: np.ndarray, face_location: Tuple[int, int, int, int]) -> np.ndarray:
        """Извлекает эмбеддинг лица для распознавания."""
        protected_code = """
if not self.model:
    raise ValueError("Model not loaded")
    
x, y, w, h = face_location
face = image[y:y+h, x:x+w]
face = cv2.resize(face, (160, 160))
face = face.astype('float32') / 255.0
face = np.expand_dims(face, axis=0)
return self.model.predict(face)[0]
"""
        return exec(self._protector.protect_code_section('extract_embedding', protected_code))
        
    def register_face(self, image: np.ndarray, person_id: str) -> bool:
        """Регистрирует новое лицо в системе."""
        protected_code = """
faces = self.detect_faces(image)
if not faces:
    self.logger.warning(f"No face detected for person {person_id}")
    return False
    
# Используем самое большое лицо на изображении
face = max(faces, key=lambda x: x[2] * x[3])
embedding = self.extract_face_embedding(image, face)
self.face_embeddings[person_id] = embedding
self.logger.info(f"Face registered for person {person_id}")
return True
"""
        return exec(self._protector.protect_code_section('register_face', protected_code))
        
    def recognize_face(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Распознает лица на изображении."""
        protected_code = """
faces = self.detect_faces(image)
results = []

for face in faces:
    embedding = self.extract_face_embedding(image, face)
    best_match = None
    best_distance = float('inf')
    
    for person_id, stored_embedding in self.face_embeddings.items():
        distance = np.linalg.norm(embedding - stored_embedding)
        if distance < best_distance and distance < self.threshold:
            best_distance = distance
            best_match = person_id
            
    results.append({
        'location': face,
        'person_id': best_match,
        'confidence': 1 - (best_distance / self.threshold) if best_match else 0
    })

return results
"""
        return exec(self._protector.protect_code_section('recognize_face', protected_code))
        
    def save_database(self, path: str) -> None:
        """Сохраняет базу данных лиц."""
        protected_code = """
data = {
    'embeddings': {k: v.tolist() for k, v in self.face_embeddings.items()},
    'threshold': self.threshold
}
with open(path, 'w') as f:
    json.dump(data, f)
self.logger.info(f"Face database saved to {path}")
"""
        return exec(self._protector.protect_code_section('save_database', protected_code))
        
    def load_database(self, path: str) -> None:
        """Загружает базу данных лиц."""
        protected_code = """
with open(path, 'r') as f:
    data = json.load(f)
self.face_embeddings = {k: np.array(v) for k, v in data['embeddings'].items()}
self.threshold = data['threshold']
self.logger.info(f"Face database loaded from {path}")
"""
        return exec(self._protector.protect_code_section('load_database', protected_code))