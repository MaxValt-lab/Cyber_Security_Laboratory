@echo off
chcp 65001 >nul
echo [START] Запуск Cyber Security Laboratory
echo.

REM Проверка виртуального окружения
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Виртуальное окружение не найдено
    echo [INFO] Запустите setup.bat для настройки
    pause
    exit /b 1
)

REM Активация окружения
echo [STEP 1] Активация окружения...
call venv\Scripts\activate.bat

REM Запуск сервера
echo [STEP 2] Запуск сервера...
echo [INFO] Веб-интерфейс: http://localhost:8000
echo [INFO] API документация: http://localhost:8000/docs
echo [INFO] Для остановки нажмите Ctrl+C
echo.
python start.py

pause