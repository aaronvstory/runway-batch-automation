import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Import path utilities for dynamic path resolution
from path_utils import path_manager

# Import GUI selectors for file/folder selection
from gui_selectors import GUISelectors, VideoInfo

# Import your existing RunwayActTwoBatchGenerator
from runway_generator import RunwayActTwoBatchGenerator

class RunwayAutomationUI:
    def __init__(self):
        # Get path relative to script location
        script_dir = Path(__file__).parent.parent
        self.config_file = str(script_dir / "config" / "runway_config.json")
        self.config = self.load_config()
        self.verbose_logging = self.config.get("verbose_logging", False)  # Default OFF
        self.setup_logging()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        # Use path utilities to get smart defaults
        default_driver = path_manager.get_default_driver_video()
        driver_video_path = str(default_driver) if default_driver else ""

        default_config = {
            "driver_video": driver_video_path,
            "output_folder": str(path_manager.downloads_dir),
            "api_key": "",  # Empty by default for security
            "verbose_logging": False,  # Default OFF
            "duplicate_detection": True,
            "delay_between_generations": 1,
            "first_run": True,  # Track if this is first time setup
            "image_search_pattern": "genx",  # Default pattern to search for in image filenames
            "exact_match": False,  # If true, requires exact pattern match (e.g., "-selfie" won't match "selfie")
            "output_location": "centralized"  # "centralized" or "co-located"
        }

        try:
            config_path = path_manager.resolve_path(self.config_file)
            if config_path.exists():
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Resolve paths in loaded config
                    if 'driver_video' in loaded_config:
                        loaded_config['driver_video'] = str(path_manager.resolve_path(loaded_config['driver_video']))
                    if 'output_folder' in loaded_config:
                        loaded_config['output_folder'] = str(path_manager.resolve_path(loaded_config['output_folder']))
                    return {**default_config, **loaded_config}
        except Exception:
            pass
        return default_config
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            if self.verbose_logging:
                print(f"Error saving config: {e}")
    
    def setup_logging(self):
        """Setup logging based on verbose setting"""
        if self.verbose_logging:
            logging.basicConfig(
                level=logging.INFO, 
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler('runway_automation.log'),
                    logging.StreamHandler()
                ]
            )
        else:
            # Disable verbose logging - only errors to file
            logging.basicConfig(
                level=logging.ERROR,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[logging.FileHandler('runway_automation.log')]
            )
            # Suppress all the spam
            logging.getLogger().setLevel(logging.CRITICAL)
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_cyan(self, text):
        """Print text in cyan color"""
        print(f"\033[96m{text}\033[0m")
    
    def print_light_purple(self, text):
        """Print text in light purple color"""
        print(f"\033[94m{text}\033[0m")
    
    def print_magenta(self, text):
        """Print text in magenta color"""  
        print(f"\033[95m{text}\033[0m")
        
    def print_green(self, text):
        """Print text in green color"""
        print(f"\033[92m{text}\033[0m", end="")
    
    def print_yellow(self, text):
        """Print text in yellow color"""
        print(f"\033[93m{text}\033[0m")
        
    def print_red(self, text):
        """Print text in red color"""
        print(f"\033[91m{text}\033[0m")
    
    def display_header(self):
        """Display the main header with beautiful ASCII art"""
        self.clear_screen()

        # Top border
        self.print_cyan("=" * 79)
        print()

        # ASCII Art for "RunwayML Batch"
        ascii_art = [
            "╦═╗╦ ╦╔╗╔╦ ╦╔═╗╦ ╦╔╦╗╦     ╔╗ ╔═╗╔╦╗╔═╗╦ ╦",
            "╠╦╝║ ║║║║║║║╠═╣╚╦╝║║║║     ╠╩╗╠═╣ ║ ║  ╠═╣",
            "╩╚═╚═╝╝╚╝╚╩╝╩ ╩ ╩ ╩ ╩╩═╝   ╚═╝╩ ╩ ╩ ╚═╝╩ ╩"
        ]

        # Center and print ASCII art in light purple
        for line in ascii_art:
            padding = (79 - len(line)) // 2
            self.print_light_purple(" " * padding + line)

        print()

        # Bottom border
        self.print_cyan("=" * 79)
        print()
        print()
    
    def display_configuration_menu(self):
        """Display configuration setup menu with video status"""
        # Configuration Setup section
        self.print_magenta("Configuration Setup:")
        print("Please configure your automation settings below")
        print()

        # Current Settings Display with visual box
        print("-" * 79)
        self.print_cyan("CURRENT SETTINGS:")
        print("-" * 79)

        # Image Search Pattern
        pattern = self.config.get('image_search_pattern', 'genx')
        exact = self.config.get('exact_match', False)
        print(f"  \033[92m✓ Image Pattern:\033[0m \033[93m{pattern}\033[0m (Mode: \033[96m{'Exact' if exact else 'Contains'}\033[0m)")

        # Driver Video Status with full path
        driver_video = self.config.get('driver_video', '')
        if driver_video and Path(driver_video).exists():
            video_name = Path(driver_video).name
            duration, formatted = VideoInfo.get_duration(driver_video)
            print(f"  \033[92m✓ Driver Video:\033[0m")
            print(f"    File: \033[97m{video_name}\033[0m")
            print(f"    Path: \033[90m{driver_video}\033[0m")
            if duration:
                print(f"    Duration: \033[93m{formatted}\033[0m")
        else:
            print(f"  \033[91m✗ Driver Video: NOT CONFIGURED\033[0m")
            print(f"    \033[93mPress '1' to browse and select a video file\033[0m")

        print()

        # Output Folder Status with free space
        # Output location strategy
        output_location = self.config.get("output_location", "centralized")
        output_folder = self.config.get('output_folder', '')

        if output_location == "co-located":
            print(f"  \033[92m✓ Output Location: Same folder as source images\033[0m")
            print(f"    \033[96mVideos will be saved next to their source images\033[0m")
        else:
            if output_folder and Path(output_folder).exists():
                print(f"  \033[92m✓ Output Folder:\033[0m")
                print(f"    Path: \033[97m{output_folder}\033[0m")
                try:
                    import shutil
                    free_gb = shutil.disk_usage(output_folder).free / (1024**3)
                    print(f"    Free Space: \033[93m{free_gb:.1f} GB\033[0m")
                except:
                    pass
            else:
                print(f"  \033[91m✗ Output Folder: NOT CONFIGURED\033[0m")
                print(f"    \033[93mPress '2' to browse and select output folder\033[0m")

        print("-" * 79)
        print()

        # Available Options section
        self.print_cyan("Available Options:")

        # Menu options with GUI selectors
        verbose_status = "ON" if self.verbose_logging else "OFF"

        # Configuration Section
        print()
        print("  \033[96m── CONFIGURATION ───────────────────────────────────────\033[0m")
        print(f"  \033[93m1\033[0m - \033[92mBrowse\033[0m for driver video (opens file browser)")
        print(f"  \033[93m2\033[0m - \033[92mBrowse\033[0m for output folder (opens folder browser)")
        print(f"  \033[93m3\033[0m - Toggle output location: {self.get_output_location_display()}")

        # Processing Section
        print()
        print("  \033[96m── PROCESSING ──────────────────────────────────────────\033[0m")
        print(f"  \033[93m4\033[0m - \033[92m🎯 Browse for INPUT folder\033[0m (select images to process)")
        print(f"  \033[93m5\033[0m - \033[92m▶ START BATCH PROCESSING\033[0m (after setup)")

        # Image Pattern Configuration
        print()
        print("  \033[96m── IMAGE SELECTION ─────────────────────────────────────\033[0m")
        pattern = self.config.get('image_search_pattern', 'genx')
        exact = "Exact" if self.config.get('exact_match', False) else "Contains"
        print(f"  \033[93m6\033[0m - Configure search pattern (current: \033[92m{pattern}\033[0m, mode: \033[93m{exact}\033[0m)")
        print(f"  \033[93m7\033[0m - \033[96m🔍 DRY RUN SCAN\033[0m - Preview which images will be processed")

        # Advanced Options
        print()
        print("  \033[96m── ADVANCED OPTIONS ────────────────────────────────────\033[0m")
        api_status = "✓ Set" if self.config.get('api_key') else "✗ Not Set"
        print(f"  \033[93m8\033[0m - Configure API key (current: \033[92m{api_status}\033[0m)")
        print(f"  \033[93m9\033[0m - Edit driver video path (manual text entry)")
        print(f"  \033[93m10\033[0m - Edit output folder path (manual text entry)")
        print(f"  \033[93m11\033[0m - Toggle verbose logging (currently: {verbose_status})")
        print(f"  \033[93m12\033[0m - Show all settings in detail")

        # System
        print()
        print("  \033[96m── SYSTEM ──────────────────────────────────────────────\033[0m")
        print(f"  \033[93mS\033[0m - Run Setup Wizard (reconfigure all settings)")
        print(f"  \033[93mH\033[0m - Help & documentation")
        print(f"  \033[93mQ\033[0m - Quit")

        print()
        print("  " + "─" * 57)

        # Input prompt - exact match
        self.print_green("  Enter your selection:")
    
    def get_output_location_display(self):
        """Get display text for output location setting"""
        if self.config.get("output_location", "centralized") == "co-located":
            return "\033[92mSame as source\033[0m"
        else:
            return "\033[93mCentralized folder\033[0m"

    def toggle_output_location(self):
        """Toggle between centralized and co-located output"""
        current = self.config.get("output_location", "centralized")
        new_location = "co-located" if current == "centralized" else "centralized"
        self.config["output_location"] = new_location
        self.save_config()

        if new_location == "co-located":
            print("\n✓ Output videos will be saved in the same folder as source images")
        else:
            print(f"\n✓ Output videos will be saved to: {self.config['output_folder']}")

        input("Press Enter to continue...")

    def show_help(self):
        """Show help documentation"""
        self.clear_screen()
        print("\n" + "=" * 79)
        self.print_cyan("📖 RUNWAYML BATCH AUTOMATION - HELP")
        print("=" * 79)
        print()
        print("  \033[96m── OVERVIEW ────────────────────────────────────────────\033[0m")
        print("  This tool automates RunwayML Act Two video generation from")
        print("  character images. It processes GenX image folders recursively")
        print("  and generates videos using the RunwayML API.")
        print()
        print("  \033[96m── QUICK START ─────────────────────────────────────────\033[0m")
        print("  1. Configure driver video (Option 1)")
        print("  2. Set output folder (Option 2)")
        print("  3. Browse for images to process (Option 4)")
        print()
        print("  \033[96m── OUTPUT MODES ────────────────────────────────────────\033[0m")
        print("  • Centralized: All videos saved to one folder")
        print("  • Co-located: Videos saved with source images")
        print()
        print("  \033[96m── FEATURES ────────────────────────────────────────────\033[0m")
        print("  • Duplicate detection (checks Downloads folder)")
        print("  • Recursive folder scanning")
        print("  • GenX image filtering")
        print("  • Progress tracking with Rich UI")
        print()
        print("  \033[96m── REQUIREMENTS ────────────────────────────────────────\033[0m")
        print("  • Valid RunwayML API key")
        print("  • Driver video (MP4 format)")
        print("  • GenX character images")
        print()
        input("  Press Enter to return to menu...")

    def select_input_folder_gui(self):
        """Select input folder using GUI browser"""
        gui = GUISelectors()
        result = gui.select_input_folder_with_scan()

        if result:
            folder_path, image_count = result
            print(f"\n✓ Selected input folder: {folder_path}")
            print(f"  Found {image_count} images to process")
            input("\nPress Enter to start processing...")
            return folder_path
        else:
            print("\nNo folder selected.")
            input("Press Enter to continue...")
            return None

    def toggle_verbose_logging(self):
        """Toggle verbose logging on/off"""
        self.verbose_logging = not self.verbose_logging
        self.config["verbose_logging"] = self.verbose_logging
        self.save_config()
        self.setup_logging()  # Reconfigure logging

        status = "enabled" if self.verbose_logging else "disabled"
        print(f"\nVerbose logging {status}")
        input("Press Enter to continue...")
    
    def edit_driver_video(self):
        """Edit the driver video path"""
        print(f"\n\033[92mCurrent driver video:\033[0m {self.config['driver_video']}")
        new_path = input("\033[92mEnter new driver video path (or press Enter to keep current):\033[0m ").strip()
        
        if new_path and Path(new_path).exists():
            self.config['driver_video'] = new_path
            self.save_config()
            print(f"Driver video updated to: {new_path}")
        elif new_path:
            self.print_red(f"File not found: {new_path}")
        
        input("Press Enter to continue...")
    
    def edit_output_folder(self):
        """Edit the output folder path"""
        print(f"\n\033[92mCurrent output folder:\033[0m {self.config['output_folder']}")
        new_path = input("\033[92mEnter new output folder path (or press Enter to keep current):\033[0m ").strip()
        
        if new_path:
            try:
                Path(new_path).mkdir(parents=True, exist_ok=True)
                self.config['output_folder'] = new_path
                self.save_config()
                print(f"Output folder updated to: {new_path}")
            except Exception as e:
                self.print_red(f"Error creating folder: {e}")
        
        input("Press Enter to continue...")
    
    def select_driver_video_gui(self):
        """Select driver video using GUI file dialog or from assets"""
        gui_selector = GUISelectors()
        current_video = self.config.get('driver_video', '')

        print("\n" + "=" * 79)
        self.print_cyan("🎬 SELECT DRIVER VIDEO")
        print("=" * 79)

        if current_video and Path(current_video).exists():
            print(f"Current: {Path(current_video).name}")
            print()

        # Check for videos in assets folder first
        assets_videos = path_manager.get_all_driver_videos()

        if assets_videos:
            self.print_green(f"✓ Found {len(assets_videos)} video(s) in assets folder:")
            print()
            for i, video in enumerate(assets_videos, 1):
                duration, formatted = VideoInfo.get_duration(str(video))
                duration_str = f" ({formatted})" if duration else ""
                print(f"  {i}. {video.name}{duration_str}")

            print("\nOptions:")
            print(f"  1-{len(assets_videos)} = Select from assets")
            print("  B = Browse for different video")
            print("  C = Cancel")

            choice = input("\nYour choice: ").strip().lower()

            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(assets_videos):
                    selected = str(assets_videos[idx])
                    self.config['driver_video'] = selected
                    self.save_config()
                    self.print_green(f"✅ Selected: {assets_videos[idx].name}")
                    input("\nPress Enter to return to menu...")
                    return
            elif choice == 'c':
                input("\nPress Enter to return to menu...")
                return
            elif choice != 'b':
                self.print_red("Invalid choice.")
                input("\nPress Enter to return to menu...")
                return

        # If no assets videos or user chose to browse
        self.print_yellow("Opening Windows file browser...")
        print("Please select your driver video file.")

        selected = gui_selector.select_driver_video(current_video)

        if selected:
            self.config['driver_video'] = selected
            self.save_config()

            print()
            self.print_green("✅ SUCCESS! Driver video updated:")
            print(f"  File: \033[97m{Path(selected).name}\033[0m")
            print(f"  Path: \033[90m{selected}\033[0m")

            # Show duration
            duration, formatted = VideoInfo.get_duration(selected)
            if duration:
                print(f"  Duration: \033[93m{formatted}\033[0m")
        else:
            self.print_yellow("❌ No file selected - keeping current setting.")

        input("\nPress Enter to return to menu...")

    def select_output_folder_gui(self):
        """Select output folder using GUI dialog"""
        gui_selector = GUISelectors()
        current_folder = self.config.get('output_folder', '')

        print("\n" + "=" * 79)
        self.print_cyan("📁 BROWSE FOR OUTPUT FOLDER")
        print("=" * 79)

        if current_folder and Path(current_folder).exists():
            print(f"Current: {current_folder}")
            print()

        self.print_yellow("Opening Windows folder browser...")
        print("Please select where generated videos should be saved.")

        selected = gui_selector.select_output_folder(current_folder)

        if selected:
            self.config['output_folder'] = selected
            self.save_config()

            print()
            self.print_green("✅ SUCCESS! Output folder updated:")
            print(f"  Path: \033[97m{selected}\033[0m")

            # Check free space
            try:
                import shutil
                free_gb = shutil.disk_usage(selected).free / (1024**3)
                print(f"  Free Space: \033[93m{free_gb:.1f} GB\033[0m")

                if free_gb < 10:
                    self.print_yellow("  ⚠ Low disk space warning - videos need storage space")
                else:
                    self.print_green("  ✓ Plenty of space available")
            except:
                pass
        else:
            self.print_yellow("❌ No folder selected - keeping current setting.")

        input("\nPress Enter to return to menu...")

    def show_all_settings(self):
        """Display all current settings in a GUI dialog"""
        gui_selector = GUISelectors()
        self.print_cyan("\n📋 Showing all settings...")
        gui_selector.show_current_settings(self.config)
        input("\nPress Enter to continue...")

    def edit_api_details(self):
        """Edit API key and other RunwayML details"""
        print(f"\nCurrent API key: {self.config['api_key'][:20]}...")

        choice = input("Do you want to update the API key? (y/n): ").strip().lower()
        if choice == 'y':
            new_key = input("Enter new API key: ").strip()
            if new_key:
                self.config['api_key'] = new_key
                self.save_config()
                print("API key updated")

        input("Press Enter to continue...")

    def configure_api_key(self):
        """Configure the RunwayML API key"""
        self.clear_screen()
        self.print_cyan("═" * 79)
        self.print_yellow("Configure RunwayML API Key")
        self.print_cyan("═" * 79)
        print()

        current_key = self.config.get('api_key', '')
        if current_key:
            masked = current_key[:10] + "..." + current_key[-4:] if len(current_key) > 20 else "***"
            print(f"  Current API key: \033[92m{masked}\033[0m")
        else:
            print(f"  Current API key: \033[91mNot Set\033[0m")

        print()
        print("  Get your API key from: https://app.runwayml.com/api")
        print()
        print("  Enter new API key (or press Enter to keep current):")

        new_key = input("  > ").strip()
        if new_key:
            if new_key.startswith("key_") and len(new_key) > 20:
                self.config['api_key'] = new_key
                self.save_config()
                self.print_green("\n✓ API key updated successfully!")
            else:
                self.print_red("\n✗ Invalid API key format. RunwayML keys start with 'key_'")
        else:
            self.print_yellow("\n✓ API key unchanged")

        time.sleep(2)

    def configure_image_search_pattern(self):
        """Configure the pattern to search for in image filenames"""
        self.clear_screen()
        self.print_cyan("═" * 79)
        self.print_yellow("Configure Image Search Pattern")
        self.print_cyan("═" * 79)
        print()

        current_pattern = self.config.get('image_search_pattern', 'genx')
        exact_match = self.config.get('exact_match', False)

        print(f"  Current pattern: \033[93m{current_pattern}\033[0m")
        print(f"  Exact match: \033[93m{'Yes' if exact_match else 'No'}\033[0m")
        print()
        print("  Examples:")
        if not exact_match:
            print(f"    Pattern 'selfie' matches: selfie.jpg, my-selfie.png, selfie-2024.jpg")
            print(f"    Pattern '-selfie' matches: my-selfie.jpg, test-selfie.png")
        else:
            print(f"    Pattern 'selfie' (exact) matches: selfie.jpg but NOT my-selfie.jpg")
            print(f"    Pattern '-selfie' (exact) matches: test-selfie.jpg but NOT selfie.jpg")
        print()
        print("  Enter new pattern (or press Enter to keep current):")

        new_pattern = input("  > ").strip()
        if new_pattern:
            self.config['image_search_pattern'] = new_pattern
            print()
            print("  Enable exact matching? (y/n)")
            print("    Yes = pattern must appear exactly as specified")
            print("    No = pattern can appear anywhere in filename")
            exact_input = input("  > ").strip().lower()
            self.config['exact_match'] = exact_input == 'y'

            self.save_config()
            self.print_green(f"\n✓ Pattern updated to: '{new_pattern}' (Exact: {'Yes' if self.config['exact_match'] else 'No'})")
        else:
            self.print_yellow("\n✓ Pattern unchanged")

        time.sleep(2)

    def perform_dry_run_scan(self):
        """Perform a dry run scan to show which images will be processed"""
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.align import Align
        from rich.text import Text
        import humanize

        console = Console(force_terminal=True, width=100)

        # Get input folder
        gui = GUISelectors()
        result = gui.select_input_folder()

        if not result:
            self.print_red("\n✗ No folder selected")
            time.sleep(2)
            return

        input_folder, _ = result
        self.clear_screen()

        # Header
        header_text = Text()
        header_text.append("🔍 DRY RUN SCAN RESULTS 🔍", style="bold cyan")
        console.print(Panel(Align.center(header_text), style="bright_blue"))

        # Get search pattern
        pattern = self.config.get('image_search_pattern', 'genx')
        exact_match = self.config.get('exact_match', False)

        # Show search criteria
        console.print(f"\n📋 Search Pattern: [yellow]{pattern}[/yellow]")
        console.print(f"🎯 Match Type: [yellow]{'Exact' if exact_match else 'Contains'}[/yellow]")
        console.print(f"📁 Root Folder: [cyan]{input_folder}[/cyan]\n")

        # Scan for matching images
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff', '.tif'}
        matching_files = []
        total_size = 0

        # Scan recursively
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in image_extensions:
                    filename_lower = file.lower()
                    pattern_lower = pattern.lower()

                    # Check if file matches pattern
                    matches = False
                    if exact_match:
                        # For exact match, check if pattern appears as a complete word/segment
                        import re
                        # Pattern should match as a complete segment (bounded by non-alphanumeric or start/end)
                        pattern_regex = r'(^|[^a-z0-9])' + re.escape(pattern_lower) + r'([^a-z0-9]|$)'
                        if re.search(pattern_regex, filename_lower):
                            matches = True
                    else:
                        # Simple contains check
                        if pattern_lower in filename_lower:
                            matches = True

                    if matches:
                        file_size = file_path.stat().st_size
                        total_size += file_size
                        relative_path = file_path.relative_to(input_folder)
                        matching_files.append({
                            'path': str(relative_path),
                            'name': file,
                            'size': file_size,
                            'folder': str(relative_path.parent) if relative_path.parent != Path('.') else 'root'
                        })

        # Sort files by folder then by name
        matching_files.sort(key=lambda x: (x['folder'], x['name']))

        if not matching_files:
            console.print(Panel(f"[red]No images found matching pattern: '{pattern}'[/red]", style="red"))
            input("\nPress Enter to continue...")
            return

        # Create table
        table = Table(title=f"Found {len(matching_files)} Matching Images", show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=5)
        table.add_column("Folder", style="yellow", width=30)
        table.add_column("Filename", style="green", width=35)
        table.add_column("Size", style="blue", justify="right", width=10)

        # Add rows
        for idx, file_info in enumerate(matching_files, 1):
            size_str = humanize.naturalsize(file_info['size'], binary=True)
            table.add_row(
                str(idx),
                file_info['folder'],
                file_info['name'],
                size_str
            )

        console.print(table)

        # Summary
        console.print(f"\n📊 [bold]Summary:[/bold]")
        console.print(f"  • Total Images: [green]{len(matching_files)}[/green]")
        console.print(f"  • Total Size: [blue]{humanize.naturalsize(total_size, binary=True)}[/blue]")
        console.print(f"  • Unique Folders: [yellow]{len(set(f['folder'] for f in matching_files))}[/yellow]")

        # Ask to proceed
        console.print(f"\n[bold cyan]Would you like to proceed with processing these {len(matching_files)} images?[/bold cyan]")
        console.print("[green]Y[/green] - Yes, start processing")
        console.print("[red]N[/red] - No, return to menu")

        choice = input("\nYour choice (Y/N): ").strip().lower()

        if choice == 'y':
            # Start actual processing
            self.start_processing(input_folder)
        else:
            console.print("\n[yellow]Returning to menu...[/yellow]")
            time.sleep(1)

    def show_detailed_settings(self):
        """Display all current settings in detail"""
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.align import Align

        console = Console(force_terminal=True, width=100)
        self.clear_screen()

        # Header
        console.print(Panel(Align.center("⚙️  CURRENT CONFIGURATION  ⚙️", style="bold cyan"), style="bright_blue"))

        # Create settings table
        table = Table(show_header=True, header_style="bold magenta", title="All Settings")
        table.add_column("Setting", style="cyan", width=30)
        table.add_column("Value", style="yellow", width=50)
        table.add_column("Status", style="green", width=15)

        # Add settings rows
        settings = [
            ("API Key", self.config.get('api_key', ''), "✓ Set" if self.config.get('api_key') else "✗ Not Set"),
            ("Driver Video", self.config.get('driver_video', 'Not Set'), "✓" if Path(self.config.get('driver_video', '')).exists() else "✗"),
            ("Output Folder", self.config.get('output_folder', 'Not Set'), "✓" if Path(self.config.get('output_folder', '')).exists() else "✗"),
            ("Output Location", self.config.get('output_location', 'centralized'), "✓"),
            ("Image Search Pattern", self.config.get('image_search_pattern', 'genx'), "✓"),
            ("Exact Match", "Yes" if self.config.get('exact_match', False) else "No", "✓"),
            ("Verbose Logging", "ON" if self.config.get('verbose_logging', False) else "OFF", "✓"),
            ("Duplicate Detection", "ON" if self.config.get('duplicate_detection', True) else "OFF", "✓"),
            ("Generation Delay", f"{self.config.get('delay_between_generations', 1)} seconds", "✓"),
        ]

        for setting, value, status in settings:
            # Truncate long values
            if setting == "API Key" and value:
                display_value = f"{value[:10]}...{value[-10:]}" if len(value) > 25 else value
            elif len(str(value)) > 50:
                display_value = str(value)[:47] + "..."
            else:
                display_value = str(value)

            table.add_row(setting, display_value, status)

        console.print(table)

        # Show pattern matching examples
        pattern = self.config.get('image_search_pattern', 'genx')
        exact = self.config.get('exact_match', False)

        console.print("\n[bold cyan]Pattern Matching Examples:[/bold cyan]")
        if exact:
            console.print(f"  Pattern '[yellow]{pattern}[/yellow]' with EXACT matching:")
            console.print(f"    ✓ Matches: photo{pattern}.jpg, test{pattern}image.png")
            console.print(f"    ✗ Doesn't match: {pattern[1:] if pattern else 'x'}.jpg, my{pattern[:-1] if pattern else 'x'}pic.png")
        else:
            console.print(f"  Pattern '[yellow]{pattern}[/yellow]' with CONTAINS matching:")
            console.print(f"    ✓ Matches: {pattern}.jpg, my-{pattern}-pic.png, test{pattern}123.jpg")
            console.print(f"    ✗ Doesn't match: {'xyz' if pattern != 'xyz' else 'abc'}.jpg")

        input("\n\nPress Enter to continue...")

    def run_setup_wizard(self):
        """Manually run the setup wizard to reconfigure all settings"""
        from first_run_setup import FirstRunSetup

        self.clear_screen()
        wizard = FirstRunSetup()
        wizard.run(preserve_existing=True)
        self.print_green("\nConfiguration updated! Reloading settings...")
        time.sleep(2)

    def run_configuration_menu(self):
        """Main configuration menu loop with GUI options"""
        while True:
            self.display_header()
            self.display_configuration_menu()

            choice = input(" ").strip().lower()

            if choice == 'q':
                print("\nGoodbye!")
                sys.exit(0)
            elif choice == '1':
                # GUI driver video selector
                self.select_driver_video_gui()
                continue
            elif choice == '2':
                # GUI output folder selector
                self.select_output_folder_gui()
                continue
            elif choice == '3':
                # Toggle output location strategy
                self.toggle_output_location()
                continue
            elif choice == '4':
                # GUI input folder selector - primary way to select images
                result = self.select_input_folder_gui()
                if result:
                    return result
                continue
            elif choice == '5':
                # Start batch processing (same as option 4)
                result = self.select_input_folder_gui()
                if result:
                    return result
                continue
            elif choice == '6':
                # Configure search pattern
                self.configure_image_search_pattern()
                continue
            elif choice == '7':
                # Dry run scan
                self.perform_dry_run_scan()
                continue
            elif choice == '8':
                # Configure API key
                self.configure_api_key()
                continue
            elif choice == '9':
                # Manual driver video edit
                self.edit_driver_video()
                continue
            elif choice == '10':
                # Manual output folder edit
                self.edit_output_folder()
                continue
            elif choice == '11':
                # Toggle verbose logging
                self.toggle_verbose_logging()
                continue
            elif choice == '12':
                # Show all settings in detail
                self.show_detailed_settings()
                continue
            elif choice.lower() == 's':
                # Run setup wizard manually
                self.run_setup_wizard()
                # Reload config after setup
                self.config = self.load_config()
                continue
            elif choice.lower() == 'h':
                # Show help
                self.show_help()
                continue
            else:
                self.print_yellow("Please select a valid option from the menu")
                time.sleep(1)
    
    def count_genx_files(self, root_directory: str) -> int:
        """Count total files matching the configured pattern"""
        count = 0
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff', '.tif'}
        pattern = self.config.get('image_search_pattern', 'genx').lower()
        exact_match = self.config.get('exact_match', False)

        try:
            for folder_path in Path(root_directory).iterdir():
                if folder_path.is_dir():
                    for file_path in folder_path.iterdir():
                        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                            filename_lower = file_path.name.lower()

                            # Check pattern match
                            matches = False
                            if exact_match:
                                import re
                                pattern_regex = r'(^|[^a-z0-9])' + re.escape(pattern) + r'([^a-z0-9]|$)'
                                if re.search(pattern_regex, filename_lower):
                                    matches = True
                            else:
                                if pattern in filename_lower:
                                    matches = True

                            if matches:
                                count += 1
        except Exception:
            pass
        return count
    
    def start_processing(self, input_folder: str):
        """Start the video generation process with Rich UI exactly like reference"""
        from rich.console import Console
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, MofNCompleteColumn, TimeElapsedColumn
        from rich.panel import Panel
        from rich.layout import Layout
        from rich.live import Live
        from rich.text import Text
        from rich.table import Table
        from rich.align import Align
        import threading
        
        console = Console(force_terminal=True, width=100)  # Reduced from 120 to 100
        self.clear_screen()
        
        # Rich header panel with emojis
        from rich.panel import Panel
        from rich.align import Align
        from rich.text import Text
        
        header_text = Text()
        header_text.append("🚀 RUNWAY BATCH VIDEO GENERATOR 🚀", style="bold cyan")
        
        header_panel = Panel(
            Align.center(header_text),
            style="bright_blue",
            padding=(0, 1)  # Reduced padding
        )
        
        console.print(header_panel)
        
        # Show loading message with Rich Live spinner
        from rich.spinner import Spinner
        from rich.live import Live
        from rich.console import Group
        
        # Create animated loading display with Rich Spinner
        def create_loading_spinner(message):
            return Spinner("dots", text=message, style="green bold")
        
        with Live(create_loading_spinner("Analyzing folders and checking for duplicates..."), 
                  console=console, refresh_per_second=10) as loading_live:
            
            # Start actual processing
            generator = RunwayActTwoBatchGenerator(
                self.config['api_key'],
                verbose=self.verbose_logging,
                driver_video_path=self.config.get('driver_video')
            )
            
            genx_count = self.count_genx_files(input_folder)
            folders = self.get_all_folders(input_folder)
            
            # Update loading message with new spinner
            loading_live.update(create_loading_spinner("Filtering out duplicates..."))
            
            # Get actual count of files to be processed (after duplicate filtering)
            pattern = self.config.get('image_search_pattern', 'genx')
            exact_match = self.config.get('exact_match', False)
            total_files = 0
            for folder in folders:
                genx_images = generator.get_genx_image_files(folder, search_pattern=pattern, exact_match=exact_match)
                total_files += len(genx_images)
        
        # FORCE clear screen completely - remove all duplicates and loading messages
        console.clear()
        os.system('cls' if os.name == 'nt' else 'clear')  # Force system clear
        time.sleep(0.1)
        
        # Show header ONLY ONCE after clearing
        console.print(header_panel)
        
        # Start timer here
        start_time = time.time()
        
        # Main processing - single clean display
        try:
            if not self.verbose_logging:
                # Configuration panel - show once only
                config_table = Table.grid(padding=0)
                config_table.add_column(style="cyan", justify="left", width=15)
                config_table.add_column(style="white", justify="left")
                
                config_table.add_row("Files Amt:", f"{total_files} GenX files")
                config_table.add_row("Driver video:", Path(self.config['driver_video']).name)
                config_table.add_row("Output folder:", "Downloads")
                config_table.add_row("Verbose mode:", "Hidden")
                
                config_panel = Panel(
                    config_table,
                    title="Configuration",
                    border_style="green",
                    title_align="left",
                    padding=(0, 1)  # Reduced padding
                )
                console.print(config_panel)
                
                # Progress bar with cyan spinner on the left
                with Progress(
                    SpinnerColumn(style="bright_cyan"),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(bar_width=None),
                    MofNCompleteColumn(), 
                    TextColumn("•"),
                    TimeElapsedColumn(),
                    console=console
                ) as progress:
                    
                    main_task = progress.add_task("📊 [cyan]0% complete[/cyan] • 🎬 Processing GenX files... 🚀", total=total_files)
                    
                    # Add colorful spinners below progress bar
                    status_text = "Loading..."
                    processed = 0
                    
                    def create_colorful_spinners():
                        from rich.text import Text
                        from rich.spinner import Spinner
                        from rich.console import Group
                        
                        # Activity spinner - bright green with emoji and status icons
                        activity_text = Text()
                        activity_text.append("🔥 Activity: ", style="bright_green bold")
                        
                        if "Generating:" in status_text:
                            filename = status_text.replace("Generating: ", "")
                            activity_text.append("⏳ Generating: ", style="bright_cyan")
                            activity_text.append(filename, style="white")
                        elif "Completed:" in status_text:
                            filename = status_text.replace("Completed: ", "")
                            activity_text.append("✅ Completed: ", style="bright_green")
                            activity_text.append(filename, style="white")
                        elif "Failed:" in status_text:
                            filename = status_text.replace("Failed: ", "")
                            activity_text.append("❌ Failed: ", style="bright_red")
                            activity_text.append(filename, style="white")
                        else:
                            activity_text.append(status_text, style="bright_cyan")
                        activity_spinner = Spinner("dots", text=activity_text, style="bright_green")
                        
                        # Action spinner - bright blue with emoji
                        action_text = Text()
                        action_text.append("⚡ Action: ", style="bright_blue bold")
                        action_text.append("Monitoring for interrupts...", style="bright_white")
                        action_spinner = Spinner("dots", text=action_text, style="bright_blue")
                        
                        # Next spinner - bright magenta with emoji (show only FUTURE files)
                        next_text = Text()
                        next_text.append("🔮 Next: ", style="bright_magenta bold")
                        
                        # Get all remaining files that come AFTER current one
                        all_remaining = []
                        current_found = False
                        for folder in folders:
                            genx_images = generator.get_genx_image_files(folder, search_pattern=pattern, exact_match=exact_match)
                            for img in genx_images:
                                img_name = Path(img).name
                                if current_found:
                                    all_remaining.append(Path(folder).name)
                                    break
                                elif "Generating:" in status_text and img_name in status_text:
                                    current_found = True
                        
                        if all_remaining:
                            display = all_remaining[:3]
                            folder_list = ", ".join(display)
                            if len(all_remaining) > 3:
                                folder_list += f" (+{len(all_remaining)-3} more)"
                            next_text.append(folder_list, style="bright_yellow")
                        else:
                            next_text.append("All processing complete", style="bright_green")
                        next_spinner = Spinner("dots", text=next_text, style="bright_magenta")
                        
                        return Group(activity_spinner, action_spinner, next_spinner)
                    
                    # Display colorful spinners below progress bar
                    from rich.live import Live
                    with Live(create_colorful_spinners(), console=console, refresh_per_second=10) as live:
                        def update_spinners(new_status):
                            nonlocal status_text
                            status_text = new_status
                            live.update(create_colorful_spinners())
                        
                        # Process files with BOTH progress bar AND spinner updates
                        for folder in folders:
                            folder_name = Path(folder).name
                            genx_images = generator.get_genx_image_files(folder, search_pattern=pattern, exact_match=exact_match)
                            
                            if not genx_images:
                                continue
                            
                            specific_output = Path(self.config['output_folder'])
                            
                            for image_path in genx_images:
                                image_name = Path(image_path).name
                                
                                # Update progress bar to show percentage during processing
                                status_text = f"Generating: {image_name}"
                                current_pct = int((processed / total_files) * 100) if total_files > 0 else 0
                                progress.update(main_task, description=f"📊 [cyan]{current_pct}% complete[/cyan] • ⏳")
                                update_spinners(status_text)
                                
                                try:
                                    result = generator.create_act_two_generation(
                                        character_image_path=image_path,
                                        output_folder=str(specific_output)
                                    )
                                except Exception as e:
                                    result = None
                                
                                processed += 1
                                completion_pct = int((processed / total_files) * 100) if total_files > 0 else 0
                                
                                # Update main progress bar with dynamic percentage
                                if result:
                                    progress.update(main_task, 
                                        completed=processed,
                                        description=f"📊 [cyan]{completion_pct}% complete[/cyan] • ✅")
                                    update_spinners(f"Completed: {image_name}")
                                else:
                                    progress.update(main_task, 
                                        completed=processed,
                                        description=f"📊 [cyan]{completion_pct}% complete[/cyan] • ❌")
                                    update_spinners(f"Failed: {image_name}")
                                
                                if self.config['delay_between_generations'] > 0:
                                    time.sleep(self.config['delay_between_generations'])
                        
                        # Final update
                        if total_files > 0:
                            progress.update(main_task, completed=total_files, 
                                description="📊 [cyan]100% complete[/cyan] • 🎉 All files processed!")
                            update_spinners("Processing complete!")
                        
                        time.sleep(2)
                        # Calculate elapsed time
                        elapsed = time.time() - start_time
                        elapsed_str = f"{int(elapsed//60)}:{int(elapsed%60):02d}"
                        
                        # Main progress with cyan colors
                        main_text = Text()
                        if processed > 0:
                            pct = int((processed / total_files) * 100) if total_files > 0 else 0
                            main_text.append(f"{pct}% complete • ", style="bright_cyan")
                            if "Generating:" in status_text:
                                filename = status_text.replace("Generating: ", "") 
                                main_text.append("Generating: ", style="bright_cyan bold")
                                main_text.append(filename, style="white")
                            else:
                                main_text.append("Processing GenX files...", style="bright_cyan")
                            
                            # Add colorful progress bar
                            bar_length = 25
                            filled = int((pct / 100) * bar_length)
                            bar = "█" * filled + "░" * (bar_length - filled)
                            main_text.append(f"  {bar}  {processed}/{total_files} • {elapsed_str}", style="bright_cyan")
                        else:
                            main_text.append("Processing GenX files... ", style="bright_cyan")
                            bar = "░" * 25
                            main_text.append(f"  {bar}  0/{total_files} • {elapsed_str}", style="bright_cyan")
                        main_spinner = Spinner("dots", text=main_text, style="bright_cyan")
                        
                        # Activity with bright green spinner
                        activity_text = Text()
                        activity_text.append("Activity: ", style="bright_green bold")
                        activity_text.append(status_text, style="bright_cyan")
                        activity_spinner = Spinner("dots", text=activity_text, style="bright_green")
                        
                        # Action with bright blue spinner
                        action_text = Text()
                        action_text.append("Action: ", style="bright_blue bold")
                        action_text.append("Monitoring for interrupts...", style="bright_white")
                        action_spinner = Spinner("dots", text=action_text, style="bright_blue")
                        
                        # Next with bright magenta spinner
                        next_text = Text()
                        next_text.append("Next: ", style="bright_magenta bold")
                        remaining = [Path(f).name for f in folders if generator.get_genx_image_files(f, search_pattern=pattern, exact_match=exact_match)]
                        if remaining and processed < total_files:
                            display = remaining[:3]
                            folder_list = ", ".join(display) 
                            if len(remaining) > 3:
                                folder_list += f" (+{len(remaining)-3} more)"
                            next_text.append(folder_list, style="bright_yellow")
                        else:
                            next_text.append("All processing complete", style="bright_green")
                        next_spinner = Spinner("dots", text=next_text, style="bright_magenta")
                        
                        return Group(main_spinner, activity_spinner, action_spinner, next_spinner)
                
                # Use Rich Live display with Rich Spinners
                with Live(create_status_display(), console=console, refresh_per_second=10) as live:
                    def update_status_live(new_text):
                        nonlocal status_text
                        status_text = new_text
                        live.update(create_status_display())
                    
                    # Process files with spinner updates only
                    for folder in folders:
                            folder_name = Path(folder).name
                            # Use generator's duplicate-filtered method instead of local method
                            genx_images = generator.get_genx_image_files(folder, search_pattern=pattern, exact_match=exact_match)
                            
                            if not genx_images:
                                continue
                            
                            # Determine output location based on configuration
                            if self.config.get("output_location", "centralized") == "co-located":
                                # Save to same folder as source image
                                specific_output = Path(image_path).parent if genx_images else Path(self.config['output_folder'])
                            else:
                                # Save to centralized output folder
                                specific_output = Path(self.config['output_folder'])

                            status_text = f"Processing folder: {folder_name}"
                            progress.update(main_task, description=f"📂 Processing: {folder_name}")
                            update_status_live(status_text)

                            for image_path in genx_images:
                                image_name = Path(image_path).name
                                status_text = f"Generating: {image_name}"
                                progress.update(main_task, description=f"🎬 [cyan]Generating:[/cyan] {image_name}")
                                update_status_live(status_text)

                                # Determine output folder for this specific image
                                if self.config.get("output_location", "centralized") == "co-located":
                                    output_for_this_image = str(Path(image_path).parent)
                                else:
                                    output_for_this_image = str(specific_output)

                                try:
                                    result = generator.create_act_two_generation(
                                        character_image_path=image_path,
                                        output_folder=output_for_this_image
                                    )
                                except Exception as e:
                                    result = None
                                    update_status_live(f"Error: {image_name}")
                                
                                processed += 1
                                completion_pct = int((processed / total_files) * 100) if total_files > 0 else 0
                                
                                if result:
                                    progress.update(main_task, 
                                        completed=processed,
                                        description=f"📊 [cyan]{completion_pct}% complete[/cyan] • ✅ {image_name}")
                                    update_status_live(f"Completed: {image_name}")
                                else:
                                    progress.update(main_task, 
                                        completed=processed,
                                        description=f"📊 [cyan]{completion_pct}% complete[/cyan] • ❌ {image_name}")
                                    update_status_live(f"Failed: {image_name}")
                                
                                if self.config['delay_between_generations'] > 0:
                                    time.sleep(self.config['delay_between_generations'])
                    
                    # Final update
                    if total_files > 0:
                        update_status_live("Processing complete!")
                    
                    time.sleep(2)
                        
            else:
                # Verbose processing - let all logs show
                print("Processing started with verbose logging...")
                print("All detailed logs will be displayed below:")
                print()

                # Pass output location preference to generator
                output_location = self.config.get("output_location", "centralized")

                generator.process_all_images(
                    target_directory=input_folder,
                    output_directory=self.config['output_folder'] if output_location == "centralized" else None,
                    delay_between_generations=self.config['delay_between_generations'],
                    co_located_output=(output_location == "co-located")
                )
                    
        except Exception as e:
            print(f"\nError during processing: {e}")
            if self.verbose_logging:
                import traceback
                print(f"{traceback.format_exc()}")
        
        print("\nProcessing complete!")
        if self.config.get("output_location", "centralized") == "co-located":
            print("✓ Videos saved in the same folders as their source images")
        else:
            print(f"✓ Check your videos in: {self.config['output_folder']}")
        input("\nPress Enter to return to main menu...")
    
    def get_all_folders(self, root_directory: str):
        """Get all folders that contain images matching the configured pattern"""
        folders = []
        try:
            for folder_path in Path(root_directory).iterdir():
                if folder_path.is_dir():
                    if self.get_genx_files_in_folder(str(folder_path)):
                        folders.append(str(folder_path))
        except Exception:
            pass
        return folders
    
    def get_genx_files_in_folder(self, folder_path: str):
        """Get files matching the configured pattern in a specific folder"""
        matching_files = []
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff', '.tif'}
        pattern = self.config.get('image_search_pattern', 'genx').lower()
        exact_match = self.config.get('exact_match', False)

        try:
            for file_path in Path(folder_path).iterdir():
                if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                    filename_lower = file_path.name.lower()

                    # Check pattern match
                    matches = False
                    if exact_match:
                        import re
                        pattern_regex = r'(^|[^a-z0-9])' + re.escape(pattern) + r'([^a-z0-9]|$)'
                        if re.search(pattern_regex, filename_lower):
                            matches = True
                    else:
                        if pattern in filename_lower:
                            matches = True

                    if matches:
                        matching_files.append(str(file_path))
        except Exception:
            pass
        return matching_files
    
    def run(self):
        """Main application loop"""
        while True:
            input_folder = self.run_configuration_menu()
            self.start_processing(input_folder)


def main():
    """Entry point"""
    try:
        # Enable ANSI colors on Windows
        os.system('color')

        # Get the current working directory (where exe/script is run from)
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_dir = Path(sys.executable).parent
        else:
            # Running as Python script
            base_dir = Path(__file__).parent.parent

        config_path = base_dir / "config" / "runway_config.json"
        needs_setup = False

        # Skip first run check if environment variable is set
        if os.environ.get('SKIP_FIRST_RUN') == '1':
            needs_setup = False
        elif not config_path.exists():
            needs_setup = True
        else:
            # Check if config has required fields
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # Only run setup if first_run is explicitly True or no API key
                    if config.get("first_run") is True or not config.get("api_key"):
                        needs_setup = True
            except:
                needs_setup = True

        # Run first-time setup if needed
        if needs_setup:
            from first_run_setup import FirstRunSetup
            wizard = FirstRunSetup()
            wizard.run()

        # Now run the main application
        app = RunwayAutomationUI()
        app.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
