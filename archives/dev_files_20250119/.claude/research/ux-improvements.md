# RunwayML Automation Tool - UX Improvement Plan

## Current UX Issues

### 1. Poor Error Recovery
- Cryptic error messages when paths don't exist
- No guidance on how to fix issues
- Application crashes instead of graceful handling

### 2. Confusing First-Time Experience
- Assumes user has files in specific locations
- No setup wizard or onboarding
- Hardcoded paths don't match user's system

### 3. Limited Feedback
- No clear indication of what's happening during processing
- Progress indicators don't show actual progress
- No estimation of time remaining

### 4. Configuration Difficulties
- Manual JSON editing required for some settings
- No validation of entered paths
- No way to test configuration before running

## Proposed UX Improvements

### 1. Smart Onboarding Flow

#### First-Run Detection
```python
class OnboardingManager:
    def should_show_onboarding(self):
        """Check if this is first run"""
        markers = [
            Path.home() / ".runway_setup_complete",
            Path("runway_config.json"),
            Path.home() / ".runway_profiles"
        ]
        return not any(m.exists() for m in markers)

    def show_welcome_screen(self):
        """Display attractive welcome message"""
        print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║     🚀 Welcome to RunwayML Batch Video Generator v3.0 🚀         ║
║                                                                    ║
║     Generate stunning AI videos from your image collections!       ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║     This appears to be your first time using the tool.           ║
║     Let's set everything up in just 3 easy steps!                ║
║                                                                    ║
║     • Step 1: Configure your API key                             ║
║     • Step 2: Select your driver video                           ║
║     • Step 3: Choose output folder                               ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
        """)
```

#### Guided Setup Process
```python
def guided_api_setup(self):
    """Interactive API key configuration"""
    print("\n📋 STEP 1: API Key Setup")
    print("─" * 50)
    print("\nYou'll need a RunwayML API key to use this tool.")
    print("\nOptions:")
    print("1. Enter API key now")
    print("2. Get an API key (opens browser)")
    print("3. Use demo mode (limited features)")

    choice = input("\nSelect option (1-3): ")

    if choice == "1":
        api_key = self.secure_api_input()
        self.validate_api_key(api_key)
    elif choice == "2":
        webbrowser.open("https://runwayml.com/api")
        print("\n✅ Browser opened. Come back when you have your API key.")
        input("Press Enter when ready...")
        return self.guided_api_setup()
    elif choice == "3":
        return "DEMO_MODE"
```

### 2. Enhanced Configuration Interface

#### Visual Path Selection
```python
class VisualPathSelector:
    def select_with_preview(self, path_type="video"):
        """Show file browser with preview capabilities"""
        print(f"\n📁 Select {path_type.upper()} File")
        print("─" * 50)

        # Show recent files
        recent = self.get_recent_files(path_type)
        if recent:
            print("\nRecent files:")
            for i, file in enumerate(recent[:5], 1):
                size = self.get_file_size_human(file)
                print(f"  {i}. {file.name} ({size})")
            print(f"  6. Browse for other file...")

            choice = input("\nSelect (1-6): ")
            if choice.isdigit() and 1 <= int(choice) <= 5:
                return recent[int(choice)-1]

        # Open file browser
        return self.open_file_browser(path_type)
```

#### Live Configuration Testing
```python
class ConfigTester:
    def test_configuration(self, config):
        """Test configuration before starting"""
        print("\n🔍 Testing Configuration...")
        print("─" * 50)

        tests = [
            ("API Key", self.test_api_key(config['api_key'])),
            ("Driver Video", self.test_file_exists(config['driver_video'])),
            ("Output Folder", self.test_folder_writable(config['output_folder'])),
            ("Network Access", self.test_network()),
            ("Required Libraries", self.test_dependencies())
        ]

        for name, (passed, message) in tests:
            status = "✅" if passed else "❌"
            print(f"{status} {name}: {message}")

        all_passed = all(t[1][0] for t in tests)
        if not all_passed:
            print("\n⚠️ Some tests failed. Fix issues before continuing.")
            return False

        print("\n✅ All tests passed! Ready to generate videos.")
        return True
```

