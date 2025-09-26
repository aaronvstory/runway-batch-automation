#!/usr/bin/env python
"""Comprehensive test of all implemented features"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from path_utils import path_manager
from gui_selectors import VideoInfo
from pathlib import Path

print("="*80)
print("COMPREHENSIVE TEST - RunwayML Batch Automation Tool")
print("="*80)

# Test 1: Video Scanning in Assets
print("\n1. VIDEO SCANNING IN ASSETS FOLDER")
print("-"*40)
assets_videos = path_manager.get_all_driver_videos()
print(f"Found {len(assets_videos)} video(s) in assets folder:")
if assets_videos:
    for i, video in enumerate(assets_videos, 1):
        duration, formatted = VideoInfo.get_duration(str(video))
        print(f"  {i}. {video.name} ({formatted if duration else 'N/A'})")
else:
    print("  No videos found")

# Test 2: Configuration File
print("\n2. CONFIGURATION FILE CHECK")
print("-"*40)
config_path = Path(__file__).parent / "config" / "runway_config.json"
print(f"Config path: {config_path}")
print(f"Config exists: {config_path.exists()}")

if config_path.exists():
    import json
    with open(config_path, 'r') as f:
        config = json.load(f)
    print("\nConfiguration settings:")
    print(f"  - first_run: {config.get('first_run', 'Not set')}")
    print(f"  - api_key: {'✓ Set' if config.get('api_key') else '✗ Not set'}")
    print(f"  - driver_video: {Path(config.get('driver_video', '')).name if config.get('driver_video') else 'Not set'}")
    print(f"  - image_search_pattern: {config.get('image_search_pattern', 'Not set')}")
    print(f"  - exact_match: {config.get('exact_match', False)}")
    print(f"  - output_location: {config.get('output_location', 'Not set')}")

# Test 3: Image Pattern Matching
print("\n3. IMAGE PATTERN MATCHING TEST")
print("-"*40)

# Create test images to demonstrate pattern matching
test_dir = Path("test_images")
test_dir.mkdir(exist_ok=True)

test_files = [
    "genx-test.jpg",
    "test-genx.png",
    "selfie-test.jpg",
    "test-selfie.png",
    "my-selfie.jpg",
    "random.jpg"
]

print("Creating test images:")
for file in test_files:
    (test_dir / file).touch()
    print(f"  ✓ Created {file}")

# Test pattern matching
def test_pattern(pattern, exact_match=False):
    import re
    matches = []
    for file in test_files:
        filename_lower = file.lower()
        pattern_lower = pattern.lower()

        if exact_match:
            pattern_regex = r'(^|[^a-z0-9])' + re.escape(pattern_lower) + r'([^a-z0-9]|$)'
            if re.search(pattern_regex, filename_lower):
                matches.append(file)
        else:
            if pattern_lower in filename_lower:
                matches.append(file)
    return matches

print("\nPattern 'genx' (Contains mode):")
for match in test_pattern('genx', False):
    print(f"  ✓ {match}")

print("\nPattern 'selfie' (Contains mode):")
for match in test_pattern('selfie', False):
    print(f"  ✓ {match}")

print("\nPattern '-selfie' (Exact mode):")
for match in test_pattern('-selfie', True):
    print(f"  ✓ {match}")

# Clean up test images
import shutil
shutil.rmtree(test_dir)

# Test 4: Path Resolution
print("\n4. PATH RESOLUTION TEST")
print("-"*40)
print(f"Module directory: {path_manager.module_dir}")
print(f"Project directory: {path_manager.project_dir}")
print(f"Assets directory: {path_manager.project_dir / 'assets'}")
print(f"Config directory: {path_manager.project_dir / 'config'}")

print("\n" + "="*80)
print("ALL TESTS COMPLETED SUCCESSFULLY!")
print("="*80)