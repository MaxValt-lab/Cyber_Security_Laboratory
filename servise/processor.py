from risk_engine import RiskEngine
from audit_writer import log_event
from policy_enforcer import log_incident
from config import RISK_POLICY_PATH, THRESHOLD
from client import notify_admin

engine = RiskEngine(RISK_POLICY_PATH)

def process_event(event: dict):
    risk = engine.assess_event(event)
    log_event(event["message"])
    
    if risk["risk_score"] >= THRESHOLD:
        log_incident(risk)
        notify_admin(event["message"])
        action = "incident_logged"
    else:
        action = "no_action"

    return {"risk_score": risk["risk_score"], "action": action}
