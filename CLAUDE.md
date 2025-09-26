# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RunwayML Batch Automation Tool - A Python application for automating RunwayML Act Two video generation from character images. Processes image folders recursively and generates videos using the RunwayML API with duplicate detection and smart output management.

## Development Commands

### Running the Application
```bash
# Windows executable (production)
RunwayML_Batch.exe

# Windows batch launcher (auto-detects exe or Python)
RunwayML_Batch.bat

# Python development
python src\runway_automation_ui.py
```

### Building the Executable
```bash
# Install PyInstaller if not present
pip install pyinstaller

# Build executable (outputs to root folder)
pyinstaller build_exe.spec --clean --distpath .

# The spec file should be created/maintained in root with:
# - name='RunwayML_Batch'
# - icon=str(project_root / 'assets' / 'runway_icon.ico')
# - Outputs to root folder, not distribution/dist
```

### Dependencies Installation
```bash
# Install from requirements file (archived)
pip install -r archives/development_files/requirements.txt

# Or install manually
pip install rich>=13.0.0 requests>=2.28.0 pillow>=9.0.0

# Optional for video duration detection
pip install opencv-python moviepy

# Development dependencies for building
pip install pyinstaller>=6.0.0
```

## Architecture & Key Components

### Core Processing Pipeline
The application follows a clear data flow:
1. **Video Selection**: Driver video from `assets/` folder or user browse
2. **Image Discovery**: Recursive scan for GenX images in selected folders
3. **Duplicate Detection**: Checks existing videos before API calls
4. **API Generation**: Submits to RunwayML Act Two endpoint
5. **Status Polling**: Monitors with exponential backoff (10s → 60s)
6. **Output Management**: Saves to centralized or co-located folders

### Module Responsibilities & Inter-Module Communication

**runway_automation_ui.py** - Main UI orchestrator
- Menu system with sectioned interface (Configuration, Processing, Advanced, System)
- Config management via `config/runway_config.json`
- Rich terminal UI with progress bars
- Creates `RunwayActTwoBatchGenerator` instances for processing
- Calls `gui_selectors` for file/folder selection
- Uses `path_manager` global instance from `path_utils`

**runway_generator.py** - RunwayML API client (`RunwayActTwoBatchGenerator` class)
- Handles Act Two generation requests
- Base64 encoding for images/videos
- Duplicate detection via `check_for_duplicate()` method
- API polling with timeout handling (max 600 seconds)
- Output strategies: centralized vs co-located via `output_location` param
- Returns generation ID and output path on success

**path_utils.py** - Cross-platform path resolution (`PathManager` class, global `path_manager` instance)
- `get_all_driver_videos()` - Scans assets/ folder for videos
- `get_default_driver_video()` - Finds suitable driver video (assets/ only, no Downloads)
- `resolve_path()` - Handles relative paths, env variables, tilde expansion
- Detects executable vs script context via `sys.frozen`
- Used by all modules for path resolution

**gui_selectors.py** - Tkinter file/folder browsers
- `select_driver_video()` - Video selection with duration display
- `select_image_folders()` - Multiple folder selection
- `select_output_folder()` - Single folder selection
- Video duration detection chain: ffprobe → OpenCV → MoviePy
- GenX image filtering in `find_genx_images()`

**first_run_setup.py** - Initial configuration wizard (`FirstRunSetup` class)
- Three-step wizard: API key → Driver video → Output folder
- Supports co-located mode selection (option 5 in output folder)
- Returns config dict that's saved to `config/runway_config.json`
- Uses same `path_manager` instance for path operations

### Configuration Schema
```json
{
  "driver_video": "path/to/video.mp4",
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

**Endpoints**:
- Base URL: `https://api.dev.runwayml.com/v1`
- POST `/act-two/generations` - Create generation
- GET `/act-two/generations/{id}` - Check status

**Headers Required**:
```python
{
    "Authorization": f"Bearer {api_key}",
    "X-Runway-Version": "2024-11-06"
}
```

**Generation Payload Structure**:
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

## Key Implementation Details

### Executable vs Script Path Detection
The application detects its execution context and adjusts paths accordingly:
```python
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_dir = Path(sys.executable).parent
else:
    # Running as Python script
    base_dir = Path(__file__).parent.parent
```

### Driver Video Selection Priority
1. **assets/ folder** - ONLY source via `path_manager.get_all_driver_videos()`
2. **GUI browser** - Manual selection fallback
3. **No Downloads scanning** - Removed to prevent confusion

### GenX Image Filtering
- Looks for "genx" in filename (case-insensitive)
- Supports: .jpg, .jpeg, .png, .bmp, .gif, .webp, .tiff, .tif
- Recursive folder scanning
- Duplicate detection by checking Downloads/*.mp4

### Output Location Strategies
- **Centralized**: All videos saved to configured output folder
- **Co-located**: Videos saved in same folder as source images
- Toggle via menu option 3 in Configuration section

### Video Duration Detection Chain
1. ffprobe (fastest, most reliable)
2. OpenCV cv2.VideoCapture (fallback)
3. MoviePy VideoFileClip (last resort)
4. File size display if all fail

### Menu Structure Updates
The UI was reorganized into sections (lines 202-227 of runway_automation_ui.py):
- CONFIGURATION (options 1-3)
- PROCESSING (options 4-5)
- ADVANCED OPTIONS (options 6-9)
- SYSTEM (H for help, Q for quit)

## Project Structure

```
RunwayML_Batch/
├── RunwayML_Batch.exe    # Compiled executable (60MB)
├── RunwayML_Batch.bat    # Smart launcher
├── src/                  # Python source modules
├── assets/               # Driver videos and icon
├── config/               # runway_config.json storage
└── archives/             # Development artifacts (can be deleted)
```

## Testing & Debugging

### First-Run Experience
Delete `config/runway_config.json` to trigger setup wizard again

### Verbose Logging
Toggle via menu option 8 or set `"verbose_logging": true` in config

### Common Issues
- **OpenCV numpy warning on exe**: Can be ignored, doesn't affect functionality
- **Path resolution**: All paths converted to absolute via path_utils
- **API timeouts**: 10-minute max wait with exponential backoff
- **"Act-Two LR_gen-3.mp4" appears**: Check if file exists in Downloads, app no longer scans there

### Testing Individual Components

```python
# Test path resolution
from path_utils import path_manager
videos = path_manager.get_all_driver_videos()
print(f"Found {len(videos)} videos in assets/")

# Test single generation
from runway_generator import RunwayActTwoBatchGenerator
gen = RunwayActTwoBatchGenerator('YOUR_KEY', verbose=True)
result = gen.generate_act_two(driver_video, character_image, output_folder)

# Test duplicate detection
duplicate = gen.check_for_duplicate(character_image_path, output_folder)
print(f"Duplicate found: {duplicate}")

# Test GUI components (requires display)
from gui_selectors import select_driver_video
video_path = select_driver_video()
```

### Rebuilding After Code Changes
```bash
# Clean previous build
rm -rf build/ dist/ *.spec

# Rebuild with spec file
pyinstaller archives/development_files/build_exe.spec --clean --distpath .

# Or create new spec and build
pyinstaller src/runway_automation_ui.py --onefile --icon=assets/runway_icon.ico --name=RunwayML_Batch
```