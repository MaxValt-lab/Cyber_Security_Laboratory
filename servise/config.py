# servise/config.py

import os

# Пути (учитывая текущую структуру репозитория)
RISK_POLICY_PATH = os.getenv("RISK_POLICY_PATH", "tools/risk_policy.json")
AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "audit.log")
RISK_REPORT_PATH = os.getenv("RISK_REPORT_PATH", "risk_report.json")
INCIDENT_LOG_PATH = os.getenv("INCIDENT_LOG_PATH", "incident.log")

# Порог реагирования
RISK_THRESHOLD = int(os.getenv("RISK_THRESHOLD", "50"))

# Уведомления (заглушки/расширяемо)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
