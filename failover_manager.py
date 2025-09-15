"""
Менеджер отказоустойчивости системы
"""
import psutil
import time
import subprocess
import threading
import json
import logging
from datetime import datetime
from security_core import security_core

class FailoverManager:
    def __init__(self):
        self.services = {
            "director_dashboard": {"port": 8080, "process": None, "restarts": 0},
            "general_dashboard": {"port": 8090, "process": None, "restarts": 0},
            "api_gateway": {"port": 9000, "process": None, "restarts": 0}
        }
        self.max_restarts = 3
        self.check_interval = 30
        self.setup_logging()
        self.start_monitoring()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('failover.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_service_health(self, service_name, port):
        """Проверка состояния сервиса"""
        try:
            # Проверка порта
            for conn in psutil.net_connections():
                if conn.laddr.port == port and conn.status == 'LISTEN':
                    return True
            return False
        except:
            return False
    
    def restart_service(self, service_name):
        """Перезапуск сервиса"""
        try:
            service = self.services[service_name]
            
            if service["restarts"] >= self.max_restarts:
                self.logger.error(f"Max restarts reached for {service_name}")
                return False
            
            # Остановка процесса
            if service["process"]:
                service["process"].terminate()
                time.sleep(5)
            
            # Запуск сервиса
            if service_name == "director_dashboard":
                service["process"] = subprocess.Popen(["python", "director_dashboard.py"])
            elif service_name == "general_dashboard":
                service["process"] = subprocess.Popen(["python", "general_dashboard.py"])
            elif service_name == "api_gateway":
                service["process"] = subprocess.Popen(["python", "api_gateway.py"])
            
            service["restarts"] += 1
            self.logger.info(f"Service {service_name} restarted (attempt {service['restarts']})")
            
            # Аудит
            security_core.audit_log("service_restart", "system", {
                "service": service_name,
                "restart_count": service["restarts"]
            })
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restart {service_name}: {e}")
            return False
    
    def monitor_services(self):
        """Мониторинг сервисов"""
        while True:
            for service_name, service in self.services.items():
                if not self.check_service_health(service_name, service["port"]):
                    self.logger.warning(f"Service {service_name} is down")
                    self.restart_service(service_name)
            
            time.sleep(self.check_interval)
    
    def start_monitoring(self):
        """Запуск мониторинга"""
        monitor_thread = threading.Thread(target=self.monitor_services, daemon=True)
        monitor_thread.start()
        self.logger.info("Failover monitoring started")
    
    def get_system_status(self):
        """Получение статуса системы"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "services": {},
            "system": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent
            }
        }
        
        for service_name, service in self.services.items():
            status["services"][service_name] = {
                "healthy": self.check_service_health(service_name, service["port"]),
                "restarts": service["restarts"],
                "port": service["port"]
            }
        
        return status
    
    def emergency_shutdown(self):
        """Аварийное отключение"""
        self.logger.critical("Emergency shutdown initiated")
        
        for service_name, service in self.services.items():
            if service["process"]:
                service["process"].terminate()
        
        security_core.audit_log("emergency_shutdown", "system", {
            "reason": "manual_trigger",
            "timestamp": datetime.now().isoformat()
        })

# Глобальный экземпляр
failover_manager = FailoverManager()