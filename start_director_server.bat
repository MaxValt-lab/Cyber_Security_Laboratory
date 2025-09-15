@echo off
chcp 65001 >nul
echo Starting Director Web Server...
echo.

cd /d "%~dp0"
py simple_director_server.py

pause