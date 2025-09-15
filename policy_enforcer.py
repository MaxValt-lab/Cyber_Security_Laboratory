# policy_enforcer.py

import json
from datetime import datetime
import hashlib

THRESHOLD = 50  # Порог риска
RISK_REPORT = "risk_report.json"
INCIDENT_LOG = "incident.log"

def enforce_policy():
    try:
        with open(RISK_REPORT, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[✘] Ошибка чтения отчёта риска: {e}")
        return

    for entry in data[-10:]:  # Проверяем последние 10 событий
        score = entry.get("risk_score", 0)
        event = entry.get("event", {})
        message = event.get("message", "Без описания")

        if score >= THRESHOLD:
            print(f"[🚨] Высокий риск ({score}): {message}")
            log_incident(entry)
        else:
            print(f"[✔] Риск допустим ({score}): {message}")

def log_incident(entry):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    hash_value = hashlib.sha256(json.dumps(entry).encode()).hexdigest()

    line = f"{timestamp} | Risk: {entry['risk_score']} | {entry['event']['message']} | Hash: {hash_value}\n"

    try:
        with open(INCIDENT_LOG, "a") as f:
            f.write(line)
        print(f"[🛡] Инцидент записан в {INCIDENT_LOG}")
    except Exception as e:
        print(f"[✘] Ошибка записи инцидента: {e}")

if __name__ == "__main__":
    enforce_policy()