### 3. Improved Progress Feedback

#### Realistic Progress Tracking
```python
class EnhancedProgress:
    def __init__(self, total_items):
        self.total = total_items
        self.current = 0
        self.start_time = time.time()
        self.eta_calculator = ETACalculator()

    def update_with_context(self, item_name, stage):
        """Update progress with detailed context"""
        self.current += 1
        eta = self.eta_calculator.calculate(self.current, self.total)

        # Clear line and show detailed status
        print(f"\r📊 Progress: {self.current}/{self.total} | "
              f"🎬 Processing: {item_name[:20]}... | "
              f"📍 Stage: {stage} | "
              f"⏱️ ETA: {eta}", end="")

    def show_stage_progress(self):
        """Show progress for current operation"""
        stages = [
            ("Loading image", 10),
            ("Resizing to 16:9", 20),
            ("Encoding image", 30),
            ("Uploading to API", 50),
            ("Generating video", 80),
            ("Downloading result", 95),
            ("Saving to disk", 100)
        ]

        for stage, percent in stages:
            self.show_mini_progress(stage, percent)
            time.sleep(0.1)  # Simulated - replace with actual operations
```

### 4. Smart Error Handling

#### Contextual Error Messages
```python
class SmartErrorHandler:
    def handle_error(self, error_type, context):
        """Provide helpful error messages with solutions"""

        error_templates = {
            "file_not_found": {
                "message": "Could not find the file: {file_path}",
                "solutions": [
                    "Check if the file was moved or renamed",
                    "Use the configuration menu to update the path",
                    "Browse for the file using option [B]"
                ],
                "auto_fix": self.try_find_similar_file
            },
            "api_error": {
                "message": "API request failed: {error_message}",
                "solutions": [
                    "Check your internet connection",
                    "Verify your API key is valid",
                    "Check RunwayML service status",
                    "Try again in a few moments"
                ],
                "auto_fix": self.try_retry_api
            },
            "permission_error": {
                "message": "Cannot write to folder: {folder_path}",
                "solutions": [
                    "Choose a different output folder",
                    "Run the application as administrator",
                    "Check folder permissions"
                ],
                "auto_fix": self.suggest_alternative_folder
            }
        }

        template = error_templates.get(error_type, {})
        self.show_error_dialog(template, context)
```

#### Recovery Options
```python
def show_error_dialog(self, template, context):
    """Show error with recovery options"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                     ⚠️ ERROR DETECTED                      ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print(f"║ {template['message'].format(**context)[:58]:<58} ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print("║ Possible solutions:                                        ║")

    for i, solution in enumerate(template['solutions'], 1):
        print(f"║   {i}. {solution[:54]:<54} ║")

    print("╠════════════════════════════════════════════════════════════╣")
    print("║ Options:                                                   ║")
    print("║   [A] Try automatic fix                                    ║")
    print("║   [R] Retry operation                                      ║")
    print("║   [S] Skip this item                                       ║")
    print("║   [Q] Quit application                                     ║")
    print("╚════════════════════════════════════════════════════════════╝")

    choice = input("\nSelect option: ").upper()
    return self.handle_recovery_choice(choice, template, context)
```

### 5. Quality of Life Features

#### Auto-Save Progress
```python
class ProgressManager:
    def __init__(self):
        self.progress_file = Path("progress.json")
        self.processed_items = set()

    def save_progress(self, item_id):
        """Save progress after each successful item"""
        self.processed_items.add(item_id)
        progress_data = {
            "processed": list(self.processed_items),
            "timestamp": datetime.now().isoformat(),
            "total_processed": len(self.processed_items)
        }
        self.progress_file.write_text(json.dumps(progress_data, indent=2))

    def can_resume(self):
        """Check if there's a previous session to resume"""
        if self.progress_file.exists():
            data = json.loads(self.progress_file.read_text())
            timestamp = datetime.fromisoformat(data['timestamp'])
            age = datetime.now() - timestamp

            if age.days < 7:  # Resume if less than a week old
                return True, data
        return False, None
```

