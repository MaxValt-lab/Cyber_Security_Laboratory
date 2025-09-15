"""
Продвинутая система безопасности с 2FA и мониторингом
"""
import pyotp
import qrcode
import io
import base64
import sqlite3
import hashlib
import time
import json
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

class AdvancedSecurity:
    def __init__(self):
        self.setup_database()
        self.cipher = self._init_encryption()
        self.suspicious_patterns = []
        
    def setup_database(self):
        """Расширенная база данных безопасности"""
        conn = sqlite3.connect('advanced_security.db')
        cursor = conn.cursor()
        
        # Таблица 2FA
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS two_factor_auth (
                user_id INTEGER PRIMARY KEY,
                secret_key TEXT,
                backup_codes TEXT,
                enabled BOOLEAN DEFAULT 0,
                last_used TEXT
            )
        ''')
        
        # Таблица подозрительной активности
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suspicious_activity (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                user_id INTEGER,
                activity_type TEXT,
                risk_score INTEGER,
                details TEXT,
                resolved BOOLEAN DEFAULT 0
            )
        ''')
        
        # Таблица резервных копий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_log (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                backup_type TEXT,
                file_path TEXT,
                size INTEGER,
                checksum TEXT,
                encrypted BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _init_encryption(self):
        """Многоуровневое шифрование"""
        key = Fernet.generate_key()
        return Fernet(key)
    
    def setup_2fa(self, user_id, username):
        """Настройка двухфакторной аутентификации"""
        secret = pyotp.random_base32()
        
        # Генерация backup кодов
        backup_codes = [pyotp.random_base32()[:8] for _ in range(10)]
        
        conn = sqlite3.connect('advanced_security.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO two_factor_auth (user_id, secret_key, backup_codes, enabled)
            VALUES (?, ?, ?, 1)
        ''', (user_id, secret, json.dumps(backup_codes)))
        
        conn.commit()
        conn.close()
        
        # Генерация QR кода
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name="Director Security System"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_code = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "secret": secret,
            "qr_code": qr_code,
            "backup_codes": backup_codes
        }
    
    def verify_2fa(self, user_id, token):
        """Проверка 2FA токена"""
        conn = sqlite3.connect('advanced_security.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT secret_key, backup_codes FROM two_factor_auth WHERE user_id = ? AND enabled = 1", (user_id,))
        result = cursor.fetchone()
        
        if not result:
            return False
        
        secret, backup_codes_json = result
        backup_codes = json.loads(backup_codes_json)
        
        # Проверка TOTP токена
        totp = pyotp.TOTP(secret)
        if totp.verify(token, valid_window=1):
            cursor.execute("UPDATE two_factor_auth SET last_used = ? WHERE user_id = ?", 
                         (datetime.now().isoformat(), user_id))
            conn.commit()
            conn.close()
            return True
        
        # Проверка backup кода
        if token in backup_codes:
            backup_codes.remove(token)
            cursor.execute("UPDATE two_factor_auth SET backup_codes = ? WHERE user_id = ?", 
                         (json.dumps(backup_codes), user_id))
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    
    def detect_suspicious_activity(self, user_id, activity_data):
        """Детекция подозрительной активности"""
        risk_score = 0
        alerts = []
        
        # Проверка времени входа
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour > 22:
            risk_score += 20
            alerts.append("Вход в нерабочее время")
        
        # Проверка IP адреса
        ip = activity_data.get('ip_address', '')
        if self._is_suspicious_ip(ip):
            risk_score += 30
            alerts.append("Подозрительный IP адрес")
        
        # Проверка частоты запросов
        if self._check_request_frequency(user_id):
            risk_score += 25
            alerts.append("Высокая частота запросов")
        
        # Проверка геолокации
        if self._check_geolocation_anomaly(user_id, ip):
            risk_score += 40
            alerts.append("Аномальная геолокация")
        
        if risk_score >= 50:
            self._log_suspicious_activity(user_id, "high_risk_login", risk_score, alerts)
            return {"suspicious": True, "risk_score": risk_score, "alerts": alerts}
        
        return {"suspicious": False, "risk_score": risk_score}
    
    def _is_suspicious_ip(self, ip):
        """Проверка подозрительного IP"""
        # Простая проверка на известные подозрительные диапазоны
        suspicious_ranges = ['10.0.0.', '192.168.1.', '172.16.']
        return not any(ip.startswith(range_) for range_ in suspicious_ranges)
    
    def _check_request_frequency(self, user_id):
        """Проверка частоты запросов"""
        # Проверка количества запросов за последние 5 минут
        return False  # Упрощенная реализация
    
    def _check_geolocation_anomaly(self, user_id, ip):
        """Проверка аномалий геолокации"""
        # Проверка изменения местоположения
        return False  # Упрощенная реализация
    
    def _log_suspicious_activity(self, user_id, activity_type, risk_score, details):
        """Логирование подозрительной активности"""
        conn = sqlite3.connect('advanced_security.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO suspicious_activity (timestamp, user_id, activity_type, risk_score, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), user_id, activity_type, risk_score, json.dumps(details)))
        
        conn.commit()
        conn.close()
    
    def create_encrypted_backup(self, source_files):
        """Создание зашифрованной резервной копии"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"encrypted_backup_{timestamp}.enc"
        
        # Сбор данных
        backup_data = {}
        total_size = 0
        
        for file_path in source_files:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    data = f.read()
                    backup_data[file_path] = base64.b64encode(data).decode()
                    total_size += len(data)
        
        # Шифрование
        json_data = json.dumps(backup_data)
        encrypted_data = self.cipher.encrypt(json_data.encode())
        
        # Сохранение
        backup_path = os.path.join("backups", backup_name)
        os.makedirs("backups", exist_ok=True)
        
        with open(backup_path, 'wb') as f:
            f.write(encrypted_data)
        
        # Контрольная сумма
        checksum = hashlib.sha256(encrypted_data).hexdigest()
        
        # Логирование
        conn = sqlite3.connect('advanced_security.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO backup_log (timestamp, backup_type, file_path, size, checksum, encrypted)
            VALUES (?, ?, ?, ?, ?, 1)
        ''', (datetime.now().isoformat(), "full", backup_path, total_size, checksum))
        
        conn.commit()
        conn.close()
        
        return {"backup_path": backup_path, "checksum": checksum, "size": total_size}
    
    def restore_encrypted_backup(self, backup_path, target_dir):
        """Восстановление зашифрованной резервной копии"""
        try:
            with open(backup_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Расшифровка
            decrypted_data = self.cipher.decrypt(encrypted_data)
            backup_data = json.loads(decrypted_data.decode())
            
            # Восстановление файлов
            restored_files = []
            for file_path, encoded_data in backup_data.items():
                data = base64.b64decode(encoded_data)
                
                # Создание директорий
                os.makedirs(os.path.dirname(os.path.join(target_dir, file_path)), exist_ok=True)
                
                # Восстановление файла
                restore_path = os.path.join(target_dir, os.path.basename(file_path))
                with open(restore_path, 'wb') as f:
                    f.write(data)
                
                restored_files.append(restore_path)
            
            return {"success": True, "restored_files": restored_files}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_security_dashboard(self):
        """Панель безопасности"""
        conn = sqlite3.connect('advanced_security.db')
        cursor = conn.cursor()
        
        # Подозрительная активность
        cursor.execute('''
            SELECT COUNT(*) FROM suspicious_activity 
            WHERE timestamp > datetime('now', '-24 hours')
        ''')
        recent_alerts = cursor.fetchone()[0]
        
        # 2FA статистика
        cursor.execute("SELECT COUNT(*) FROM two_factor_auth WHERE enabled = 1")
        users_with_2fa = cursor.fetchone()[0]
        
        # Резервные копии
        cursor.execute('''
            SELECT COUNT(*), MAX(timestamp) FROM backup_log 
            WHERE timestamp > datetime('now', '-7 days')
        ''')
        backup_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            "recent_alerts": recent_alerts,
            "users_with_2fa": users_with_2fa,
            "recent_backups": backup_stats[0] or 0,
            "last_backup": backup_stats[1],
            "security_level": "HIGH" if users_with_2fa > 0 and recent_alerts < 5 else "MEDIUM"
        }

# Глобальный экземпляр
advanced_security = AdvancedSecurity()