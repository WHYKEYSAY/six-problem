#!/usr/bin/env python3
"""
Batch EEG Analysis Script
Processes multiple EEG files and extracts marker information for six-problem study
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Handle encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import mne
    import numpy as np
except ImportError:
    print("[ERROR] Required packages not installed: mne, numpy")
    sys.exit(1)

print("=" * 80)
print("BATCH EEG MARKER EXTRACTION")
print("=" * 80)
print(f"Timestamp: {datetime.now()}\n")

# Configuration
EEG_SEARCH_PATHS = [
    Path(r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026"),
    Path.cwd(),
    Path(r"C:\Users\whyke\OneDrive\Documents\EEG\0_raw_data"),
    Path(r"C:\Users\whyke\Documents\EEGToolbox_Data\0_raw_data"),
]

EEG_EXTENSIONS = ['.vhdr', '.edf', '.set', '.fif']
EXPECTED_MARKERS = [
    'eye_closed',
    '1_problem', '1_solution', '1_rate', '1_eval', '1_type',
    '2_problem', '2_solution', '2_rate', '2_eval', '2_type',
    '3_problem', '3_solution', '3_rate', '3_eval', '3_type',
    '4_problem', '4_solution', '4_rate', '4_eval', '4_type',
    '5_problem', '5_solution', '5_rate', '5_eval', '5_type',
    '6_problem', '6_solution', '6_rate', '6_eval', '6_type',
    'eye_closed_2'
]

# Step 1: Find EEG files
print("[STEP 1] Searching for EEG files...")
print("-" * 80)

eeg_files = []
for search_path in EEG_SEARCH_PATHS:
    if search_path.exists():
        print(f"Searching: {search_path}")
        for ext in EEG_EXTENSIONS:
            found = list(search_path.glob(f'**/*{ext}'))
            eeg_files.extend(found)
            if found:
                print(f"  Found {len(found)} {ext} files")
    else:
        print(f"Path not found: {search_path}")

if not eeg_files:
    print("\n[WARN] No EEG files found!")
    print("Expected location: D:\\Six problem\\six-problem\\six-problem\\EEG_six_problem")
    print("Please ensure EEG data is accessible before proceeding.")
    sys.exit(0)

print(f"\nTotal EEG files found: {len(eeg_files)}")
for f in eeg_files[:10]:
    print(f"  - {f.name}")
if len(eeg_files) > 10:
    print(f"  ... and {len(eeg_files) - 10} more")

# Step 2: Process each EEG file
print("\n[STEP 2] Processing EEG files...")
print("-" * 80)

results = []
errors = []

for idx, eeg_file in enumerate(eeg_files, 1):
    print(f"\n[{idx}/{len(eeg_files)}] Processing: {eeg_file.name}")

    try:
        # Read raw EEG
        if eeg_file.suffix == '.vhdr':
            raw = mne.io.read_raw_brainvision(str(eeg_file), preload=False, verbose='ERROR')
        elif eeg_file.suffix == '.edf':
            raw = mne.io.read_raw_edf(str(eeg_file), preload=False, verbose='ERROR')
        elif eeg_file.suffix == '.set':
            raw = mne.io.read_raw_eeglab(str(eeg_file), preload=False, verbose='ERROR')
        elif eeg_file.suffix == '.fif':
            raw = mne.io.read_raw_fif(str(eeg_file), preload=False, verbose='ERROR')
        else:
            raise ValueError(f"Unsupported format: {eeg_file.suffix}")

        # Extract annotations
        if len(raw.annotations) == 0:
            print("  [WARN] No annotations found!")
            errors.append((eeg_file.name, "No annotations"))
            continue

        # Convert to events
        events, event_id = mne.events_from_annotations(raw)

        print(f"  Info: {len(raw.ch_names)} channels, {raw.info['sfreq']} Hz, {len(raw.annotations)} annotations")

        # Count event types
        event_counts = {}
        for event_code, event_name in event_id.items():
            count = sum(1 for e in events if e[2] == event_code)
            event_counts[event_name] = count

        # Create result entry
        result = {
            'File': eeg_file.name,
            'Path': str(eeg_file),
            'Total_Events': len(events),
            'Total_Annotations': len(raw.annotations),
            'Duration_sec': raw.times[-1],
            'Channels': len(raw.ch_names),
            'Sfreq_Hz': raw.info['sfreq']
        }

        # Add event counts
        for marker in EXPECTED_MARKERS:
            # Try exact match and case-insensitive variants
            count = 0
            for event_name, c in event_counts.items():
                # Convert to string in case it's an integer
                event_name_str = str(event_name).lower()
                if event_name_str == marker.lower():
                    count = c
                    break
            result[marker] = count

        # Check if markers match documentation
        extracted_markers = set(str(k).lower() for k in event_counts.keys())
        expected_markers_lower = set(m.lower() for m in EXPECTED_MARKERS)

        mismatches = extracted_markers - expected_markers_lower
        missing = expected_markers_lower - extracted_markers

        result['Match_Status'] = 'OK' if len(mismatches) == 0 and len(missing) == 0 else 'MISMATCH'
        result['Unexpected_Markers'] = ','.join(sorted(mismatches)) if mismatches else 'None'
        result['Missing_Markers'] = ','.join(sorted(missing)) if missing else 'None'

        results.append(result)
        print(f"  [OK] Extracted {len(event_counts)} event types, {len(events)} total events")

    except Exception as e:
        print(f"  [ERROR] {str(e)}")
        errors.append((eeg_file.name, str(e)))

# Step 3: Save results
print("\n[STEP 3] Saving results...")
print("-" * 80)

if results:
    # Create DataFrame
    df = pd.DataFrame(results)

    # Save to CSV
    csv_file = 'eeg_extracted_events.csv'
    df.to_csv(csv_file, index=False)
    print(f"[OK] Saved to: {csv_file}")

    # Display summary
    print(f"\nProcessed {len(results)} files successfully")
    print("\nSummary of extracted events:")
    print(df[['File', 'Total_Events', 'Match_Status']].to_string())

    # Check for mismatches
    mismatches = df[df['Match_Status'] != 'OK']
    if len(mismatches) > 0:
        print(f"\n[WARN] {len(mismatches)} files have marker mismatches:")
        for _, row in mismatches.iterrows():
            print(f"  {row['File']}:")
            if row['Unexpected_Markers'] != 'None':
                print(f"    Unexpected: {row['Unexpected_Markers']}")
            if row['Missing_Markers'] != 'None':
                print(f"    Missing: {row['Missing_Markers']}")

if errors:
    print(f"\n[WARN] {len(errors)} files had errors:")
    for filename, error in errors:
        print(f"  {filename}: {error}")

# Step 4: Summary statistics
print("\n[STEP 4] Summary Statistics")
print("-" * 80)

if results:
    df = pd.DataFrame(results)

    # Event count statistics
    print("\nEvent Counts (across all files):")
    for marker in EXPECTED_MARKERS:
        if marker in df.columns:
            total = df[marker].sum()
            avg = df[marker].mean()
            max_val = df[marker].max()
            print(f"  {marker:20} - Total: {int(total):4}, Avg: {avg:6.2f}, Max: {int(max_val):4}")

    # File statistics
    print(f"\nFile Statistics:")
    print(f"  Total files: {len(df)}")
    print(f"  Avg duration: {df['Duration_sec'].mean():.2f} sec")
    print(f"  Avg events per file: {df['Total_Events'].mean():.1f}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print("\nNext steps:")
print("1. Review eeg_extracted_events.csv for event details")
print("2. Run fill_excel_from_eeg.py to update EEG_Segmentation.xlsx")
print("3. Check for any marker mismatches or unexpected events")
print("=" * 80)
