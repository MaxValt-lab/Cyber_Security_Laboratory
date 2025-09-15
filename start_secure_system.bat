@echo off
echo Starting Secure Management System...

REM Install dependencies
pip install -r requirements_security.txt

REM Create necessary directories
mkdir backups 2>nul
mkdir logs 2>nul

REM Set environment variables
set MASTER_KEY=SecureKey2024_Laboratory

REM Start secure dashboard
echo Starting Secure Dashboard on port 8085...
start "Secure Dashboard" python secure_dashboard.py

REM Wait a bit
timeout /t 3 /nobreak >nul

REM Start failover manager
echo Starting Failover Manager...
start "Failover Manager" python -c "from failover_manager import failover_manager; import time; time.sleep(3600)"

echo.
echo ========================================
echo   SECURE MANAGEMENT SYSTEM STARTED
echo ========================================
echo.
echo Dashboard: http://localhost:8085
echo Credentials: admin/secure2024
echo.
echo Press any key to exit...
pause >nul