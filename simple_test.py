"""
Простой тест сервера без внешних зависимостей
"""
import urllib.request
import urllib.parse
import json
import threading
import subprocess
import time

def test_url(url, method="GET", data=None):
    """Тестирование URL"""
    try:
        if method == "POST" and data:
            data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        else:
            req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.getcode(), response.read().decode('utf-8')[:100]
    except Exception as e:
        return f"ERROR: {e}", ""

def run_tests():
    """Запуск тестов"""
    print("Ожидание запуска сервера...")
    time.sleep(3)
    
    base_url = "http://localhost:8089"
    
    tests = [
        ("Главная страница", f"{base_url}/", "GET"),
        ("Страница входа", f"{base_url}/login", "GET"), 
        ("Панель управления", f"{base_url}/dashboard", "GET"),
        ("Чат с агентами", f"{base_url}/chat", "GET"),
        ("API входа", f"{base_url}/api/login", "POST", {"username": "director", "password": "admin2024"})
    ]
    
    print("\n=== ТЕСТИРОВАНИЕ СЕРВЕРА ===\n")
    
    for name, url, method, *args in tests:
        data = args[0] if args else None
        status, content = test_url(url, method, data)
        print(f"{'✅' if str(status).startswith('2') else '❌'} {name}: {status}")
        if method == "POST" and "success" in content:
            print(f"   Ответ: {content}")
    
    print(f"\n🌐 Сервер запущен: {base_url}")
    print("🔐 Учетные данные: director / admin2024")
    print("\nОткройте браузер и перейдите по ссылке для проверки!")

if __name__ == "__main__":
    print("Запуск сервера директора...")
    
    # Запуск сервера в отдельном потоке
    def start_server():
        subprocess.run(["py", "simple_director_server.py"])
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Запуск тестов
    run_tests()
    
    input("\nНажмите Enter для завершения...")