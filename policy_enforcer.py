# policy_enforcer.py

import json

THRESHOLD = 50  # Порог риска

def enforce_policy(risk_report_path="risk_report.json"):
    try:
        with open(risk_report_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[✘] Ошибка чтения отчёта риска: {e}")
        return

    for entry in data[-5:]:  # Проверяем последние 5 событий
        score = entry.get("risk_score", 0)
        message = entry["event"].get("message", "Без описания")

        if score >= THRESHOLD:
            print(f"[🚨] Обнаружен высокий риск ({score}): {message}")
            # Здесь можно добавить:
            # - отправку уведомления
            # - остановку CI/CD
            # - запись в отдельный журнал
        else:
            print(f"[✔] Риск допустим ({score}): {message}")

if __name__ == "__main__":
    enforce_policy()