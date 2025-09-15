"""
Автоматизация развертывания и мониторинга
"""
import os
import shutil
import subprocess
import json
import time
import psutil
from datetime import datetime
import sqlite3

class DeploymentManager:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.backup_dir = os.path.join(self.project_root, "backups")
        self.logs_dir = os.path.join(self.project_root, "logs")
        self.config_file = os.path.join(self.project_root, "deployment_config.json")
        self.setup_directories()
        
    def setup_directories(self):
        """Создание необходимых директорий"""
        for directory in [self.backup_dir, self.logs_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def create_backup(self):
        """Создание резервной копии"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            os.makedirs(backup_path, exist_ok=True)
            
            # Копирование файлов
            important_files = [
                "security.db",
                "director_system.db", 
                "general_system.db",
                "enhanced_security.py",
                "simple_director_server.py"
            ]
            
            for file in important_files:
                if os.path.exists(file):
                    shutil.copy2(file, backup_path)
            
            # Создание архива
            archive_path = f"{backup_path}.zip"
            shutil.make_archive(backup_path, 'zip', backup_path)
            shutil.rmtree(backup_path)
            
            self.log_event("backup_created", f"Backup created: {archive_path}")
            return archive_path
            
        except Exception as e:
            self.log_event("backup_failed", f"Backup failed: {str(e)}")
            return None
    
    def deploy_application(self):
        """Развертывание приложения"""
        try:
            self.log_event("deployment_started", "Starting deployment process")
            
            # Создание бэкапа перед развертыванием
            backup_path = self.create_backup()
            if not backup_path:
                raise Exception("Backup creation failed")
            
            # Проверка зависимостей
            self.check_dependencies()
            
            # Запуск тестов
            if not self.run_tests():
                raise Exception("Tests failed")
            
            # Запуск сервисов
            self.start_services()
            
            self.log_event("deployment_completed", "Deployment completed successfully")
            return True
            
        except Exception as e:
            self.log_event("deployment_failed", f"Deployment failed: {str(e)}")
            return False
    
    def check_dependencies(self):
        """Проверка зависимостей"""
        required_modules = ["sqlite3", "json", "datetime", "hashlib", "secrets"]
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                raise Exception(f"Required module {module} not found")
    
    def run_tests(self):
        """Запуск тестов"""
        try:
            result = subprocess.run(["python", "test_suite.py"], 
                                  capture_output=True, text=True, timeout=60)
            return result.returncode == 0
        except:
            return False
    
    def start_services(self):
        """Запуск сервисов"""
        services = [
            {"name": "director_server", "command": ["python", "simple_director_server.py"], "port": 8089}
        ]
        
        for service in services:
            try:
                # Проверка, не запущен ли уже сервис
                if self.is_port_in_use(service["port"]):
                    self.log_event("service_already_running", f"Service {service['name']} already running")
                    continue
                
                # Запуск сервиса
                subprocess.Popen(service["command"])
                time.sleep(2)
                
                if self.is_port_in_use(service["port"]):
                    self.log_event("service_started", f"Service {service['name']} started successfully")
                else:
                    raise Exception(f"Failed to start {service['name']}")
                    
            except Exception as e:
                self.log_event("service_start_failed", f"Failed to start {service['name']}: {str(e)}")
    
    def is_port_in_use(self, port):
        """Проверка использования порта"""
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == 'LISTEN':
                return True
        return False
    
    def monitor_system(self):
        """Мониторинг системы"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "active_connections": len(psutil.net_connections()),
            "running_processes": len(psutil.pids())
        }
        
        # Сохранение метрик
        metrics_file = os.path.join(self.logs_dir, f"metrics_{datetime.now().strftime('%Y%m%d')}.json")
        
        try:
            with open(metrics_file, 'a') as f:
                f.write(json.dumps(metrics) + '\n')
        except Exception as e:
            self.log_event("metrics_save_failed", f"Failed to save metrics: {str(e)}")
        
        return metrics
    
    def log_event(self, event_type, message):
        """Логирование событий"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "message": message
        }
        
        log_file = os.path.join(self.logs_dir, f"deployment_{datetime.now().strftime('%Y%m%d')}.log")
        
        try:
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Failed to write log: {e}")
    
    def get_system_status(self):
        """Получение статуса системы"""
        return {
            "deployment_status": "active",
            "services": self.check_services_status(),
            "system_metrics": self.monitor_system(),
            "last_backup": self.get_last_backup_info(),
            "uptime": self.get_system_uptime()
        }
    
    def check_services_status(self):
        """Проверка статуса сервисов"""
        services = {
            "director_server": self.is_port_in_use(8089),
            "security_system": os.path.exists("security.db"),
            "backup_system": os.path.exists(self.backup_dir)
        }
        return services
    
    def get_last_backup_info(self):
        """Информация о последнем бэкапе"""
        try:
            backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.zip')]
            if backups:
                latest_backup = max(backups, key=lambda x: os.path.getctime(os.path.join(self.backup_dir, x)))
                backup_path = os.path.join(self.backup_dir, latest_backup)
                return {
                    "filename": latest_backup,
                    "created": datetime.fromtimestamp(os.path.getctime(backup_path)).isoformat(),
                    "size": os.path.getsize(backup_path)
                }
        except:
            pass
        return None
    
    def get_system_uptime(self):
        """Время работы системы"""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            return int(uptime_seconds)
        except:
            return 0
    
    def cleanup_old_backups(self, keep_count=10):
        """Очистка старых бэкапов"""
        try:
            backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.zip')]
            backups.sort(key=lambda x: os.path.getctime(os.path.join(self.backup_dir, x)), reverse=True)
            
            for backup in backups[keep_count:]:
                backup_path = os.path.join(self.backup_dir, backup)
                os.remove(backup_path)
                self.log_event("backup_cleaned", f"Removed old backup: {backup}")
                
        except Exception as e:
            self.log_event("cleanup_failed", f"Cleanup failed: {str(e)}")

# Глобальный экземпляр
deployment_manager = DeploymentManager()

if __name__ == "__main__":
    print("🚀 Система автоматизации развертывания")
    print("=" * 40)
    
    while True:
        print("\n1. Развернуть приложение")
        print("2. Создать бэкап")
        print("3. Мониторинг системы")
        print("4. Статус системы")
        print("5. Очистить старые бэкапы")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ")
        
        if choice == "1":
            print("Запуск развертывания...")
            success = deployment_manager.deploy_application()
            print("✅ Развертывание завершено" if success else "❌ Развертывание провалилось")
            
        elif choice == "2":
            print("Создание бэкапа...")
            backup_path = deployment_manager.create_backup()
            print(f"✅ Бэкап создан: {backup_path}" if backup_path else "❌ Ошибка создания бэкапа")
            
        elif choice == "3":
            metrics = deployment_manager.monitor_system()
            print(f"📊 CPU: {metrics['cpu_percent']}%")
            print(f"💾 Память: {metrics['memory_percent']}%")
            print(f"💿 Диск: {metrics['disk_percent']}%")
            
        elif choice == "4":
            status = deployment_manager.get_system_status()
            print(json.dumps(status, indent=2, ensure_ascii=False))
            
        elif choice == "5":
            deployment_manager.cleanup_old_backups()
            print("✅ Очистка завершена")
            
        elif choice == "0":
            break