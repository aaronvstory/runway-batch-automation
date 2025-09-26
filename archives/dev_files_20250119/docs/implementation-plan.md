# RunwayML Automation Tool - Implementation Plan

## Overview
Comprehensive plan to fix path portability issues and enhance the RunwayML automation tool for better user experience and maintainability.

## Implementation Phases

### Phase 1: Critical Path Fixes (Priority: HIGH)

#### 1.1 Fix Batch File Portability
**File:** `run_runway_ui.bat`

**Changes:**
```batch
@echo off
:: Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Rest of script uses relative paths
if not exist "runway_automation_ui.py" (
    echo Error: runway_automation_ui.py not found in %SCRIPT_DIR%
)
```

**Benefits:**
- Works from any directory
- No hardcoded C:\CLAUDE dependency
- Portable across different systems

#### 1.2 Dynamic Python Path Resolution
**Files:** `runway_automation_ui.py`, `runway_generator.py`

**Implementation:**
```python
from pathlib import Path
import os

class PathManager:
    @staticmethod
    def get_script_dir():
        """Get directory where script is located"""
        return Path(__file__).parent.absolute()

    @staticmethod
    def get_downloads_folder():
        """Get user's Downloads folder dynamically"""
        # Windows-specific
        downloads = Path.home() / "Downloads"
        if not downloads.exists():
            # Fallback to Documents
            downloads = Path.home() / "Documents"
        return downloads

    @staticmethod
    def get_default_video_path():
        """Get default driver video path"""
        # First check script directory
        script_dir = PathManager.get_script_dir()
        local_video = script_dir / "driver_videos" / "default.mp4"
        if local_video.exists():
            return local_video
        # Fallback to Downloads
        return PathManager.get_downloads_folder() / "LRx_9sec.mp4"
```

#### 1.3 Configuration System Upgrade
**New file:** `config_manager.py`

```python
class ConfigManager:
    def __init__(self):
        self.config_file = Path(__file__).parent / "runway_config.json"
        self.default_config = self.build_default_config()

    def build_default_config(self):
        """Build config with smart defaults"""
        return {
            "driver_video": str(PathManager.get_default_video_path()),
            "output_folder": str(PathManager.get_downloads_folder()),
            "api_key": os.environ.get("RUNWAY_API_KEY", ""),
            "verbose_logging": False,
            "duplicate_detection": True,
            "delay_between_generations": 1
        }

    def expand_path(self, path_str):
        """Expand environment variables and ~ in paths"""
        expanded = os.path.expandvars(os.path.expanduser(path_str))
        return Path(expanded).resolve()
```

### Phase 2: Configuration Enhancement (Priority: MEDIUM)

#### 2.1 First-Run Setup Wizard
```python
class SetupWizard:
    def run_initial_setup(self):
        """Guide user through initial configuration"""
        print("Welcome to RunwayML Automation Tool!")
        print("Let's set up your configuration...\n")

        # API Key setup
        api_key = self.get_api_key()

        # Driver video selection
        driver_video = self.select_driver_video()

        # Output folder selection
        output_folder = self.select_output_folder()

        # Save configuration
        config = {
            "api_key": api_key,
            "driver_video": driver_video,
            "output_folder": output_folder,
            "first_run_complete": True
        }
        self.save_config(config)
```

#### 2.2 Environment Variable Support
```python
# Support in config file
{
    "driver_video": "${RUNWAY_DRIVER_VIDEO:-./driver_videos/default.mp4}",
    "output_folder": "${RUNWAY_OUTPUT:-~/Downloads}",
    "api_key": "${RUNWAY_API_KEY}"
}
```

#### 2.3 Multiple Profile Support
```python
class ProfileManager:
    def __init__(self):
        self.profiles_dir = Path.home() / ".runway_profiles"
        self.profiles_dir.mkdir(exist_ok=True)

    def list_profiles(self):
        """List available profiles"""
        return [p.stem for p in self.profiles_dir.glob("*.json")]

    def load_profile(self, name):
        """Load a specific profile"""
        profile_path = self.profiles_dir / f"{name}.json"
        if profile_path.exists():
            return json.loads(profile_path.read_text())
        return None
```

### Phase 3: Error Handling & UX (Priority: MEDIUM)

#### 3.1 Path Validation System
```python
class PathValidator:
    @staticmethod
    def validate_and_fix_path(path_str, path_type="file"):
        """Validate path and provide helpful fixes"""
        path = Path(path_str)

        if not path.exists():
            # Try common fixes
            fixes = PathValidator.suggest_fixes(path, path_type)
            if fixes:
                print(f"Path not found: {path}")
                print("Suggestions:")
                for i, fix in enumerate(fixes, 1):
                    print(f"  {i}. {fix}")
                return PathValidator.prompt_for_fix(fixes)
        return path

    @staticmethod
    def suggest_fixes(path, path_type):
        """Suggest possible path corrections"""
        suggestions = []

        # Check if it's in Downloads
        downloads_path = Path.home() / "Downloads" / path.name
        if downloads_path.exists():
            suggestions.append(str(downloads_path))

        # Check current directory
        current_path = Path.cwd() / path.name
        if current_path.exists():
            suggestions.append(str(current_path))

        return suggestions
```

