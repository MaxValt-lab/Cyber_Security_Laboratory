#!/usr/bin/env python3
"""
Тестовый клиент для проверки API
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("🧪 Тестирование API Cyber Security Laboratory")
    
    # Проверка статуса
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"✅ Статус: {response.json()}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return
    
    # Тестовые события
    test_events = [
        {
            "type": "login_attempt",
            "source": "external",
            "severity": "medium",
            "message": "Неудачная попытка входа с IP 192.168.1.100"
        },
        {
            "type": "file_access",
            "source": "internal",
            "severity": "high",
            "message": "Доступ к конфиденциальному файлу"
        },
        {
            "type": "network_scan",
            "source": "external",
            "severity": "critical",
            "message": "Обнаружено сканирование портов"
        }
    ]
    
    # Отправка событий
    for i, event in enumerate(test_events, 1):
        try:
            response = requests.post(f"{BASE_URL}/event", json=event)
            result = response.json()
            print(f"📝 Событие {i}: риск={result['risk_score']}, действие={result['action']}")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Ошибка отправки события {i}: {e}")
    
    # Получение статистики
    try:
        response = requests.get(f"{BASE_URL}/stats")
        stats = response.json()
        print(f"📊 Статистика: {stats}")
    except Exception as e:
        print(f"❌ Ошибка получения статистики: {e}")

if __name__ == "__main__":
    test_api()