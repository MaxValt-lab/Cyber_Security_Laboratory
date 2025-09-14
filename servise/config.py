import os

RISK_POLICY_PATH = os.getenv("RISK_POLICY_PATH", "risk_policy.json")
AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "audit.log")
RISK_REPORT_PATH = os.getenv("RISK_REPORT_PATH", "risk_report.json")
INCIDENT_LOG_PATH = os.getenv("INCIDENT_LOG_PATH", "incident.log")
THRESHOLD = int(os.getenv("RISK_THRESHOLD", 50))
