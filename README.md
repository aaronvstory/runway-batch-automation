# RunwayML Batch Automation Tool

Automate RunwayML Act Two video generation from character images with smart batch processing and duplicate detection.

## Quick Start

**Windows Users:** Double-click `RunwayML_Batch.exe` to run the application.

**Alternative:** Double-click `RunwayML_Batch.bat` for smart launcher (auto-detects exe or Python).

**Python Development:**
```bash
python src\runway_automation_ui.py
```

## Features

### Core Capabilities
- **Batch Processing**: Process multiple GenX character images automatically
- **Duplicate Detection**: Smart checking prevents wasting API calls on existing videos
- **Driver Video Management**: Scans assets/ folder for available driver videos
- **Output Strategies**:
  - **Centralized**: All videos saved to one configured folder
  - **Co-located**: Videos saved in same folder as source images
- **Rich Terminal UI**: Beautiful progress bars, status displays, and organized menu
- **First-Run Wizard**: Guided setup for API key and preferences

### Advanced Features
- Recursive folder scanning for GenX images
- Exponential backoff polling (10s → 60s)
- Video duration detection (ffprobe → OpenCV → MoviePy fallback)
- Comprehensive error handling and recovery
- Verbose logging mode for debugging
- Persistent configuration management

## System Requirements

- **OS**: Windows 10/11 (64-bit)
- **Storage**: 100MB free disk space
- **API**: Valid RunwayML API key
- **Network**: Active internet connection
- **Runtime**: No Python required for exe version

## Configuration

First-time setup wizard guides you through:
1. **API Key**: Enter your RunwayML API key
2. **Driver Video**: Select from assets/ folder or browse
3. **Output Folder**: Choose where to save generated videos

Settings persist in `config/runway_config.json`

## Menu Structure

### CONFIGURATION
1. Browse for driver video
2. Browse for output folder
3. Toggle output location (centralized/co-located)

### PROCESSING
4. Browse for input images (GenX character images)
5. Start batch processing

### ADVANCED OPTIONS
6. Configure API key
7. Manual path editing
8. Toggle verbose logging
9. Display current settings

### SYSTEM
- [H] Help documentation
- [Q] Quit application

## Project Structure

```
RunwayML_Batch/
├── RunwayML_Batch.exe    # Main executable (60MB)
├── RunwayML_Batch.bat    # Smart launcher script
├── README.md             # This documentation
├── CLAUDE.md             # Claude AI instructions
├── src/                  # Python source modules
│   ├── runway_automation_ui.py      # Main UI orchestrator
│   ├── runway_generator.py          # RunwayML API client
│   ├── path_utils.py               # Path resolution utilities
│   ├── gui_selectors.py            # File/folder browsers
│   └── first_run_setup.py          # Initial setup wizard
├── assets/               # Driver videos and icon
│   └── runway_icon.ico  # Application icon
├── config/               # Configuration storage
│   └── runway_config.json
├── build/                # Build artifacts (PyInstaller)
└── archives/             # Development archives
```

## API Integration

Uses RunwayML Act Two API:
- Base URL: `https://api.dev.runwayml.com/v1`
- Endpoints: `/act-two/generations`
- Authentication: Bearer token
- Resolution: 720p
- Duration: 10 seconds per video

## Troubleshooting

### Common Issues

**API Key Invalid**: Re-enter via Advanced Options → Configure API key

**No Driver Videos Found**: Place MP4 videos in `assets/` folder

**Generation Timeout**: API has 10-minute timeout, check RunwayML dashboard

**Duplicate Not Detected**: Checks Downloads folder for existing videos

### Debug Mode

Enable verbose logging (option 8) to see detailed API responses and processing steps.

## Version History

### v1.0.1 (Current)
- Reorganized menu into logical sections
- Improved driver video discovery (prioritizes assets/ folder)
- Enhanced duplicate detection
- Better error messages and recovery
- Cleaned project structure

### v1.0.0
- Initial production release
- Core batch processing functionality
- Basic UI implementation

## Development

### Building from Source

```bash
# Install dependencies
pip install rich requests pillow

# Optional for video duration
pip install opencv-python moviepy

# Build executable
pyinstaller build_exe.spec --clean --distpath .
```

### Testing

```bash
# Run from source
python src\runway_automation_ui.py

# Test single generation
python -c "from src.runway_generator import RunwayActTwoBatchGenerator; gen = RunwayActTwoBatchGenerator('YOUR_KEY'); print('Ready')"
```

## Support

For issues or questions:
- Check verbose logging output
- Verify API key is valid
- Ensure driver videos are in assets/ folder
- Check Downloads folder for existing videos

## License

Private tool for authorized use only.

---

**Note**: This tool requires a valid RunwayML API key and incurs costs per generation.