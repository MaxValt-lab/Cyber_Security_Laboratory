@echo off
chcp 65001 >nul
echo [SETUP] Настройка Cyber Security Laboratory
echo.

REM Проверка Python
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не найден. Установите Python с python.org
    pause
    exit /b 1
)

REM Создание виртуального окружения
echo [STEP 1] Создание виртуального окружения...
py -m venv venv
if errorlevel 1 (
    echo [ERROR] Не удалось создать venv
    pause
    exit /b 1
)

REM Активация venv и установка pip
echo [STEP 2] Активация окружения...
call venv\Scripts\activate.bat

REM Обновление pip
echo [STEP 3] Обновление pip...
python -m pip install --upgrade pip

REM Установка базовых зависимостей
echo [STEP 4] Установка зависимостей...
pip install -r requirements-minimal.txt

REM Создание конфигурации
echo [STEP 5] Создание конфигурации...
copy .env.example .env 2>nul

echo.
echo [SUCCESS] Настройка завершена!
echo [INFO] Для запуска используйте: start.bat
pause