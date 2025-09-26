@echo off
REM Build RunwayML Batch executable in root folder

echo Building RunwayML_Batch.exe...
echo.

REM Clean old build artifacts
if exist "build" rmdir /s /q "build"
if exist "RunwayML_Batch.exe" del /q "RunwayML_Batch.exe"

REM Build using the spec file
pyinstaller build_exe.spec --clean --distpath .

echo.
if exist "RunwayML_Batch.exe" (
    echo BUILD SUCCESSFUL!
    echo Executable created: RunwayML_Batch.exe
    for %%I in ("RunwayML_Batch.exe") do echo Size: %%~zI bytes
) else (
    echo BUILD FAILED!
)

pause