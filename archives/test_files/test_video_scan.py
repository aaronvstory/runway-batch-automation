#!/usr/bin/env python
"""Test video scanning functionality"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from path_utils import path_manager
from gui_selectors import VideoInfo

print("="*60)
print("Testing Video Scanning in Assets Folder")
print("="*60)

# Test get_all_driver_videos
assets_videos = path_manager.get_all_driver_videos()
print(f"\nFound {len(assets_videos)} video(s) in assets folder:\n")

if assets_videos:
    for i, video in enumerate(assets_videos, 1):
        duration, formatted = VideoInfo.get_duration(str(video))
        duration_str = f" ({formatted})" if duration else ""
        print(f"  {i}. {video.name}{duration_str}")
        print(f"     Full path: {video}")
else:
    print("  No videos found in assets folder")

# Test project directory
print(f"\nProject directory: {path_manager.project_dir}")
print(f"Assets directory: {path_manager.project_dir / 'assets'}")
print(f"Assets exists: {(path_manager.project_dir / 'assets').exists()}")

# Test get_default_driver_video
default = path_manager.get_default_driver_video()
if default:
    print(f"\nDefault video: {default.name}")