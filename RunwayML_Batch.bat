@echo off
REM RunwayML Batch Automation Tool
REM Simple launcher that checks for exe first, then runs from Python

cd /d "%~dp0"

REM Check if the compiled exe exists in root folder
if exist "RunwayML_Batch.exe" (
    echo Starting RunwayML Batch...
    start "" "RunwayML_Batch.exe"
    exit /b
)

REM Otherwise run from Python source
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not installed or not in PATH
    echo Please install Python 3.8+ or use RunwayML_Batch.exe
    pause
    exit /b 1
)

echo Starting RunwayML Batch from source...
python src\runway_automation_ui.py
pause