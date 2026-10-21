@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo  AegisGate — Offline-First AI Security Gateway
echo ========================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] Error: Python 3.12 is required but not found in PATH.
    echo     Please install Python 3.12 from https://www.python.org/
    pause
    exit /b 1
)

if not exist ".venv" (
    echo [*] Creating virtual environment (.venv)...
    python -m venv .venv
)

echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [*] Checking local dependencies...
python -m pip install -q -r requirements.txt

echo.
echo [+] Starting AegisGate strictly on localhost (127.0.0.1:8000)...
echo [+] Local Dashboard: http://127.0.0.1:8000/
echo [*] Press Ctrl+C to stop.
echo.

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
