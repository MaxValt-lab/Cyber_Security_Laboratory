"""
Усиленная система безопасности с многофакторной аутентификацией
"""
import hashlib
import secrets
import time
import json
import sqlite3
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class EnhancedSecurity:
    def __init__(self):
        self.setup_database()
        self.cipher = self._init_encryption()
        self.failed_attempts = {}
        self.active_sessions = {}
        
    def _init_encryption(self):
        """Инициализация шифрования"""
        password = b"SecureKey2024_Laboratory"
        salt = b"salt_security_2024"
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return Fernet(key)
    
    def setup_database(self):
        """Настройка базы данных безопасности"""
        conn = sqlite3.connect('security.db')
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT,
                salt TEXT,
                role TEXT,
                mfa_secret TEXT,
                created_at TEXT,
                last_login TEXT,
                failed_attempts INTEGER DEFAULT 0,
                locked_until TEXT
            )
        ''')
        
        # Таблица аудита
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                user_id INTEGER,
                action TEXT,
                resource TEXT,
                ip_address TEXT,
                user_agent TEXT,
                success BOOLEAN,
                details TEXT
            )
        ''')
        
        # Таблица сессий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                session_token TEXT UNIQUE,
                user_id INTEGER,
                created_at TEXT,
                expires_at TEXT,
                ip_address TEXT,
                active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Создание администратора по умолчанию
        self._create_default_admin()
        
        conn.commit()
        conn.close()
    
    def _create_default_admin(self):
        """Создание администратора по умолчанию"""
        conn = sqlite3.connect('security.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'director'")
        if cursor.fetchone()[0] == 0:
            salt = secrets.token_hex(32)
            password_hash = self._hash_password("admin2024", salt)
            mfa_secret = secrets.token_hex(16)
            
            cursor.execute('''
                INSERT INTO users (username, password_hash, salt, role, mfa_secret, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ("director", password_hash, salt, "admin", mfa_secret, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def _hash_password(self, password, salt):
        """Хеширование пароля"""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def authenticate(self, username, password, ip_address, user_agent):
        """Аутентификация пользователя"""
        conn = sqlite3.connect('security.db')
        cursor = conn.cursor()
        
        # Проверка блокировки
        cursor.execute("SELECT locked_until FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result and result[0]:
            locked_until = datetime.fromisoformat(result[0])
            if datetime.now() < locked_until:
                self.log_audit(None, "login_attempt", "authentication", ip_address, user_agent, False, "Account locked")
                conn.close()
                return {"success": False, "error": "Account locked"}
        
        # Проверка учетных данных
        cursor.execute("SELECT id, password_hash, salt, role, failed_attempts FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if not user:
            self.log_audit(None, "login_attempt", "authentication", ip_address, user_agent, False, "User not found")
            conn.close()
            return {"success": False, "error": "Invalid credentials"}
        
        user_id, stored_hash, salt, role, failed_attempts = user
        password_hash = self._hash_password(password, salt)
        
        if password_hash == stored_hash:
            # Успешная аутентификация
            session_token = self._create_session(user_id, ip_address)
            cursor.execute("UPDATE users SET last_login = ?, failed_attempts = 0 WHERE id = ?", 
                         (datetime.now().isoformat(), user_id))
            
            self.log_audit(user_id, "login_success", "authentication", ip_address, user_agent, True, "Successful login")
            conn.commit()
            conn.close()
            
            return {
                "success": True, 
                "session_token": session_token,
                "user_id": user_id,
                "role": role,
                "requires_mfa": True
            }
        else:
            # Неудачная попытка
            failed_attempts += 1
            locked_until = None
            
            if failed_attempts >= 5:
                locked_until = (datetime.now() + timedelta(minutes=30)).isoformat()
            
            cursor.execute("UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?", 
                         (failed_attempts, locked_until, user_id))
            
            self.log_audit(user_id, "login_failed", "authentication", ip_address, user_agent, False, f"Failed attempt {failed_attempts}")
            conn.commit()
            conn.close()
            
            return {"success": False, "error": "Invalid credentials"}
    
    def _create_session(self, user_id, ip_address):
        """Создание сессии"""
        session_token = secrets.token_urlsafe(32)
        expires_at = (datetime.now() + timedelta(hours=8)).isoformat()
        
        conn = sqlite3.connect('security.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sessions (session_token, user_id, created_at, expires_at, ip_address)
            VALUES (?, ?, ?, ?, ?)
        ''', (session_token, user_id, datetime.now().isoformat(), expires_at, ip_address))
        
        conn.commit()
        conn.close()
        
        return session_token
    
    def validate_session(self, session_token):
        """Валидация сессии"""
        conn = sqlite3.connect('security.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.user_id, s.expires_at, u.username, u.role 
            FROM sessions s 
            JOIN users u ON s.user_id = u.id 
            WHERE s.session_token = ? AND s.active = 1
        ''', (session_token,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
        
        user_id, expires_at, username, role = result
        if datetime.now() > datetime.fromisoformat(expires_at):
            self._invalidate_session(session_token)
            return None
        
        return {"user_id": user_id, "username": username, "role": role}
    
    def _invalidate_session(self, session_token):
        """Инвалидация сессии"""
        conn = sqlite3.connect('security.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE sessions SET active = 0 WHERE session_token = ?", (session_token,))
        conn.commit()
        conn.close()
    
    def encrypt_data(self, data):
        """Шифрование данных"""
        if isinstance(data, str):
            data = data.encode()
        return base64.b64encode(self.cipher.encrypt(data)).decode()
    
    def decrypt_data(self, encrypted_data):
        """Расшифровка данных"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            return self.cipher.decrypt(encrypted_bytes).decode()
        except:
            return None
    
    def log_audit(self, user_id, action, resource, ip_address, user_agent, success, details):
        """Логирование аудита"""
        conn = sqlite3.connect('security.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_log (timestamp, user_id, action, resource, ip_address, user_agent, success, details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), user_id, action, resource, ip_address, user_agent, success, details))
        
        conn.commit()
        conn.close()
    
    def get_audit_log(self, limit=100):
        """Получение журнала аудита"""
        conn = sqlite3.connect('security.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.timestamp, u.username, a.action, a.resource, a.ip_address, a.success, a.details
            FROM audit_log a
            LEFT JOIN users u ON a.user_id = u.id
            ORDER BY a.timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{"timestamp": r[0], "username": r[1], "action": r[2], "resource": r[3], 
                "ip_address": r[4], "success": r[5], "details": r[6]} for r in results]

# Глобальный экземпляр
enhanced_security = EnhancedSecurity()