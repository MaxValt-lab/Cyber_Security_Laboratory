@echo off
chcp 65001 >nul
echo 🤖 Автоматический анализ кода
echo ================================

py run_code_analysis.py

echo.
echo ✅ Анализ завершен!
echo 📊 Проверьте файлы отчетов:
echo    - code_analysis.json
echo    - security_scan.json
echo.
pause