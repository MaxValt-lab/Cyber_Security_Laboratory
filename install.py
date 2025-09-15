#!/usr/bin/env python3
"""
Автоматическая установка и настройка Cyber Security Laboratory
"""
import os
import sys
import subprocess
import platform

def run_command(cmd, check=True):
    """Выполнение команды с обработкой ошибок"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_python():
    """Проверка версии Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"[ERROR] Требуется Python 3.8+, найден {version.major}.{version.minor}")
        return False
    print(f"[OK] Python {version.major}.{version.minor}.{version.micro}")
    return True

def setup_venv():
    """Создание виртуального окружения"""
    if os.path.exists("venv"):
        print("[INFO] Виртуальное окружение уже существует")
        return True
    
    print("[STEP] Создание виртуального окружения...")
    success, stdout, stderr = run_command(f"{sys.executable} -m venv venv")
    
    if not success:
        print(f"[ERROR] Не удалось создать venv: {stderr}")
        return False
    
    print("[OK] Виртуальное окружение создано")
    return True

def install_deps():
    """Установка зависимостей"""
    print("[STEP] Установка зависимостей...")
    
    # Определяем путь к pip в venv
    if platform.system() == "Windows":
        pip_path = "venv\\Scripts\\pip.exe"
    else:
        pip_path = "venv/bin/pip"
    
    # Обновляем pip
    success, _, stderr = run_command(f"{pip_path} install --upgrade pip")
    if not success:
        print(f"[WARNING] Не удалось обновить pip: {stderr}")
    
    # Устанавливаем зависимости
    success, stdout, stderr = run_command(f"{pip_path} install -r requirements-minimal.txt")
    
    if not success:
        print(f"[ERROR] Не удалось установить зависимости: {stderr}")
        return False
    
    print("[OK] Зависимости установлены")
    return True

def create_config():
    """Создание конфигурационных файлов"""
    print("[STEP] Создание конфигурации...")
    
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("[OK] Создан файл .env")
        else:
            print("[WARNING] .env.example не найден")
    
    return True

def main():
    """Основная функция установки"""
    print("=" * 50)
    print("Cyber Security Laboratory - Автоматическая установка")
    print("=" * 50)
    
    # Проверки
    if not check_python():
        return False
    
    # Установка
    steps = [
        ("Настройка виртуального окружения", setup_venv),
        ("Установка зависимостей", install_deps),
        ("Создание конфигурации", create_config),
    ]
    
    for step_name, step_func in steps:
        print(f"\n[STEP] {step_name}...")
        if not step_func():
            print(f"[ERROR] Ошибка на этапе: {step_name}")
            return False
    
    print("\n" + "=" * 50)
    print("[SUCCESS] Установка завершена успешно!")
    print("\nДля запуска системы:")
    if platform.system() == "Windows":
        print("  start.bat")
    else:
        print("  python start.py")
    print("\nДля тестирования:")
    if platform.system() == "Windows":
        print("  test.bat")
    else:
        print("  python test_simple.py")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)