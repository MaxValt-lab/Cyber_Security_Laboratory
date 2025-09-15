@echo off
chcp 65001 >nul
echo [TEST] Тестирование API
echo.

REM Активация окружения
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Ожидание запуска сервера
echo [INFO] Ожидание запуска сервера...
timeout /t 3 /nobreak >nul

REM Запуск тестов
echo [STEP 1] Запуск тестового клиента...
python test_simple.py

echo.
echo [INFO] Тестирование завершено
pause