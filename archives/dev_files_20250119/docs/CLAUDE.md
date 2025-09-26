# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RunwayML Batch Automation Tool - A Python application for automating RunwayML Act Two video generation from character images. Processes image folders recursively and generates videos using the RunwayML API with duplicate detection and smart output management.

## Development Commands

### Starting the Application
```bash
# Windows batch launcher (recommended)
run_runway_ui.bat

# Direct Python execution
python runway_automation_ui.py

# Test mode (no UI)
python runway_generator.py
```

### Dependencies Installation
```bash
pip install rich requests pillow

# Optional for video duration detection
pip install opencv-python moviepy
```

### Testing Single Components
```bash
# Test GUI selectors
python -c "from gui_selectors import GUISelectors; gui = GUISelectors(); gui.select_driver_video_gui()"

# Test path resolution
python -c "from path_utils import path_manager; print(path_manager.downloads_dir)"

# Test API connection (requires valid API key)
python -c "from runway_generator import RunwayActTwoBatchGenerator; gen = RunwayActTwoBatchGenerator('YOUR_KEY', verbose=True); print('Connected')"
```

## Architecture & Key Components

### Core Processing Pipeline
1. **Input Selection**: GUI folder browser scans recursively for images (supports GenX filtering)
2. **Image Preparation**: Resizes to 16:9 aspect ratio, converts to base64 data URI
3. **API Submission**: Creates Act Two generation with driver video + character image
4. **Status Polling**: Monitors generation with exponential backoff (10s → 60s max)
5. **Output Management**: Saves videos either co-located with source or centralized folder

### Module Architecture

**Entry Points:**
- `run_runway_ui.bat` → `runway_automation_ui.py` → `RunwayAutomationUI.run()`

**Core Modules:**
- `runway_automation_ui.py`: Main UI with Rich terminal display, menu system, configuration management
- `runway_generator.py`: RunwayML API client, batch processing, duplicate detection
- `gui_selectors.py`: Tkinter-based file/folder browsers with video duration detection
- `path_utils.py`: Cross-platform path resolution, environment variable expansion
- `first_run_setup.py`: Interactive setup wizard for initial configuration

**Data Flow:**
```
User Input (GUI/Menu) → Config Validation → Image Discovery →
API Generation → Status Polling → Video Download → Output Organization
```

### Configuration Schema (`runway_config.json`)
```json
{
  "driver_video": "path/to/driver.mp4",
  "output_folder": "path/to/output",
  "output_location": "centralized|co-located",
  "api_key": "key_...",
  "verbose_logging": true|false,
  "duplicate_detection": true|false,
  "delay_between_generations": 2.0,
  "first_run": false
}
```

### RunwayML API Integration

**Endpoints:**
- Base URL: `https://api.dev.runwayml.com/v1`
- POST `/act-two/generations` - Create generation
- GET `/act-two/generations/{id}` - Check status

**Required Headers:**
```python
{
    "Authorization": f"Bearer {api_key}",
    "X-Runway-Version": "2024-11-06"
}
```

**Generation Payload:**
```python
{
    "driver_image": "data:video/mp4;base64,{encoded_video}",
    "driven_image": "data:image/jpeg;base64,{encoded_image}",
    "prompt": "",
    "resolution": "720p",
    "duration": 10,
    "generation_type": "act-two"
}
```

### UI Menu Structure

**Main Menu Options:**
1. Browse for driver video (GUI)
2. Browse for output folder (GUI)
3. Browse for INPUT folder (select images to process)
4. Toggle output location (centralized/co-located)
5. Edit driver video path (manual)
6. Edit output folder path (manual)
7. Toggle verbose logging
8. Show all settings in detail
Q. Quit

### Key Implementation Patterns

**Duplicate Detection:**
```python
# Checks Downloads folder for existing videos with same base name
existing_files = [f.stem.lower() for f in downloads_path.glob("*.mp4")]
if image_stem.lower() in existing_files:
    skip_as_duplicate()
```

**Output Location Strategies:**
- **Centralized**: All videos saved to configured output folder
- **Co-located**: Videos saved in same folder as source images

**Video Duration Detection (fallback chain):**
1. ffprobe (fastest, most reliable)
2. OpenCV (cv2.VideoCapture)
3. MoviePy (VideoFileClip)
4. File size display as fallback

**Path Resolution Priority:**
1. Absolute paths used as-is
2. Relative paths resolved from script directory
3. Environment variables expanded (`%VAR%` on Windows)
4. Tilde expansion (`~/` paths)
5. Auto-creation of missing directories

### Error States & Recovery

**Common Issues:**
- `FileNotFoundError`: Usually driver video or output folder missing
- `401 Unauthorized`: Invalid API key
- `429 Too Many Requests`: Rate limit hit (increase delay)
- `Timeout`: Generation took > 10 minutes (retry or check API status)

**Logging Locations:**
- `runway_automation.log`: Main application log
- Console output: Controlled by `verbose_logging` setting
- Rich UI: Silent mode shows only progress bars and status

## Build & Distribution

### Creating Windows Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build with custom icon
pyinstaller --onefile --windowed --icon=assets/icon.ico --name "RunwayML Batch" runway_automation_ui.py

# Output in dist/RunwayML Batch.exe
```

### Project Structure for Distribution
```
RunwayML-Batch/
├── dist/
│   └── RunwayML Batch.exe
├── assets/
│   └── icon.ico (R logo)
├── config/
│   └── runway_config.json
└── logs/
    └── runway_automation.log
```