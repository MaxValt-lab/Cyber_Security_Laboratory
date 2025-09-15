@echo off
chcp 65001 >nul
echo ========================================
echo   MASTER DEPLOYMENT SYSTEM
echo ========================================
echo.

echo 🔧 Установка зависимостей...
py -m pip install cryptography psutil --quiet

echo 📚 Генерация документации...
py documentation_generator.py

echo 🧪 Запуск тестов...
py test_suite.py

echo 🚀 Развертывание системы...
py deployment_automation.py

echo.
echo ========================================
echo   СИСТЕМА РАЗВЕРНУТА УСПЕШНО
echo ========================================
echo.
echo 🌐 Веб-интерфейс: http://localhost:8089
echo 🔐 Логин: director / Пароль: admin2024
echo 📚 Документация: docs/README.md
echo 📊 Мониторинг: logs/
echo 💾 Бэкапы: backups/
echo.
pause