#### 3.2 Enhanced Error Messages
```python
class ErrorHandler:
    @staticmethod
    def handle_path_error(path, context):
        """Provide helpful error messages"""
        message = f"""
╔══════════════════════════════════════════════════════════╗
║                    PATH ERROR                             ║
╠══════════════════════════════════════════════════════════╣
║ Could not find: {path[:50]}                              ║
║                                                           ║
║ Suggestions:                                              ║
║ 1. Check if the file exists in your Downloads folder     ║
║ 2. Use the configuration menu to update the path         ║
║ 3. Place the file in: {Path.cwd()}                      ║
╚══════════════════════════════════════════════════════════╝
"""
        print(message)
```

#### 3.3 Interactive Path Picker
```python
class PathPicker:
    def pick_file(self, title="Select File", filetypes=[("All", "*.*")]):
        """Open file dialog for path selection"""
        try:
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.askopenfilename(
                title=title,
                filetypes=filetypes,
                initialdir=str(Path.home() / "Downloads")
            )

            root.destroy()
            return file_path if file_path else None
        except ImportError:
            # Fallback to manual input
            return input(f"{title}: ")
```

### Phase 4: Security Improvements (Priority: HIGH)

#### 4.1 Secure API Key Storage
```python
class SecureConfig:
    @staticmethod
    def store_api_key(api_key):
        """Store API key securely"""
        # Option 1: Environment variable
        os.environ["RUNWAY_API_KEY"] = api_key

        # Option 2: Windows Credential Manager (via keyring)
        try:
            import keyring
            keyring.set_password("runway_automation", "api_key", api_key)
        except ImportError:
            # Fallback to encoded file
            encoded = base64.b64encode(api_key.encode()).decode()
            key_file = Path.home() / ".runway_key"
            key_file.write_text(encoded)
            key_file.chmod(0o600)  # Restrict permissions
```

#### 4.2 Config Sanitization
```python
def sanitize_config_for_display(config):
    """Hide sensitive data in config display"""
    safe_config = config.copy()
    if "api_key" in safe_config:
        key = safe_config["api_key"]
        if len(key) > 10:
            safe_config["api_key"] = f"{key[:4]}...{key[-4:]}"
    return safe_config
```

### Phase 5: Testing & Validation (Priority: MEDIUM)

#### 5.1 Path Testing Suite
```python
class PathTests:
    def test_all_scenarios(self):
        """Test various path scenarios"""
        scenarios = [
            ("Normal path", "C:/Users/test/Downloads/file.mp4"),
            ("Spaces in path", "C:/Users/test user/Downloads/file.mp4"),
            ("Unicode path", "C:/Users/tëst/Downloads/файл.mp4"),
            ("Network path", "//server/share/file.mp4"),
            ("Relative path", "./downloads/file.mp4"),
            ("Home path", "~/Downloads/file.mp4")
        ]

        for name, path in scenarios:
            self.test_path_handling(name, path)
```

#### 5.2 Compatibility Checker
```python
class CompatibilityChecker:
    def check_system(self):
        """Check system compatibility"""
        checks = {
            "Python version": sys.version_info >= (3, 7),
            "Operating system": os.name == "nt",  # Windows
            "Required modules": self.check_imports(),
            "Write permissions": self.check_write_permissions(),
            "Network access": self.check_network()
        }
        return checks
```

## Implementation Timeline

### Week 1: Critical Fixes
- [ ] Fix batch file to use relative paths
- [ ] Update Python scripts to use dynamic path resolution
- [ ] Create PathManager utility class
- [ ] Test basic portability

### Week 2: Configuration System
- [ ] Implement ConfigManager with smart defaults
- [ ] Add environment variable support
- [ ] Create first-run setup wizard
- [ ] Add profile support

### Week 3: Error Handling & UX
- [ ] Implement path validation system
- [ ] Add interactive path picker
- [ ] Enhance error messages
- [ ] Add progress indicators

### Week 4: Security & Testing
- [ ] Implement secure API key storage
- [ ] Add config sanitization
- [ ] Create comprehensive test suite
- [ ] Document all changes

## Success Metrics
- Tool works from any directory location
- No hardcoded user-specific paths
- Clear error messages with solutions
- API key stored securely
- First-time setup is smooth
- Existing users' configs migrate seamlessly

## Backwards Compatibility
- Check for old config format and auto-migrate
- Preserve existing user settings
- Provide migration wizard if needed
- Keep backup of old config

## Documentation Updates Needed
1. README.md - Installation and setup instructions
2. CONFIG.md - Configuration options and examples
3. TROUBLESHOOTING.md - Common issues and solutions
4. API_SETUP.md - How to obtain and configure API key