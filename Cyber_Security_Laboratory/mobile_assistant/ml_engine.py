#!/usr/bin/env python3
import json
import numpy as np
from datetime import datetime, timedelta
import pickle

class MLEngine:
    def __init__(self):
        self.user_patterns = {}
        self.threat_patterns = []
        self.command_history = []
        self.security_events = []
        
    def learn_user_behavior(self, action, context):
        """Обучение поведению пользователя"""
        timestamp = datetime.now()
        hour = timestamp.hour
        
        if action not in self.user_patterns:
            self.user_patterns[action] = {
                'frequency': 0,
                'time_patterns': [0] * 24,
                'contexts': {}
            }
        
        self.user_patterns[action]['frequency'] += 1
        self.user_patterns[action]['time_patterns'][hour] += 1
        
        if context not in self.user_patterns[action]['contexts']:
            self.user_patterns[action]['contexts'][context] = 0
        self.user_patterns[action]['contexts'][context] += 1
    
    def predict_next_action(self):
        """Предсказание следующего действия пользователя"""
        current_hour = datetime.now().hour
        
        best_action = None
        best_score = 0
        
        for action, pattern in self.user_patterns.items():
            # Вероятность на основе времени
            time_score = pattern['time_patterns'][current_hour]
            # Общая частота
            freq_score = pattern['frequency']
            
            total_score = time_score * 0.7 + freq_score * 0.3
            
            if total_score > best_score:
                best_score = total_score
                best_action = action
        
        return best_action, best_score
    
    def analyze_security_threat(self, app_name, permissions, network_activity):
        """Анализ угроз безопасности с помощью ML"""
        threat_score = 0
        
        # Анализ разрешений
        dangerous_permissions = [
            'READ_CONTACTS', 'ACCESS_FINE_LOCATION', 'CAMERA',
            'RECORD_AUDIO', 'READ_SMS', 'CALL_PHONE'
        ]
        
        for perm in permissions:
            if perm in dangerous_permissions:
                threat_score += 10
        
        # Анализ сетевой активности
        if network_activity > 100:  # MB
            threat_score += 20
        
        # Анализ имени приложения
        suspicious_keywords = ['hack', 'crack', 'free', 'premium']
        for keyword in suspicious_keywords:
            if keyword in app_name.lower():
                threat_score += 15
        
        # Классификация угрозы
        if threat_score > 50:
            return "HIGH", threat_score
        elif threat_score > 25:
            return "MEDIUM", threat_score
        else:
            return "LOW", threat_score
    
    def learn_voice_command(self, audio_features, command_text):
        """Обучение голосовым командам"""
        command_data = {
            'features': audio_features,
            'text': command_text,
            'timestamp': datetime.now().isoformat()
        }
        
        self.command_history.append(command_data)
        
        # Ограничиваем историю последними 1000 командами
        if len(self.command_history) > 1000:
            self.command_history = self.command_history[-1000:]
    
    def recognize_voice_pattern(self, audio_features):
        """Распознавание паттернов голоса"""
        if not self.command_history:
            return None, 0
        
        # Простое сравнение с историей команд
        best_match = None
        best_similarity = 0
        
        for cmd in self.command_history[-100:]:  # Последние 100 команд
            similarity = self._calculate_similarity(audio_features, cmd['features'])
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = cmd['text']
        
        return best_match, best_similarity
    
    def _calculate_similarity(self, features1, features2):
        """Вычисление схожести аудио-признаков"""
        if not features1 or not features2:
            return 0
        
        # Простая корреляция
        try:
            correlation = np.corrcoef(features1, features2)[0, 1]
            return abs(correlation) if not np.isnan(correlation) else 0
        except:
            return 0
    
    def adaptive_security_level(self):
        """Адаптивный уровень безопасности"""
        recent_threats = [
            event for event in self.security_events 
            if datetime.fromisoformat(event['timestamp']) > datetime.now() - timedelta(hours=24)
        ]
        
        if len(recent_threats) > 5:
            return "HIGH"
        elif len(recent_threats) > 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def log_security_event(self, event_type, details):
        """Логирование событий безопасности"""
        event = {
            'type': event_type,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        
        self.security_events.append(event)
        
        # Ограничиваем историю
        if len(self.security_events) > 500:
            self.security_events = self.security_events[-500:]
    
    def get_recommendations(self):
        """Получение рекомендаций на основе ML"""
        recommendations = []
        
        # Рекомендации на основе поведения
        next_action, confidence = self.predict_next_action()
        if next_action and confidence > 5:
            recommendations.append(f"Возможно, вы хотите выполнить: {next_action}")
        
        # Рекомендации по безопасности
        security_level = self.adaptive_security_level()
        if security_level == "HIGH":
            recommendations.append("Рекомендуется полное сканирование системы")
        
        return recommendations
    
    def save_model(self, filename="ml_model.pkl"):
        """Сохранение модели ML"""
        model_data = {
            'user_patterns': self.user_patterns,
            'command_history': self.command_history[-100:],  # Последние 100
            'security_events': self.security_events[-100:]   # Последние 100
        }
        
        try:
            with open(filename, 'wb') as f:
                pickle.dump(model_data, f)
            return True
        except:
            return False
    
    def load_model(self, filename="ml_model.pkl"):
        """Загрузка модели ML"""
        try:
            with open(filename, 'rb') as f:
                model_data = pickle.load(f)
            
            self.user_patterns = model_data.get('user_patterns', {})
            self.command_history = model_data.get('command_history', [])
            self.security_events = model_data.get('security_events', [])
            return True
        except:
            return False