"""
Система защиты данных с шифрованием и контролем доступа
"""
import sqlite3
import json
import hashlib
import time
from datetime import datetime, timedelta
from security_core import security_core
import logging

class DataProtection:
    def __init__(self):
        self.access_log = []
        self.failed_attempts = {}
        self.max_failed_attempts = 5
        self.lockout_duration = 300  # 5 минут
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def secure_query(self, db_path, query, params=None, user_id=None):
        """Безопасное выполнение запроса с аудитом"""
        try:
            # Проверка блокировки пользователя
            if self.is_user_locked(user_id):
                self.logger.warning(f"Blocked query attempt from locked user: {user_id}")
                return None
            
            # Валидация запроса
            if not self.validate_query(query):
                self.record_failed_attempt(user_id)
                self.logger.warning(f"Invalid query blocked: {query[:50]}...")
                return None
            
            # Выполнение запроса
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            conn.commit()
            conn.close()
            
            # Аудит успешного запроса
            self.log_access(user_id, query, "SUCCESS")
            
            return result
            
        except Exception as e:
            self.record_failed_attempt(user_id)
            self.log_access(user_id, query, f"ERROR: {e}")
            self.logger.error(f"Query failed: {e}")
            return None
    
    def validate_query(self, query):
        """Валидация SQL запроса"""
        dangerous_keywords = [
            'DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE',
            'EXEC', 'EXECUTE', 'UNION', 'SCRIPT', '--'
        ]
        
        query_upper = query.upper()
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False
        
        return True
    
    def is_user_locked(self, user_id):
        """Проверка блокировки пользователя"""
        if not user_id or user_id not in self.failed_attempts:
            return False
        
        attempts = self.failed_attempts[user_id]
        if attempts['count'] >= self.max_failed_attempts:
            if time.time() - attempts['last_attempt'] < self.lockout_duration:
                return True
            else:
                # Сброс счетчика после истечения блокировки
                del self.failed_attempts[user_id]
        
        return False
    
    def record_failed_attempt(self, user_id):
        """Запись неудачной попытки"""
        if not user_id:
            return
        
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = {'count': 0, 'last_attempt': 0}
        
        self.failed_attempts[user_id]['count'] += 1
        self.failed_attempts[user_id]['last_attempt'] = time.time()
        
        if self.failed_attempts[user_id]['count'] >= self.max_failed_attempts:
            self.logger.warning(f"User {user_id} locked due to failed attempts")
            security_core.audit_log("user_locked", user_id, {
                "reason": "too_many_failed_attempts",
                "count": self.failed_attempts[user_id]['count']
            })
    
    def log_access(self, user_id, query, status):
        """Логирование доступа к данным"""
        access_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "query_hash": hashlib.sha256(query.encode()).hexdigest()[:16],
            "status": status
        }
        
        self.access_log.append(access_entry)
        
        # Ограничение размера лога
        if len(self.access_log) > 1000:
            self.access_log = self.access_log[-500:]
    
    def encrypt_sensitive_data(self, data, field_name):
        """Шифрование чувствительных данных"""
        sensitive_fields = ['password', 'token', 'key', 'secret', 'credit_card']
        
        if any(field in field_name.lower() for field in sensitive_fields):
            return security_core.encrypt_data(str(data)).decode('latin-1')
        
        return data
    
    def decrypt_sensitive_data(self, data, field_name):
        """Расшифровка чувствительных данных"""
        sensitive_fields = ['password', 'token', 'key', 'secret', 'credit_card']
        
        if any(field in field_name.lower() for field in sensitive_fields):
            try:
                return security_core.decrypt_data(data.encode('latin-1'))
            except:
                return data
        
        return data
    
    def sanitize_output(self, data):
        """Очистка вывода от чувствительных данных"""
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                if any(sensitive in key.lower() for sensitive in ['password', 'token', 'secret']):
                    sanitized[key] = "***HIDDEN***"
                else:
                    sanitized[key] = self.sanitize_output(value)
            return sanitized
        elif isinstance(data, list):
            return [self.sanitize_output(item) for item in data]
        else:
            return data
    
    def get_access_report(self):
        """Отчет о доступе к данным"""
        return {
            "total_accesses": len(self.access_log),
            "recent_accesses": self.access_log[-10:],
            "locked_users": list(self.failed_attempts.keys()),
            "timestamp": datetime.now().isoformat()
        }

# Глобальный экземпляр
data_protection = DataProtection()