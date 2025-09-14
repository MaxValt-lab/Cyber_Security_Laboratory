# servise/client.py

import os
import requests

def notify_admin(message: str):
    """
    Уведомление администратора.
    По умолчанию — консоль. Если заданы TELEGRAM_TOKEN и TELEGRAM_CHAT_ID — отправка в Telegram.
    """
    token = os.getenv("TELEGRAM_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    if token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            resp = requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=5)
            resp.raise_for_status()
            print("[🔔] Уведомление отправлено в Telegram")
            return
        except Exception as e:
            print(f"[✘] Ошибка отправки в Telegram: {e}")

    print(f"[🔔] Уведомление администратору: {message}")
