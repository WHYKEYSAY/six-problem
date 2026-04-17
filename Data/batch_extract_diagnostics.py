#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch EEG Event Extraction & Duration Analysis
Analyzes all subjects from April to September and saves text reports to the 'output' folder.
"""

import os
import subprocess
from pathlib import Path

# ============================================================
# SETTINGS
# ============================================================
DATA_DIR = Path(r"C:\Users\whyke\github\six-problem\Data")
OUTPUT_DIR = DATA_DIR / "output"
LOAD_DATA_SCRIPT = DATA_DIR / "load_data.py"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# SUBJECT FILE MAPPINGS
# ============================================================
SUBJECTS = {
    # APRIL (OneDrive_1_08-04-2026)
    "april_02(1)": DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_02(1)/april_2(1).vhdr",
    "april_02(3)": DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_02(3)/april_02(3).vhdr",
    "april_04(1)": DATA_DIR / "OneDrive_1_08-04-2026/EEG_april_04(1)/april_04(1).vhdr",
    "april_04(2)": DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_04(2)/apri_04(2).vhdr",
    "april_08":    DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_08/april_08.vhdr",
    "april_15":    DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_15/april_15.vhdr",
    "april_16(1)": DATA_DIR / "OneDrive_1_08-04-2026/EEG_april_16(1)/april_16(1).vhdr",
    "april_16(3)": DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_16(3)/april_16(3).vhdr",
    "april_18(1)": DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_18(1)/april_18(1).vhdr",
    "april_18(2)": DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_18(2)/april_18(2).vhdr",
    "april_19(1)": DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_19(1)/april_19(1).vhdr",
    "april_19(2)": DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_19(2)/april_19(2).vhdr",
    "april_22":    DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_22/april_22.vhdr",
    "april_24":    DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_24/april_24.vhdr",

    # JUNE/JULY (OneDrive_1_09-04-2026 & Root)
    "june_25":     DATA_DIR / "OneDrive_1_09-04-2026/june_25_eeg/june_25.vhdr",
    "july_29":     DATA_DIR / "eeg_july_29/eeg_july_29/july_29.vhdr",
    "july_30":     DATA_DIR / "OneDrive_1_09-04-2026/eeg_July_30/july_30.vhdr",

    # AUGUST (Root)
    "aug_05":      DATA_DIR / "eeg_aug_05/eeg_aug_05/aug_05.vhdr",

    # SEPTEMBER (OneDrive_1_01-04-2026)
    "sep_12(2)":   DATA_DIR / "OneDrive_1_01-04-2026/eeg_sep_12(2)/sep_12(2).vhdr",
    "sep_12":      DATA_DIR / "OneDrive_1_01-04-2026/eeg_sep_12/sep_12.vhdr",
    "sep_13(2)":   DATA_DIR / "OneDrive_1_01-04-2026/eeg_sep_13(2)/sep_13(2).vhdr",
    "sep_13":      DATA_DIR / "OneDrive_1_01-04-2026/eeg_sep_13/sep_13.vhdr",
    "sep_18":      DATA_DIR / "OneDrive_1_01-04-2026/eeg_sep_18/eeg_sep_18.vhdr",
}

import csv
import json

# CSV path
CSV_PATH = DATA_DIR / "EEG_Segmentation_correction.csv"

# Label columns in CSV (skipping first 3 metadata columns)
# Column headers: Name, total event, match or not, eye_closed, 1_problem, 1_solution, 1_rate, 1_eval, 1_type, 1_rate...
LABEL_NAMES = [
    "eye_closed_1", "1_problem", "1_solution", "1_rate_1", "1_eval", "1_type", "1_rate_2",
    "2_problem", "2_solution", "2_rate_1", "2_eval", "2_type", "2_rate_2",
    "3_problem", "3_solution", "3_rate_1", "3_eval", "3_type", "3_rate_2",
    "4_problem", "4_solution", "4_rate_1", "4_eval", "4_type", "4_rate_2",
    "5_problem", "5_solution", "5_rate_1", "5_eval", "5_type", "5_rate_2",
    "6_problem", "6_solution", "6_rate_1", "6_eval", "6_type", "6_rate_2",
    "eye_closed_2"
]

import re

def normalize_name(name):
    """Normalize subject names for robust matching (lowercase, no .xlsx, no leading zeros)"""
    if not name: return ""
    name = name.strip().lower().replace(".xlsx", "").replace(" ", "_")
    # Remove leading zeros from numbers (e.g. april_02 -> april_2)
    name = re.sub(r'([_\(])0(\d)', r'\1\2', name)
    # Also handle start of string
    name = re.sub(r'^0(\d)', r'\1', name)
    return name

def load_label_mappings():
    mappings = {}
    if not CSV_PATH.exists():
        print(f"Warning: CSV mapping file not found at {CSV_PATH}")
        return mappings

    try:
        with open(CSV_PATH, "r", encoding='latin-1') as f:
            content = f.read()
            reader = csv.reader(content.splitlines())
            headers = next(reader)
            for row in reader:
                if not row or len(row) < 4: continue
                
                # NORMALIZE NAME
                raw_name = normalize_name(row[0])
                
                # Markers start from column 3 (index 3)
                marker_vals = row[3:]
                subject_map = {}
                
                for i, val in enumerate(marker_vals):
                    if i >= len(LABEL_NAMES): break
                    val = val.strip()
                    if not val: continue
                    
                    numbers = [int(x) for x in re.findall(r'\d+', val)]
                    if numbers:
                        base_label = LABEL_NAMES[i] if i < len(LABEL_NAMES) else f"marker_{i}"
                        
                        # April 15 used the second number for 3_problem and 6_solution, all other files use the first number.
                        if "april_15" in raw_name and len(numbers) >= 2:
                            marker_num = numbers[-1]
                        else:
                            marker_num = numbers[0]
                            
                        if marker_num in subject_map:
                            subject_map[marker_num] += f" / {base_label}"
                        else:
                            subject_map[marker_num] = base_label

                
                mappings[raw_name] = subject_map
        print(f"Loaded label mappings for {len(mappings)} subjects from CSV.")
    except Exception as e:
        print(f"Error loading CSV: {e}")
    return mappings

# ============================================================
# EXECUTION
# ============================================================

LABEL_MAPPINGS = load_label_mappings()

def process_subject(name, path):
    print(f"\n[{name}]")
    if not path.exists():
        print(f"  [X] ERROR: File not found: {path}")
        return False
    
    output_file = OUTPUT_DIR / f"{name}_output_full.txt"
    print(f"  Running analysis for: {path.name}")
    
    # Get labels for this subject (Normalized!)
    norm_name = normalize_name(name)
    subject_label_map = LABEL_MAPPINGS.get(norm_name, {})
    
    if not subject_label_map:
        print(f"  [!] WARNING: No label mapping found in CSV for: {norm_name}")
    
    label_arg = json.dumps(subject_label_map)
    
    try:
        # Use subprocess.run with list to avoid shell escaping issues with JSON
        result = subprocess.run([
            "python", str(LOAD_DATA_SCRIPT),
            "--path", str(path),
            "--label-map", label_arg,
            "--no-plot"
        ], capture_output=True, text=True, encoding='utf-8')
        
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(f"OK Successfully processed: {path}\n\n")
            f.write(result.stdout)
            if result.stderr:
                f.write("\n[STDERR]\n")
                f.write(result.stderr)
        
        print(f"  [V] Done. Report saved to: output/{output_file.name}")
        return True
    except Exception as e:
        print(f"  [X] FAILED: {e}")
        return False

def main():
    print("=" * 60)
    print("BATCH EEG DIAGNOSTICS GENERATION")
    print(f"Processing {len(SUBJECTS)} subjects...")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for name, path in SUBJECTS.items():
        if process_subject(name, path):
            success += 1
        else:
            failed += 1
            
    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"  Total Subjects: {len(SUBJECTS)}")
    print(f"  Succeeded:      {success}")
    print(f"  Failed:         {failed}")
    print("=" * 60)
    print(f"All reports are available in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
