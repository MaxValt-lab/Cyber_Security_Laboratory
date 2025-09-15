from typing import Dict, Type, Any, Optional
import logging
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime
import uuid
import random

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
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    details: Optional[Dict[str, Any]] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

class AgentBase(ABC):
    """Базовый абстрактный класс агента"""
    
    def __init__(self, name: str):
        self.name = name
        self.status = "inactive"
        self.last_execution: Optional[AgentStatus] = None
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
        pass

def get_details(self) -> Dict[str, Any]:
        """Получение дополнительной информации"""
        return {
            "created_at": self.created_at.isoformat(),
            "status_history": [self.last_execution] if self.last_execution else []
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
    def get_agent(cls, name: str) -> Optional[AgentBase]:
        """Получение агента по имени"""
        return cls._agents.get(name)

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """Получение статуса всех агентов"""
return {
            name: {
                "status": agent.status,
                "last_execution": agent.last_execution.timestamp if agent.last_execution else None,
                "execution_id": agent.last_execution.id if agent.last_execution else None
            }
            for name, agent in cls._agents.items()
        }

class FinanceMonitorAgent(AgentBase):
    def __init__(self, name: str):
        super().__init__(name)
        self.balance = 0.0
        self.transactions = []

def execute(self) -> Dict[str, Any]:
        # Примерная логика мониторинга финансов
        self.balance += 100.0  # Имитация поступления средств
        self.transactions.append({
            "amount": 100.0,
            "timestamp": datetime.now().isoformat()
        })
        
        result = {
            "balance": self.balance,
            "last_transaction": self.transactions[-1] if self.transactions else None,
            "status": "monitoring"
        }
        
        self.last_execution = AgentStatus(
            name=self.name,
            status=self.status,
            details=result
        )
        self.logger.info(f"⚙️ Agent {self.name} executed")
        return result

class SecurityAgent(AgentBase):
    def __init__(self, name: str):
        super().__init__(name)
        self.threats = []
        self.security_level = "low"

def execute(self) -> Dict[str, Any]:
        # Примерная логика безопасности
        if len(self.threats) > 5:
            self.security_level = "high"
        else:
            self.security_level = "medium"
            
        # Имитация обнаружения угрозы
        if random.random() < 0.1:  # 10% вероятность
            self.threats.append({
                "type": "unknown",
                "timestamp": datetime.now().isoformat()
            })
            
        result = {
            "security_level": self.security_level,
            "threats_count": len(self.threats),
            "last_threat": self.threats[-1] if self.threats else None
        }
        
        self.last_execution = AgentStatus(
            name=self.name,
            status=self.status,
            details=result
        )
        self.logger.info(f"⚙️ Agent {self.name} executed")
        return result

class CommunicatorAgent(AgentBase):
    def __init__(self, name: str):
        super().__init__(name)
        self.messages = []
        self.contacts = {}

def execute(self) -> Dict[str, Any]:
        # Примерная логика коммуникации
        message = {
            "sender": "System",
            "receiver": "User",
            "content": "System status is normal",
            "timestamp": datetime.now().isoformat()
        }
        
        self.messages.append(message)
        
        result = {
            "last_message": message,
            "message_count": len(self.messages),
            "contacts": list(self.contacts.keys())
        }
        
        self.last_execution = AgentStatus(
            name=self.name,
            status=self.status,
            details=result
        )
        self.logger.info(f"⚙️ Agent {self.name} executed")
        return result

# Пример использования
if __name__ == "__main__":
    # Загружаем реестр агентов
    AgentRegistry.load()
    
    # Получаем список агентов
    agents = AgentRegistry.get_status()
    print("Агенты в системе:", agents)
    
    # Активируем агента
    finance_agent = AgentRegistry.get_agent("FinanceMonitor")
    if finance_agent:
        finance_agent.activate()
        result = finance_agent.execute()
        print("Результат выполнения финансового агента:", result)
