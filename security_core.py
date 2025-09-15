"""
Усиленная система защиты данных и отказоустойчивости
"""
import os
import sqlite3
import json
import hashlib
import time
import threading
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import shutil
import logging

class SecurityCore:
    def __init__(self, master_key=None):
        self.master_key = master_key or os.environ.get('MASTER_KEY', 'default_key_2024')
        self.cipher_suite = self._init_encryption()
        self.backup_interval = 300  # 5 минут
        self.max_backups = 10
        self.setup_logging()
        self.start_background_tasks()
    
    def _init_encryption(self):
        """Инициализация шифрования"""
        password = self.master_key.encode()
        salt = b'salt_2024_secure'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return Fernet(key)
    
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('security.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def encrypt_data(self, data):
        """Шифрование данных"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher_suite.encrypt(data)
    
    def decrypt_data(self, encrypted_data):
        """Расшифровка данных"""
        return self.cipher_suite.decrypt(encrypted_data).decode()
    
    def secure_database_connection(self, db_path):
        """Безопасное подключение к БД с шифрованием"""
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA key = ?", (self.master_key,))
        return conn
    
    def backup_database(self, db_path):
        """Создание резервной копии БД"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_path = os.path.join(backup_dir, f"backup_{timestamp}.db")
            shutil.copy2(db_path, backup_path)
            
            # Шифрование резервной копии
            with open(backup_path, 'rb') as f:
                encrypted_data = self.encrypt_data(f.read())
            
            with open(f"{backup_path}.enc", 'wb') as f:
                f.write(encrypted_data)
            
            os.remove(backup_path)  # Удаляем незашифрованную копию
            
            self.cleanup_old_backups(backup_dir)
            self.logger.info(f"Backup created: {backup_path}.enc")
            
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
    
    def cleanup_old_backups(self, backup_dir):
        """Очистка старых резервных копий"""
        backups = [f for f in os.listdir(backup_dir) if f.endswith('.enc')]
        backups.sort(reverse=True)
        
        for backup in backups[self.max_backups:]:
            os.remove(os.path.join(backup_dir, backup))
            self.logger.info(f"Old backup removed: {backup}")
    
    def restore_database(self, backup_path, restore_path):
        """Восстановление БД из резервной копии"""
        try:
            with open(backup_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            
            with open(restore_path, 'wb') as f:
                f.write(decrypted_data)
            
            self.logger.info(f"Database restored from {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Restore failed: {e}")
            return False
    
    def health_check(self, db_paths):
        """Проверка состояния БД"""
        results = {}
        for db_path in db_paths:
            try:
                conn = sqlite3.connect(db_path)
                conn.execute("SELECT 1")
                conn.close()
                results[db_path] = "OK"
            except Exception as e:
                results[db_path] = f"ERROR: {e}"
                self.logger.error(f"Health check failed for {db_path}: {e}")
        return results
    
    def start_background_tasks(self):
        """Запуск фоновых задач"""
        def backup_task():
            while True:
                time.sleep(self.backup_interval)
                db_paths = [
                    "director_system.db",
                    "general_system.db",
                    "cyberlab.db"
                ]
                for db_path in db_paths:
                    if os.path.exists(db_path):
                        self.backup_database(db_path)
        
        backup_thread = threading.Thread(target=backup_task, daemon=True)
        backup_thread.start()
    
    def audit_log(self, action, user, details):
        """Аудит действий"""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user": user,
            "details": details,
            "hash": hashlib.sha256(f"{action}{user}{details}".encode()).hexdigest()
        }
        
        with open("audit.log", "a") as f:
            f.write(json.dumps(audit_entry) + "\n")
    
    def validate_session(self, token, max_age_hours=24):
        """Валидация сессии"""
        try:
            decrypted = self.decrypt_data(base64.b64decode(token))
            session_data = json.loads(decrypted)
            
            session_time = datetime.fromisoformat(session_data['timestamp'])
            if datetime.now() - session_time > timedelta(hours=max_age_hours):
                return False
            
            return session_data
        except:
            return False
    
    def create_session(self, user_data):
        """Создание защищенной сессии"""
        session_data = {
            "user": user_data,
            "timestamp": datetime.now().isoformat(),
            "nonce": os.urandom(16).hex()
        }
        
        encrypted = self.encrypt_data(json.dumps(session_data))
        return base64.b64encode(encrypted).decode()

# Глобальный экземпляр
security_core = SecurityCore()