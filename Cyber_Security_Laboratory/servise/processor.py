# servise/processor.py

from typing import Dict
from .config import RISK_POLICY_PATH, RISK_THRESHOLD
from .client import notify_admin
from tools.risk_engine import RiskEngine
from database import db

# Инициализация движка рисков один раз
engine = RiskEngine(RISK_POLICY_PATH)

def process_event(event: Dict) -> Dict:
    """
    Принимает событие, оценивает риск, пишет аудит, при необходимости — инцидент и уведомление.
    Возвращает статус, риск и выполненное действие.
    """
    # Оценка риска
    risk = engine.assess_event(event)
    risk_score = risk.get("risk_score", 0)
    
    # Добавляем risk_score в event для логирования
    event_with_risk = {**event, "risk_score": risk_score}
    
    # Запись события в БД
    db.log_event(event_with_risk)

    # Реакция на высокий риск
    if risk_score >= RISK_THRESHOLD:
        # Запись инцидента в БД
        db.log_incident(risk)
        # Уведомление
        notify_admin(f"Высокий риск ({risk_score}): {event.get('message')}")
        action = "incident_logged_and_notified"
    else:
        action = "no_action"

    return {
        "status": "processed",
        "risk_score": int(risk_score),
        "action": action,
    }