#### Batch Operation Preview
```python
def show_operation_preview(self, items):
    """Show what will be processed before starting"""
    print("\n📋 Operation Preview")
    print("─" * 50)
    print(f"Total items to process: {len(items)}")
    print(f"Estimated time: {self.estimate_time(len(items))}")
    print(f"Output folder: {self.config['output_folder']}")
    print(f"Driver video: {Path(self.config['driver_video']).name}")

    print("\nFirst 5 items:")
    for item in items[:5]:
        print(f"  • {item.name}")

    if len(items) > 5:
        print(f"  ... and {len(items) - 5} more")

    confirm = input("\nProceed with generation? (Y/N): ")
    return confirm.upper() == 'Y'
```

### 6. Accessibility Improvements

#### Keyboard Navigation
```python
class KeyboardNav:
    def menu_with_hotkeys(self, options):
        """Menu system with keyboard shortcuts"""
        print("\n" + "─" * 50)

        hotkeys = {}
        for i, (key, label, action) in enumerate(options):
            print(f"  [{key}] {label}")
            hotkeys[key.lower()] = action
            hotkeys[str(i+1)] = action  # Also accept numbers

        print("─" * 50)
        print("Use arrow keys to navigate, Enter to select")

        choice = self.get_key_input()
        if choice in hotkeys:
            return hotkeys[choice]()
```

#### Screen Reader Support
```python
def announce(self, message, priority="normal"):
    """Announce messages for screen readers"""
    # Use Windows SAPI for announcements
    if self.screen_reader_enabled:
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")

        if priority == "high":
            speaker.Rate = 2

        speaker.Speak(message)
```

### 7. Visual Polish

#### Branded Interface
```python
def show_branded_header(self):
    """Show consistent branded header"""
    gradient_colors = ["96", "95", "94", "93", "92"]  # Cyan to green gradient

    logo_lines = [
        "██████╗ ██╗   ██╗███╗   ██╗██╗    ██╗ █████╗ ██╗   ██╗",
        "██╔══██╗██║   ██║████╗  ██║██║    ██║██╔══██╗╚██╗ ██╔╝",
        "██████╔╝██║   ██║██╔██╗ ██║██║ █╗ ██║███████║ ╚████╔╝ ",
        "██╔══██╗██║   ██║██║╚██╗██║██║███╗██║██╔══██║  ╚██╔╝  ",
        "██║  ██║╚██████╔╝██║ ╚████║╚███╔███╔╝██║  ██║   ██║   ",
        "╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝   "
    ]

    for i, line in enumerate(logo_lines):
        color = gradient_colors[min(i, len(gradient_colors)-1)]
        print(f"\033[{color}m{line}\033[0m")

    print("\n" + "─" * 60)
    print("         Batch Video Generator v3.0 - AI Powered")
    print("─" * 60)
```

#### Status Icons
```python
STATUS_ICONS = {
    "ready": "🟢",
    "processing": "🔄",
    "complete": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "folder": "📁",
    "video": "🎬",
    "image": "🖼️",
    "config": "⚙️",
    "time": "⏱️",
    "network": "🌐"
}

def format_status(self, status, message):
    """Format status messages with icons"""
    icon = self.STATUS_ICONS.get(status, "•")
    return f"{icon} {message}"
```

## Implementation Priority

### Phase 1: Critical UX (Week 1)
- First-run detection and setup wizard
- Better error messages with solutions
- Path validation and auto-fix attempts

### Phase 2: Progress & Feedback (Week 2)
- Realistic progress tracking with ETA
- Stage-based progress indicators
- Operation preview before processing

### Phase 3: Polish & Accessibility (Week 3)
- Branded interface elements
- Keyboard navigation
- Visual consistency improvements

### Phase 4: Advanced Features (Week 4)
- Resume interrupted sessions
- Batch operation management
- Configuration profiles

## Success Metrics
- First-time setup completion rate > 90%
- Error recovery success rate > 75%
- User-reported issues reduced by 50%
- Average time to first successful generation < 5 minutes
- Configuration errors reduced by 80%