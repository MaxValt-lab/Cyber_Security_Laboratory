#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import time

def send_event(event):
    url = "http://localhost:8000/api/event"
    data = json.dumps(event).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Событие отправлено: риск={result['risk_score']}")
    except Exception as e:
        print(f"Ошибка: {e}")

def test_api():
    print("Тестирование Cyber Security Laboratory")
    
    # Проверка статуса
    try:
        with urllib.request.urlopen("http://localhost:8000/api/status") as response:
            status = json.loads(response.read().decode('utf-8'))
            print(f"Статус: {status}")
    except Exception as e:
        print(f"Сервер недоступен: {e}")
        return
    
    # Тестовые события
    events = [
        {"type": "login_attempt", "source": "external", "severity": "medium", "message": "Попытка входа"},
        {"type": "file_access", "source": "internal", "severity": "high", "message": "Доступ к файлу"},
        {"type": "network_scan", "source": "external", "severity": "critical", "message": "Сканирование сети"}
    ]
    
    for event in events:
        send_event(event)
        time.sleep(1)
    
    # Статистика
    try:
        with urllib.request.urlopen("http://localhost:8000/api/stats") as response:
            stats = json.loads(response.read().decode('utf-8'))
            print(f"Статистика: {stats}")
    except Exception as e:
        print(f"Ошибка статистики: {e}")

if __name__ == "__main__":
    test_api()