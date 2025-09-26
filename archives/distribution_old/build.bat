@echo off
REM Build script for RunwayML Batch Automation Tool
echo.
echo ===============================================================================
echo    BUILDING RUNWAYML BATCH AUTOMATION TOOL
echo ===============================================================================
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found! Installing...
    python -m pip install pyinstaller
    echo.
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec.bak" del /q "*.spec.bak"

REM Build the executable
echo.
echo Building executable...
echo.

REM Use the spec file for building
pyinstaller runway_batch.spec --clean

echo.
if exist "dist\RunwayML_Batch.exe" (
    echo ===============================================================================
    echo    BUILD SUCCESSFUL!
    echo ===============================================================================
    echo.
    echo Executable created at: dist\RunwayML_Batch.exe
    echo.

    REM Get file size
    for %%I in ("dist\RunwayML_Batch.exe") do (
        set /a size=%%~zI/1048576
        echo File size: %%~zI bytes
    )

    echo.
    echo You can now run the application using:
    echo    dist\RunwayML_Batch.exe
    echo.
) else (
    echo ===============================================================================
    echo    BUILD FAILED!
    echo ===============================================================================
    echo.
    echo Please check the error messages above.
    echo.
)

pause