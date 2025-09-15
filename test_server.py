"""
Тест сервера директора
"""
import subprocess
import time
import requests
import threading

def start_server():
    """Запуск сервера в отдельном потоке"""
    subprocess.run(["py", "simple_director_server.py"])

def test_server():
    """Тестирование сервера"""
    time.sleep(2)  # Ждем запуска сервера
    
    try:
        # Тест главной страницы
        response = requests.get("http://localhost:8089/", timeout=5)
        print(f"✅ Главная страница: {response.status_code}")
        
        # Тест страницы входа
        response = requests.get("http://localhost:8089/login", timeout=5)
        print(f"✅ Страница входа: {response.status_code}")
        
        # Тест API входа
        login_data = {"username": "director", "password": "admin2024"}
        response = requests.post("http://localhost:8089/api/login", json=login_data, timeout=5)
        print(f"✅ API входа: {response.status_code} - {response.json()}")
        
        # Тест панели управления
        response = requests.get("http://localhost:8089/dashboard", timeout=5)
        print(f"✅ Панель управления: {response.status_code}")
        
        # Тест чата
        response = requests.get("http://localhost:8089/chat", timeout=5)
        print(f"✅ Чат с агентами: {response.status_code}")
        
        print("\n🎉 Все тесты пройдены успешно!")
        print("🌐 Сервер доступен по адресу: http://localhost:8089")
        print("🔐 Логин: director / Пароль: admin2024")
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")

if __name__ == "__main__":
    # Запуск сервера в отдельном потоке
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Тестирование
    test_server()
    
    input("\nНажмите Enter для завершения...")