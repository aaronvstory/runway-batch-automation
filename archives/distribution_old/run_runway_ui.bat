@echo off
:: Enable ANSI color support
for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

title RunwayML Automation v3.0 - Enhanced with Rich UI

:: Change to the directory where this batch file is located
cd /d "%~dp0"

if not exist runway_automation_ui.py (
    echo %ESC%[91mError: runway_automation_ui.py not found in current directory%ESC%[0m
    echo Please make sure this batch file is in the same folder as the Python scripts.
    echo.
    pause
    exit /b 1
)

if not exist runway_generator.py (
    echo %ESC%[91mError: runway_generator.py not found in current directory%ESC%[0m
    echo Please make sure this batch file is in the same folder as the Python scripts.
    echo.
    pause
    exit /b 1
)

:: Install rich if not available
python -c "import rich" 2>nul
if errorlevel 1 (
    echo %ESC%[93mInstalling required dependencies...%ESC%[0m
    pip install rich
)

:: Launch the Rich UI
python runway_automation_ui.py

pause