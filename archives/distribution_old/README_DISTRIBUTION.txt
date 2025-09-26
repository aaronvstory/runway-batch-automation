========================================================================================
                        RunwayML Batch Automation - Distribution Guide
========================================================================================

FOLDER STRUCTURE:
-----------------
/builds        - Compiled executables and builds
/installer     - Installation packages and setup files
run_runway_ui.bat - Original batch launcher (legacy)

BUILD INSTRUCTIONS:
-------------------
To create a Windows executable:

1. Install PyInstaller:
   pip install pyinstaller

2. Build from project root:
   pyinstaller --onefile --windowed --name "RunwayML_Batch" --distpath distribution/builds ../src/runway_automation_ui.py

3. Optional: Add icon
   pyinstaller --onefile --windowed --icon=../assets/icon.ico --name "RunwayML_Batch" --distpath distribution/builds ../src/runway_automation_ui.py

DISTRIBUTION CHECKLIST:
----------------------
[ ] Build executable with PyInstaller
[ ] Test on clean Windows system
[ ] Include config/runway_config.json template
[ ] Include assets/driver_video.mp4 sample
[ ] Create installer with NSIS/Inno Setup (optional)
[ ] Version numbering in filename
[ ] Include requirements.txt for Python users

RELEASE FILES:
-------------
- RunwayML_Batch.exe (standalone executable)
- config/runway_config.json (configuration template)
- assets/driver_video.mp4 (sample driver video)
- requirements.txt (Python dependencies)

========================================================================================