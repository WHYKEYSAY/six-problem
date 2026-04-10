#!/usr/bin/env python3
"""
Analyze marker codes and create mapping
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mne
from pathlib import Path
import pandas as pd

print("=" * 80)
print("MARKER CODE ANALYSIS")
print("=" * 80)

# 打开一个September文件看详细信息
sep_file = Path(r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026\eeg_sep_12\sep_12.vhdr")

print(f"\nAnalyzing: {sep_file.name}")
print("-" * 80)

# 加载文件
raw = mne.io.read_raw_brainvision(str(sep_file), preload=False, verbose='ERROR')

print(f"File info:")
print(f"  Channels: {len(raw.ch_names)}")
print(f"  Sampling rate: {raw.info['sfreq']} Hz")
print(f"  Duration: {raw.times[-1]:.2f} seconds")
print(f"  Total annotations: {len(raw.annotations)}")

# 详细的注释信息
print(f"\nDetailed annotations:")
print(f"  Unique descriptions: {set(raw.annotations.description)}")

# 列出所有注释
print(f"\nAll annotations (first 20):")
annotations_list = list(zip(
    raw.annotations.onset,
    raw.annotations.duration,
    raw.annotations.description
))
for i, (onset, duration, description) in enumerate(annotations_list[:20]):
    time_sec = onset / raw.info['sfreq']
    print(f"  [{i+1:2}] {description:15} at {time_sec:8.2f}s")

# 统计
print(f"\nMarker distribution:")
from collections import Counter
marker_counts = Counter(raw.annotations.description)
for marker, count in sorted(marker_counts.items()):
    print(f"  {str(marker):20} : {count:3}个")

print(f"\nPattern analysis:")
print(f"  Total: {len(raw.annotations)} markers")
print(f"  Types: {len(marker_counts)} unique markers")

if len(marker_counts) == 2:
    print(f"\n  ⚠ Only 2 unique marker types found!")
    print(f"     This suggests binary choice experiment")
    print(f"     Not the 6-problem paradigm (which needs 38+ markers)")

print("\n" + "=" * 80)
print("QUESTIONS FOR USER:")
print("=" * 80)
print("""
1. What does "S 14" represent? (e.g., stimulus, problem, response, etc.)
2. What does "S 15" represent?
3. Is this the 6-problem experiment?
4. Are there marker definitions in the PDF?
5. Should we count both S14 and S15 together as one "event type"?
""")
print("=" * 80)
