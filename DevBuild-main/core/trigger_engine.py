from typing import Callable, Dict, List, Optional
import logging
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TriggerEngine")

@dataclass
class TriggerMetadata:
    """Метаданные триггера"""
    name: str
    priority: int = 1
    group: Optional[str] = None
    enabled: bool = True

class Trigger(ABC):
    def __init__(self, metadata: TriggerMetadata):
        self.metadata = metadata
        self.last_execution: Optional[float] = None

    @abstractmethod
    def condition(self) -> bool:
        pass

    @abstractmethod
    def action(self):
        pass

    def evaluate(self):
        try:
            if self.metadata.enabled and self.condition():
                self.last_execution = datetime.now().timestamp()
                logger.info(f"⚡ Trigger '{self.metadata.name}' activated")
                self.action()
            else:
                logger.debug(f"⏸️ Trigger '{self.metadata.name}' not activated")
        except Exception as e:
            logger.error(f"❌ Error in trigger '{self.metadata.name}': {str(e)}")

class SimpleTrigger(Trigger):
    def __init__(self, metadata: TriggerMetadata, condition: Callable[[], bool], action: Callable[[], None]):
        super().__init__(metadata)
        self.condition_func = condition
        self.action_func = action

    def condition(self) -> bool:
        return self.condition_func()

    def action(self):
        self.action_func()

class TriggerEngine:
    def __init__(self):
        self.triggers: Dict[str, Trigger] = {}
        self.groups: Dict[str, List[str]] = {}

    def register(self, metadata: TriggerMetadata, condition: Callable[[], bool], action: Callable[[], None]):
        if metadata.name in self.triggers:
            logger.warning(f"⚠️ Trigger '{metadata.name}' already exists. Overwriting...")

        trigger = SimpleTrigger(metadata, condition, action)
        self.triggers[metadata.name] = trigger

        if metadata.group:
            if metadata.group not in self.groups:
                self.groups[metadata.group] = []
            if metadata.name not in self.groups[metadata.group]:
                self.groups[metadata.group].append(metadata.name)

        logger.info(f"📌 Registered trigger: {metadata.name}")

    def unregister(self, name: str):
        if name in self.triggers:
            del self.triggers[name]
            logger.info(f"🗑️ Unregistered trigger: {name}")
            for group, triggers in self.groups.items():
                if name in triggers:
                    triggers.remove(name)
        else:
            logger.warning(f"⚠️ Trigger '{name}' not found")

    def evaluate_all(self):
        logger.info("🔍 Evaluating all triggers...")
        sorted_triggers = sorted(
            self.triggers.values(),
            key=lambda t: t.metadata.priority,
            reverse=True
        )
        for trigger in sorted_triggers:
            trigger.evaluate()

    def evaluate_group(self, group_name: str):
        if group_name in self.groups:
            logger.info(f"🔍 Evaluating group: {group_name}")
            for trigger_name in self.groups[group_name]:
                if trigger_name in self.triggers:
                    self.triggers[trigger_name].evaluate()
        else:
            logger.warning(f"⚠️ Group '{group_name}' not found")

    def get_trigger_status(self, name: str) -> Optional[Dict]:
        if name in self.triggers:
            trigger = self.triggers[name]
            return {
                "name": trigger.metadata.name,
                "priority": trigger.metadata.priority,
                "group": trigger.metadata.group,
                "enabled": trigger.metadata.enabled,
                "last_execution": trigger.last_execution
            }
        return None

    def disable_trigger(self, name: str):
        if name in self.triggers:
            self.triggers[name].metadata.enabled = False
            logger.info(f"🚫 Trigger '{name}' disabled")
        else:
            logger.warning(f"⚠️ Trigger '{name}' not found")

    def enable_trigger(self, name: str):
        if name in self.triggers:
            self.triggers[name].metadata.enabled = True
            logger.info(f"✅ Trigger '{name}' enabled")
        else:
            logger.warning(f"⚠️ Trigger '{name}' not found")

    def get_all_triggers_status(self) -> Dict:
        status = {}
        for name, trigger in self.triggers.items():
            status[name] = {
                "priority": trigger.metadata.priority,
                "group": trigger.metadata.group,
                "enabled": trigger.metadata.enabled,
                "last_execution": trigger.last_execution
            }
        return status

    def get_groups(self) -> Dict:
        return self.groups

    def add_to_group(self, trigger_name: str, group_name: str):
        if trigger_name in self.triggers:
            if group_name not in self.groups:
                self.groups[group_name] = []
            if trigger_name not in self.groups[group_name]:
                self.groups[group_name].append(trigger_name)
                logger.info(f"👥 Added trigger '{trigger_name}' to group '{group_name}'")
        else:
            logger.warning(f"⚠️ Trigger '{trigger_name}' not found")

    def remove_from_group(self, trigger_name: str, group_name: str):
        if group_name in self.groups:
            if trigger_name in self.groups[group_name]:
                self.groups[group_name].remove(trigger_name)
                logger.info(f"🗑️ Removed trigger '{trigger_name}' from group '{group_name}'")
            else:
                logger.warning(f"⚠️ Trigger '{trigger_name}' not in group '{group_name}'")
        else:
            logger.warning(f"⚠️ Group '{group_name}' not found")

# Пример использования
def example_condition() -> bool:
    return True

def example_action():
    print("Trigger action executed!")

if __name__ == "__main__":
    engine = TriggerEngine()

    metadata = TriggerMetadata(
        name="example_trigger",
        priority=5,
        group="main_group"
    )

    engine.register(metadata, example_condition, example_action)
    engine.evaluate_all()
    print(engine.get_trigger_status("example_trigger"))
    engine.add_to_group("example_trigger", "new_group")
    print(engine.get_groups())