# data_collector_agent.py

from agent_logic import AgentLogic
import datetime
import psutil
import json

class DataCollectorAgent(AgentLogic):
    def __init__(self):
        super().__init__("DataCollector")
        self.data_storage = {}
        self.collection_interval = 60  # в секундах

    def execute(self):
        self.logger.info("Сбор системных данных...")
        system_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "memory_usage": self.get_memory_usage(),
            "cpu_usage": self.get_cpu_usage(),
            "disk_usage": self.get_disk_usage()
        }
        self.data_storagesystem_data"timestamp" = system_data
        self.logger.info("Данные собраны")
        self.save_data()

    def get_memory_usage(self):
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent
        }

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def get_disk_usage(self):
        disk = psutil.disk_usage('/')
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }

    def save_data(self, filename="data_storage.json"):
        with open(filename, "w") as f:
            json.dump(self.data_storage, f)
        self.logger.info("Данные сохранены")