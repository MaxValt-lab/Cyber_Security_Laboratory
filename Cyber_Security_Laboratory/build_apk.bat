@echo off
chcp 65001 >nul
title Cyber Security Laboratory - APK Builder

echo ================================================
echo  Cyber Security Laboratory - Сборка APK
echo ================================================
echo.

REM Проверка Python
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не найден
    pause
    exit /b 1
)

REM Установка зависимостей для сборки
echo [STEP 1] Установка зависимостей...
py -m pip install kivy kivymd buildozer python-for-android

REM Запуск сборки
echo [STEP 2] Запуск сборки APK...
py build_apk.py

echo.
echo [INFO] Процесс сборки завершен
pause