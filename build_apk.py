#!/usr/bin/env python3
"""
Автоматическая сборка APK для Cyber Security Laboratory
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Выполнение команды"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_requirements():
    """Проверка требований для сборки"""
    print("[CHECK] Проверка требований...")
    
    # Проверка Python
    if sys.version_info < (3, 8):
        print("[ERROR] Требуется Python 3.8+")
        return False
    
    # Проверка Buildozer
    success, output = run_command("buildozer --version")
    if not success:
        print("[INFO] Buildozer не найден, устанавливаю...")
        success, output = run_command("pip install buildozer")
        if not success:
            print(f"[ERROR] Не удалось установить Buildozer: {output}")
            return False
    
    print("[OK] Требования выполнены")
    return True

def prepare_build_env():
    """Подготовка окружения сборки"""
    print("[STEP] Подготовка окружения...")
    
    # Создание директории сборки
    build_dir = Path("mobile_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    
    # Копирование файлов
    files_to_copy = [
        ("mobile/main.py", "main.py"),
        ("mobile/buildozer.spec", "buildozer.spec"),
        ("database.py", "database.py"),
        ("servise/models.py", "models.py"),
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, build_dir / dst)
            print(f"[COPY] {src} -> {dst}")
    
    return build_dir

def create_simple_apk():
    """Создание упрощенного APK через Python-for-Android"""
    print("[STEP] Создание APK через p4a...")
    
    # Установка python-for-android
    success, output = run_command("pip install python-for-android")
    if not success:
        print(f"[ERROR] Не удалось установить p4a: {output}")
        return False
    
    # Создание простого APK
    build_cmd = """
p4a apk --private mobile --package=org.cyberseclab.app --name="CyberSecLab" 
--version=1.0 --bootstrap=sdl2 --requirements=python3,kivy,requests 
--permission INTERNET --arch armeabi-v7a
"""
    
    success, output = run_command(build_cmd.replace('\n', ' '))
    if success:
        print("[OK] APK создан успешно")
        return True
    else:
        print(f"[ERROR] Ошибка сборки APK: {output}")
        return False

def build_with_buildozer():
    """Сборка APK через Buildozer"""
    print("[STEP] Сборка через Buildozer...")
    
    build_dir = prepare_build_env()
    
    # Инициализация Buildozer
    success, output = run_command("buildozer init", cwd=build_dir)
    if not success:
        print(f"[ERROR] Ошибка инициализации: {output}")
        return False
    
    # Сборка APK
    success, output = run_command("buildozer android debug", cwd=build_dir)
    if success:
        print("[OK] APK собран успешно")
        
        # Поиск APK файла
        apk_files = list(build_dir.glob("bin/*.apk"))
        if apk_files:
            apk_file = apk_files[0]
            final_apk = Path("CyberSecurityLab.apk")
            shutil.copy2(apk_file, final_apk)
            print(f"[OK] APK скопирован: {final_apk}")
            return True
    
    print(f"[ERROR] Ошибка сборки: {output}")
    return False

def create_web_apk():
    """Создание WebView APK"""
    print("[STEP] Создание WebView APK...")
    
    # Создание простого WebView приложения
    webview_main = '''
from kivy.app import App
from kivy.uix.widget import Widget
from android.runnable import run_on_ui_thread
from jnius import autoclass, cast

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity

class WebViewApp(App):
    def build(self):
        self.webview = WebView(activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.setWebViewClient(WebViewClient())
        
        @run_on_ui_thread
        def create_webview():
            self.webview.loadUrl('http://192.168.1.100:8000')
        
        create_webview()
        return self.webview

WebViewApp().run()
'''
    
    # Сохранение WebView приложения
    with open("mobile/webview_main.py", "w", encoding="utf-8") as f:
        f.write(webview_main)
    
    print("[OK] WebView приложение создано")
    return True

def main():
    """Основная функция сборки"""
    print("=" * 50)
    print("Cyber Security Laboratory - Сборка APK")
    print("=" * 50)
    
    if not check_requirements():
        return False
    
    # Выбор метода сборки
    print("\nВыберите метод сборки:")
    print("1. Buildozer (рекомендуется)")
    print("2. Python-for-Android")
    print("3. WebView APK")
    
    try:
        choice = input("Введите номер (1-3): ").strip()
    except KeyboardInterrupt:
        print("\n[INFO] Отменено пользователем")
        return False
    
    if choice == "1":
        success = build_with_buildozer()
    elif choice == "2":
        success = create_simple_apk()
    elif choice == "3":
        success = create_web_apk()
    else:
        print("[ERROR] Неверный выбор")
        return False
    
    if success:
        print("\n" + "=" * 50)
        print("[SUCCESS] APK создан успешно!")
        print("Файл: CyberSecurityLab.apk")
        print("=" * 50)
    else:
        print("\n[ERROR] Ошибка создания APK")
    
    return success

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)