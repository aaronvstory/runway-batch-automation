# RunwayML Automation Tool - Path Dependency Analysis

## Executive Summary
The RunwayML automation tool has critical path portability issues due to extensive hardcoded absolute paths. The tool will only work if placed in C:\CLAUDE directory and uses hardcoded user-specific paths (C:\Users\ashrv\Downloads).

## Critical Issues Identified

### 1. Batch File Hardcoded Paths
**File:** `run_runway_ui.bat`
- **Line 7:** `cd /d "C:\CLAUDE"` - Forces execution from specific directory
- **Lines 10, 18:** Error messages reference C:\CLAUDE explicitly
- **Impact:** Script fails if not in exact C:\CLAUDE location

### 2. Python Configuration Defaults
**File:** `runway_automation_ui.py`
- **Lines 22-23:** Default config uses hardcoded paths:
  - `r"C:\Users\ashrv\Downloads\LRx_9sec.mp4"`
  - `r"C:\Users\ashrv\Downloads"`
- **Impact:** New users must manually edit config for their username

### 3. Generator Class Hardcoded Paths
**File:** `runway_generator.py`
- **Line 18:** `self.driver_video_path = r"C:\Users\ashrv\Downloads\LRx_9sec.mp4"`
- **Line 27:** `self.downloads_folder = r"C:\Users\ashrv\Downloads"`
- **Line 367:** Default parameter with hardcoded path
- **Line 513:** Hardcoded output directory
- **Line 560:** UI text displays hardcoded path
- **Impact:** Core functionality tied to specific user folder

### 4. Configuration File Issues
**File:** `runway_config.json`
- Contains user-specific paths with username "ashrv"
- API key exposed in plaintext (security concern)
- No environment variable substitution

## Path Dependencies Map

```
run_runway_ui.bat
├── Expects: C:\CLAUDE\runway_automation_ui.py
├── Expects: C:\CLAUDE\runway_generator.py
└── Changes directory to: C:\CLAUDE

runway_automation_ui.py
├── Default driver video: C:\Users\ashrv\Downloads\LRx_9sec.mp4
├── Default output: C:\Users\ashrv\Downloads
└── Loads: ./runway_config.json

runway_generator.py
├── Hardcoded driver: C:\Users\ashrv\Downloads\LRx_9sec.mp4
├── Hardcoded downloads: C:\Users\ashrv\Downloads
└── Creates temp folder: ./temp_resized

runway_config.json
├── driver_video: C:\Users\ashrv\Downloads\LRx_9sec.mp4
└── output_folder: C:\Users\ashrv\Downloads
```

## Best Practices for Windows Path Handling

### 1. Use Relative Paths
- Replace `cd /d "C:\CLAUDE"` with `cd /d "%~dp0"` (batch file's directory)
- Use `os.path.dirname(os.path.abspath(__file__))` in Python

### 2. Environment Variables
- Use `%USERPROFILE%` in batch files
- Use `os.path.expanduser("~")` in Python for user home
- Use `os.environ.get("USERPROFILE")` for Windows user folder

### 3. Configuration Flexibility
- Allow environment variable expansion in config
- Provide sensible defaults based on current location
- Support both absolute and relative paths

### 4. Path Construction
- Use `pathlib.Path` for cross-platform compatibility
- Use `os.path.join()` instead of string concatenation
- Normalize paths with `os.path.normpath()`

### 5. Dynamic Path Resolution
```python
# Get script directory
script_dir = Path(__file__).parent.absolute()

# Get user's Downloads folder
downloads_folder = Path.home() / "Downloads"

# Get Windows user profile
user_profile = Path(os.environ.get("USERPROFILE", Path.home()))
```

## Recommended Solution Architecture

### Phase 1: Immediate Fixes
1. Update batch file to use relative paths
2. Replace hardcoded Python paths with dynamic resolution
3. Update default config to use environment variables

### Phase 2: Configuration Enhancement
1. Implement path validation and auto-correction
2. Add first-run setup wizard for paths
3. Support multiple config profiles

### Phase 3: Polish & UX
1. Add path picker dialogs
2. Implement path existence checking
3. Add helpful error messages with solutions

## Security Concerns
- API key stored in plaintext in config
- Should use environment variables or secure storage
- Config file should not be committed to version control

## Testing Requirements
- Test from different directories
- Test with different usernames
- Test with spaces in paths
- Test with non-ASCII characters in paths