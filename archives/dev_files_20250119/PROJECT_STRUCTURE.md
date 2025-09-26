# RunwayML Batch Automation - Project Structure

## Directory Layout

```
faggotRUNWAYS2.0/
│
├── src/                          # Source code
│   ├── runway_automation_ui.py   # Main UI application
│   ├── runway_generator.py       # RunwayML API client
│   ├── gui_selectors.py         # Tkinter GUI components
│   ├── path_utils.py            # Path resolution utilities
│   ├── first_run_setup.py       # Initial setup wizard
│   └── spinner_section_fixed.py  # UI spinner component
│
├── assets/                       # Media and resources
│   └── driver_video.mp4         # Default driver video
│
├── config/                       # Configuration files
│   └── runway_config.json       # Main application config
│
├── distribution/                 # Build and release files
│   ├── builds/                  # Compiled executables
│   ├── installer/               # Setup packages
│   ├── run_runway_ui.bat        # Legacy batch launcher
│   └── README_DISTRIBUTION.txt  # Build instructions
│
├── docs/                        # Documentation
│   ├── CLAUDE.md               # Claude AI instructions
│   ├── implementation-plan.md   # Technical implementation
│   ├── path-analysis.md        # Path handling details
│   ├── summary-report.md       # Project summary
│   └── ux-improvements.md      # UX enhancement notes
│
├── archives/                    # Backup and old files
│   └── backup-YYYYMMDD/        # Date-stamped backups
│
├── RunwayML_Batch.bat          # Main launcher script
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore patterns
└── PROJECT_STRUCTURE.md        # This file
```

## Quick Start

1. **Run the application:**
   ```
   RunwayML_Batch.bat
   ```
   or
   ```
   python src/runway_automation_ui.py
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Build executable:**
   ```
   cd distribution
   pyinstaller --onefile --windowed --name "RunwayML_Batch" ../src/runway_automation_ui.py
   ```

## Key Components

### Source Code (`/src`)
- Core Python modules for RunwayML automation
- GUI components using Tkinter
- API integration and batch processing

### Assets (`/assets`)
- Default driver videos and media files
- Icons and images (to be added)

### Configuration (`/config`)
- User settings and API keys
- Output location preferences
- Processing parameters

### Distribution (`/distribution`)
- Compiled executables for end users
- Installation packages
- Build scripts and instructions

### Documentation (`/docs`)
- Technical documentation
- Implementation details
- User guides

## Development Notes

- Python 3.8+ required
- Uses Rich library for terminal UI
- Tkinter for file/folder selection dialogs
- Supports Windows, macOS, Linux (Windows primary)
- API key required for RunwayML access

## Security Notes

- API keys stored in local config only
- No cloud sync or external dependencies
- All processing done locally
- Sensitive config excluded from version control (.gitignore)