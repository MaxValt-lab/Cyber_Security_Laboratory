"""
Мобильный интерфейс и система уведомлений
"""
import json
import sqlite3
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time

class MobileInterface:
    def __init__(self):
        self.setup_mobile_db()
        self.notification_queue = []
        self.start_notification_service()
    
    def setup_mobile_db(self):
        """База данных для мобильного интерфейса"""
        conn = sqlite3.connect('mobile.db')
        cursor = conn.cursor()
        
        # Таблица устройств
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mobile_devices (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                device_token TEXT,
                device_type TEXT,
                app_version TEXT,
                last_active TEXT,
                push_enabled BOOLEAN DEFAULT 1
            )
        ''')
        
        # Таблица уведомлений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT,
                message TEXT,
                type TEXT,
                priority INTEGER,
                created_at TEXT,
                sent_at TEXT,
                read_at TEXT,
                data TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_mobile_dashboard_data(self, user_id):
        """Данные для мобильной панели"""
        return {
            "user_info": self._get_user_info(user_id),
            "quick_stats": self._get_quick_stats(),
            "recent_notifications": self._get_recent_notifications(user_id),
            "urgent_tasks": self._get_urgent_tasks(user_id),
            "system_status": self._get_system_status()
        }
    
    def _get_user_info(self, user_id):
        """Информация о пользователе"""
        return {
            "id": user_id,
            "name": "Директор",
            "role": "admin",
            "last_login": datetime.now().isoformat(),
            "unread_notifications": self._count_unread_notifications(user_id)
        }
    
    def _get_quick_stats(self):
        """Быстрая статистика"""
        return {
            "active_projects": 12,
            "pending_approvals": 3,
            "today_revenue": 150000,
            "online_staff": 8,
            "system_alerts": 1
        }
    
    def _get_recent_notifications(self, user_id, limit=5):
        """Последние уведомления"""
        conn = sqlite3.connect('mobile.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, message, type, created_at, read_at 
            FROM notifications 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        notifications = []
        for row in cursor.fetchall():
            notifications.append({
                "title": row[0],
                "message": row[1],
                "type": row[2],
                "created_at": row[3],
                "is_read": row[4] is not None
            })
        
        conn.close()
        return notifications
    
    def _get_urgent_tasks(self, user_id):
        """Срочные задачи"""
        return [
            {
                "id": 1,
                "title": "Утверждение бюджета проекта А",
                "priority": "high",
                "deadline": "2024-01-15T18:00:00"
            },
            {
                "id": 2,
                "title": "Подписание договора с подрядчиком",
                "priority": "medium",
                "deadline": "2024-01-16T12:00:00"
            }
        ]
    
    def _get_system_status(self):
        """Статус системы"""
        return {
            "overall_status": "healthy",
            "services_online": 4,
            "services_total": 4,
            "last_backup": "2024-01-15T10:30:00",
            "security_level": "high"
        }
    
    def _count_unread_notifications(self, user_id):
        """Количество непрочитанных уведомлений"""
        conn = sqlite3.connect('mobile.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM notifications 
            WHERE user_id = ? AND read_at IS NULL
        ''', (user_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def send_notification(self, user_id, title, message, notification_type="info", priority=1, data=None):
        """Отправка уведомления"""
        conn = sqlite3.connect('mobile.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notifications (user_id, title, message, type, priority, created_at, data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, title, message, notification_type, priority, datetime.now().isoformat(), 
              json.dumps(data) if data else None))
        
        notification_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Добавление в очередь для отправки
        self.notification_queue.append({
            "id": notification_id,
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "priority": priority
        })
        
        return notification_id
    
    def start_notification_service(self):
        """Запуск сервиса уведомлений"""
        def notification_worker():
            while True:
                if self.notification_queue:
                    notification = self.notification_queue.pop(0)
                    self._process_notification(notification)
                time.sleep(1)
        
        thread = threading.Thread(target=notification_worker, daemon=True)
        thread.start()
    
    def _process_notification(self, notification):
        """Обработка уведомления"""
        try:
            # Push уведомление (имитация)
            self._send_push_notification(notification)
            
            # Email уведомление для высокого приоритета
            if notification["priority"] >= 3:
                self._send_email_notification(notification)
            
            # Обновление статуса
            conn = sqlite3.connect('mobile.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE notifications SET sent_at = ? WHERE id = ?
            ''', (datetime.now().isoformat(), notification["id"]))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")
    
    def _send_push_notification(self, notification):
        """Отправка push уведомления"""
        # Получение токенов устройств
        conn = sqlite3.connect('mobile.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT device_token, device_type FROM mobile_devices 
            WHERE user_id = ? AND push_enabled = 1
        ''', (notification["user_id"],))
        
        devices = cursor.fetchall()
        conn.close()
        
        for device_token, device_type in devices:
            # Имитация отправки push уведомления
            print(f"📱 Push уведомление отправлено на {device_type}: {notification['title']}")
    
    def _send_email_notification(self, notification):
        """Отправка email уведомления"""
        # Имитация отправки email
        print(f"📧 Email уведомление: {notification['title']} - {notification['message']}")
    
    def register_mobile_device(self, user_id, device_token, device_type, app_version):
        """Регистрация мобильного устройства"""
        conn = sqlite3.connect('mobile.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO mobile_devices 
            (user_id, device_token, device_type, app_version, last_active)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, device_token, device_type, app_version, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Устройство зарегистрировано"}
    
    def mark_notification_read(self, notification_id, user_id):
        """Отметка уведомления как прочитанного"""
        conn = sqlite3.connect('mobile.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notifications SET read_at = ? 
            WHERE id = ? AND user_id = ?
        ''', (datetime.now().isoformat(), notification_id, user_id))
        
        conn.commit()
        conn.close()
        
        return {"success": True}
    
    def get_mobile_api_endpoints(self):
        """API эндпоинты для мобильного приложения"""
        return {
            "dashboard": "/api/mobile/dashboard",
            "notifications": "/api/mobile/notifications",
            "mark_read": "/api/mobile/notifications/{id}/read",
            "register_device": "/api/mobile/device/register",
            "quick_actions": "/api/mobile/actions",
            "system_status": "/api/mobile/status"
        }

class NotificationManager:
    def __init__(self):
        self.mobile_interface = MobileInterface()
        self.alert_rules = self._load_alert_rules()
    
    def _load_alert_rules(self):
        """Правила для автоматических уведомлений"""
        return {
            "security_alert": {"priority": 5, "email": True, "push": True},
            "system_error": {"priority": 4, "email": True, "push": True},
            "backup_failed": {"priority": 3, "email": True, "push": False},
            "login_anomaly": {"priority": 3, "email": False, "push": True},
            "task_deadline": {"priority": 2, "email": False, "push": True},
            "system_info": {"priority": 1, "email": False, "push": False}
        }
    
    def trigger_alert(self, alert_type, message, user_id=1, data=None):
        """Запуск автоматического уведомления"""
        if alert_type not in self.alert_rules:
            alert_type = "system_info"
        
        rule = self.alert_rules[alert_type]
        
        # Определение заголовка
        titles = {
            "security_alert": "🚨 Предупреждение безопасности",
            "system_error": "⚠️ Системная ошибка",
            "backup_failed": "💾 Ошибка резервного копирования",
            "login_anomaly": "🔐 Подозрительный вход",
            "task_deadline": "⏰ Приближается дедлайн",
            "system_info": "ℹ️ Системная информация"
        }
        
        title = titles.get(alert_type, "Уведомление")
        
        # Отправка уведомления
        self.mobile_interface.send_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=alert_type,
            priority=rule["priority"],
            data=data
        )
        
        return {"alert_sent": True, "type": alert_type, "priority": rule["priority"]}

# Глобальные экземпляры
mobile_interface = MobileInterface()
notification_manager = NotificationManager()

# Примеры использования
if __name__ == "__main__":
    # Регистрация устройства
    mobile_interface.register_mobile_device(1, "device_token_123", "iOS", "1.0.0")
    
    # Отправка тестовых уведомлений
    notification_manager.trigger_alert("security_alert", "Обнаружена подозрительная активность")
    notification_manager.trigger_alert("task_deadline", "Задача 'Утверждение бюджета' требует внимания")
    
    # Получение данных для мобильной панели
    dashboard_data = mobile_interface.get_mobile_dashboard_data(1)
    print(json.dumps(dashboard_data, indent=2, ensure_ascii=False))