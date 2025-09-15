@echo off
echo Starting Director Web Interface...

REM Install Flask if needed
pip install flask

REM Start director interface
echo Starting Director Interface on port 8088...
start "Director Interface" python director_web_interface.py

echo.
echo ========================================
echo   DIRECTOR WEB INTERFACE STARTED
echo ========================================
echo.
echo Main Dashboard: http://localhost:8088
echo Agent Chat: http://localhost:8088/chat
echo.
echo Press any key to exit...
pause >nul