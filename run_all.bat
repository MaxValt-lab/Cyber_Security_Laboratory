@echo off
chcp 65001 >nul
title Cyber Security Laboratory - Полная установка и запуск

echo ================================================
echo  Cyber Security Laboratory - Автоматизация
echo ================================================
echo.

REM Проверка Python
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не найден
    echo [INFO] Скачайте Python с https://python.org
    pause
    exit /b 1
)

REM Автоматическая установка
echo [STEP 1] Автоматическая установка...
py install.py
if errorlevel 1 (
    echo [ERROR] Ошибка установки
    pause
    exit /b 1
)

echo.
echo [STEP 2] Запуск системы...
echo [INFO] Система будет доступна по адресу: http://localhost:8000
echo [INFO] Для остановки нажмите Ctrl+C
echo.

REM Запуск в фоне и открытие браузера
start /B start.bat
timeout /t 5 /nobreak >nul
start http://localhost:8000

echo [INFO] Система запущена!
echo [INFO] Веб-интерфейс открыт в браузере
echo.
pause