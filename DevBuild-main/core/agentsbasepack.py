from typing import Dict, Type, Any
import logging
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AgentRegistry")

@dataclass
class AgentStatus:
    """Класс для хранения статуса агента"""
    name: str
    status: str
    timestamp: float = datetime.now().timestamp()
    details: Dict[str, Any] = None
    id: str = str(uuid.uuid4())

class AgentBase(ABC):
    """Базовый абстрактный класс агента"""
    
    def __init__(self, name: str):
        self.name = name
        self.status = "inactive"
        self.last_execution: AgentStatus = None
        self.logger = logging.getLogger(f"Agent.{name}")
        self.created_at = datetime.now()

    def activate(self):
        """Активация агента"""
        self.status = "active"
        self.logger.info(f"✅ Agent {self.name} activated")

    def deactivate(self):
        """Деактивация агента"""
        self.status = "inactive"
        self.logger.info(f"🛑 Agent {self.name} deactivated")

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """Основной метод выполнения агента"""
        self.last_execution = AgentStatus(
            name=self.name,
            status=self.status,
            details=self.get_details()
        )
        self.logger.info(f"⚙️ Agent {self.name} executed")
        return {
            "status": self.status,
            "name": self.name,
            "execution_time": self.last_execution.timestamp,
            "execution_id": self.last_execution.id
        }

    def get_details(self) -> Dict[str, Any]:
        """Получение дополнительной информации"""
        return {
            "created_at": self.created_at.isoformat(),
            "status_history": [self.last_execution]
        }

class AgentRegistry:
    """Реестр агентов"""
    _agents: Dict[str, AgentBase] = {}
    _lock: bool = False

    @classmethod
    def register(cls, name: str, agent: AgentBase):
        """Регистрация нового агента"""
        if name in cls._agents:
            logger.warning(f"⚠️ Agent {name} already exists. Overwriting...")
        cls._agents[name] = agent
        logger.info(f"📦 Registered agent: {name}")

    @classmethod
    def unregister(cls, name: str):
        """Удаление агента"""
        if name in cls._agents:
            del cls._agents[name]
            logger.info(f"🗑️ Unregistered agent: {name}")
        else:
            logger.warning(f"⚠️ Agent {name} not found")

    @classmethod
    def load(cls) -> Dict[str, AgentBase]:
        """Загрузка агентов"""
        if cls._lock:
            logger.warning("🔐 Registry is locked. Cannot load agents.")
            return cls._agents
        
        cls._lock = True
        try:
            # Примерная загрузка агентов
            cls.register("FinanceMonitor", FinanceMonitorAgent("FinanceMonitor"))
            cls.register("Security", SecurityAgent("Security"))
            cls.register("Communicator", CommunicatorAgent("Communicator"))
            logger.info("📥 Agents loaded successfully")
        finally:
            cls._lock = False
        return cls._agents

    @classmethod
    def get_agent(cls, name: str) -> AgentBase:
        """Получение агента по имени"""
        return cls._agents.get(name, None)

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """Получение статуса всех агентов"""
        return {
            name: {
                "status": agent.status
"last_execution": agent.last_execution.timestamp if agent.last_execution else None,
                "execution_id": agent.last_execution.id if agent.last_execution else None
            }
            for name, agent in cls._agents.items()
        }

# Заглушки агентов — временные, заменишь на реальные
class FinanceMonitorAgent(AgentBase):
    def execute(self) -> Dict[str, Any]:
        return super().execute()

class SecurityAgent(AgentBase):
    def execute(self) -> Dict[str, Any]:
        return super().execute()

class CommunicatorAgent(AgentBase):
    def execute(self) -> Dict[str, Any]:
        return super().execute()