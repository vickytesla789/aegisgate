# =========================================================================
# AegisGate — Windows PowerShell Offline Launch Script
# =========================================================================

$ErrorActionPreference = "Stop"

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " AegisGate — Offline-First AI Security Gateway" -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

# 1. Verify Python is installed
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "[+] Detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[!] Error: Python 3.12 is required but not found in PATH." -ForegroundColor Red
    Write-Host "    Please install Python 3.12 from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# 2. Check and activate virtual environment
$venvPath = Join-Path $PSScriptRoot ".venv"
$venvActivate = Join-Path $venvPath "Scripts\Activate.ps1"

if (-not (Test-Path $venvPath)) {
    Write-Host "[*] Creating Python virtual environment (.venv)..." -ForegroundColor Yellow
    & python -m venv $venvPath
}

if (Test-Path $venvActivate) {
    Write-Host "[*] Activating virtual environment..." -ForegroundColor Yellow
    & $venvActivate
} else {
    Write-Host "[!] Warning: Virtual environment activation script not found. Using system python." -ForegroundColor Yellow
}

# 3. Ensure dependencies are satisfied
Write-Host "[*] Checking local dependencies..." -ForegroundColor Yellow
& python -m pip install -q -r (Join-Path $PSScriptRoot "requirements.txt")

# 4. Start AegisGate
Write-Host "`n[+] Starting AegisGate strictly on localhost (127.0.0.1:8000)..." -ForegroundColor Green
Write-Host "[+] Local Dashboard: http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "[*] Press Ctrl+C to safely shut down AegisGate.`n" -ForegroundColor Gray

& python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
