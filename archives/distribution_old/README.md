# RunwayML Batch Automation - Distribution

## 📦 Compiled Executable

The compiled Windows executable is located at:
```
dist\RunwayML_Batch.exe
```

**File Size:** ~60 MB
**Icon:** Custom "R" icon with gradient background

## 🚀 Running the Application

### Option 1: Use the Compiled EXE (Recommended)
```bash
dist\RunwayML_Batch.exe
```

### Option 2: Build from Source
```bash
build.bat
```

## 🛠️ Building from Source

### Requirements
- Python 3.8 or higher
- PyInstaller (`pip install pyinstaller`)

### Build Steps
1. Navigate to the `distribution` folder
2. Run `build.bat`
3. The executable will be created in `dist\RunwayML_Batch.exe`

## 📂 Distribution Structure

```
distribution/
├── dist/                     # Compiled executable
│   └── RunwayML_Batch.exe   # Main application (60MB)
├── build/                    # Build artifacts (temp)
├── runway_batch.spec         # PyInstaller specification
├── build.bat                 # Build automation script
└── README.md                 # This file
```

## ⚙️ Configuration

The application looks for configuration in:
```
config/runway_config.json
```

First-time users will be guided through setup wizard.

## 🎨 Features

- **Organized Menu**: Sectioned interface for better usability
- **Rich UI**: Beautiful terminal interface with progress bars
- **Batch Processing**: Process multiple GenX images automatically
- **Duplicate Detection**: Intelligent file management
- **Two Output Modes**: Centralized or co-located with source

## 📋 System Requirements

- Windows 10/11
- 100MB free disk space
- RunwayML API key
- Internet connection for API calls

## 🔧 Troubleshooting

If the executable doesn't run:
1. Check antivirus isn't blocking it
2. Run as administrator if needed
3. Ensure all dependencies are in the same folder
4. Use Python source version as fallback

## 📝 Version History

- v1.0.0 - Initial release with organized menu and R icon
- Compiled: 2025

## 🤝 Support

For issues or questions, check the main project documentation or run the application with Help option (H).