# servise/processor.py

from typing import Dict
from .config import (
    RISK_POLICY_PATH,
    RISK_REPORT_PATH,
    INCIDENT_LOG_PATH,
    AUDIT_LOG_PATH,
    RISK_THRESHOLD,
)
from .client import notify_admin

# Импорт из корня проекта
from risk_engine import RiskEngine
from audit_writer import log_event
from policy_enforcer import log_incident

# Инициализация движка рисков один раз
engine = RiskEngine(RISK_POLICY_PATH)

def process_event(event: Dict) -> Dict:
    """
    Принимает событие, оценивает риск, пишет аудит, при необходимости — инцидент и уведомление.
    Возвращает статус, риск и выполненное действие.
    """
    # Оценка риска
    risk = engine.assess_event(event)

    # Запись в audit.log и обновление risk_report.json через существующий механизм
    # Используем уже имеющийся канал: log_event пишет в audit.log и risk_report.json
    log_event(event.get("message", "Событие без описания"))

    # Реакция на высокий риск
    if risk.get("risk_score", 0) >= RISK_THRESHOLD:
        # Запись в incident.log через policy_enforcer.log_incident
        log_incident(risk)
        # Уведомление
        notify_admin(f"Высокий риск ({risk['risk_score']}): {event.get('message')}")
        action = "incident_logged_and_notified"
    else:
        action = "no_action"

    return {
        "status": "processed",
        "risk_score": int(risk.get("risk_score", 0)),
        "action": action,
    }
