# audit_writer.py

from datetime import datetime
import hashlib
import json
import sys
import os
from risk_engine import RiskEngine

AUDIT_LOG = "audit.log"
RISK_REPORT = "risk_report.json"

engine = RiskEngine("risk_policy.json")

def log_event(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    event = {
        "type": "system_event",
        "source": "internal",
        "severity": "medium",
        "message": message
    }

    risk = engine.assess_event(event)
    entry = f"{timestamp} | {message} | Risk: {risk['risk_score']} | Hash: {risk['hash']}\n"

    try:
        with open(AUDIT_LOG, "a") as f:
            f.write(entry)
        print(f"[✔] Записано в журнал: {entry.strip()}")
    except Exception as e:
        print(f"[✘] Ошибка записи в журнал: {e}")
        sys.exit(1)

    try:
        if os.path.exists(RISK_REPORT):
            with open(RISK_REPORT, "r") as f:
                report_data = json.load(f)
        else:
            report_data = []

        report_data.append(risk)

        with open(RISK_REPORT, "w") as f:
            json.dump(report_data, f, indent=2)
        print(f"[✔] Оценка риска сохранена в {RISK_REPORT}")
    except Exception as e:
        print(f"[✘] Ошибка записи отчёта риска: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        log_event(" ".join(sys.argv[1:]))
    else:
        log_event("Событие без описания")