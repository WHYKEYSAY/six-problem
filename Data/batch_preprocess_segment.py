# -*- coding: utf-8 -*-
"""
Batch EEG Preprocessing & Segmentation
Based on EEG_Segmentation_correction.csv

Pipeline per subject:
  1. Load raw BrainVision EEG
  2. Bandpass filter 0.5–40 Hz
  3. Average re-reference
  4. Extract event timestamps (marker numbers = 1-based event index)
  5. Segment into 8 types per problem × 6 problems + 2 eye-closed
  6. Save each segment as .fif to per-subject output folder

Segment types:
  eye_closed_1, P1-P6 (prob, sol, rate1, eval, type, rate2), eye_closed_2
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import csv
import mne
import numpy as np
from pathlib import Path

# ============================================================
# PATHS
# ============================================================
DATA_DIR   = Path(r"C:\Users\whyke\github\six-problem\Data")
OUTPUT_DIR = DATA_DIR / "segments_output"
LOCS_PATH  = DATA_DIR / "Cap63 (1).locs"
CSV_PATH   = DATA_DIR / "EEG_Segmentation_correction.csv"

# ============================================================
# EEG FILE PATH MAP  (csv_name → vhdr path)
# ============================================================
FILE_MAP = {
    # April
    "April_2(1).xlsx":   DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_02(1)/april_2(1).vhdr",
    "april_02(3).xlsx":  DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_02(3)/april_02(3).vhdr",
    "april_04(1).xlsx":  DATA_DIR / "OneDrive_1_08-04-2026/EEG_april_04(1)/april_04(1).vhdr",
    "April_04(2).xlsx":  DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_04(2)/apri_04(2).vhdr",
    "april_08.xlsx":     DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_08/april_08.vhdr",
    "April_15.xlsx":     DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_15/april_15.vhdr",
    "April_16(1).xlsx":  DATA_DIR / "OneDrive_1_08-04-2026/EEG_april_16(1)/april_16(1).vhdr",
    "april_16(3).xlsx":  DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_16(3)/april_16(3).vhdr",
    "april_18(1).xlsx":  DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_18(1)/april_18(1).vhdr",
    "april_18(2).xlsx":  DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_18(2)/april_18(2).vhdr",
    "april_19(1).xlsx":  DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_19(1)/april_19(1).vhdr",
    "April_19(2).xlsx":  DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_19(2)/april_19(2).vhdr",
    "april_22.xlsx":     DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_22/april_22.vhdr",
    "april_24.xlsx":     DATA_DIR / "OneDrive_1_08-04-2026/eeg_april_24/april_24.vhdr",
    # August
    "aug_05.xlsx":       DATA_DIR / "eeg_aug_05/eeg_aug_05/aug_05.vhdr",
    # July
    "July_29.xlsx":      DATA_DIR / "eeg_july_29/eeg_july_29/july_29.vhdr",
    # September
    "Sep_12(2).xlsx":    DATA_DIR / "OneDrive_1_01-04-2026/eeg_sep_12(2)/sep_12(2).vhdr",
    "Sep_12.xlsx":       DATA_DIR / "OneDrive_1_01-04-2026/eeg_sep_12/sep_12.vhdr",
    "Sep_13(2).xlsx":    DATA_DIR / "OneDrive_1_01-04-2026/eeg_sep_13(2)/sep_13(2).vhdr",
    "Sep_13.xlsx":       DATA_DIR / "OneDrive_1_01-04-2026/eeg_sep_13/sep_13.vhdr",
    "Sep_18.xlsx":       DATA_DIR / "OneDrive_1_01-04-2026/eeg_sep_18/eeg_sep_18.vhdr",
    # Not available locally (no file found):
    # "July_30.xlsx", "June_25.xlsx"
}

# ============================================================
# CSV COLUMN STRUCTURE (38 marker columns after col C)
# ============================================================
SEG_LABELS = [
    "eye_closed_1",
    "P1_prob", "P1_sol", "P1_rate1", "P1_eval", "P1_type", "P1_rate2",
    "P2_prob", "P2_sol", "P2_rate1", "P2_eval", "P2_type", "P2_rate2",
    "P3_prob", "P3_sol", "P3_rate1", "P3_eval", "P3_type", "P3_rate2",
    "P4_prob", "P4_sol", "P4_rate1", "P4_eval", "P4_type", "P4_rate2",
    "P5_prob", "P5_sol", "P5_rate1", "P5_eval", "P5_type", "P5_rate2",
    "P6_prob", "P6_sol", "P6_rate1", "P6_eval", "P6_type", "P6_rate2",
    "eye_closed_2",
]

# ============================================================
# READ CSV
# ============================================================
def read_correction_csv():
    subjects = {}
    with open(CSV_PATH, encoding='latin-1') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if not row[0].strip() or not row[1].strip():
                continue
            name = row[0].strip()
            total = row[1].strip()
            marker_vals = [v.strip() for v in row[3:41]]  # 38 columns

            if not total.isdigit():
                continue

            markers = []
            for v in marker_vals:
                if v == '' or v.upper() == 'NA':
                    markers.append(None)
                elif v.isdigit():
                    markers.append(int(v))
                else:
                    markers.append(None)

            subjects[name] = {
                'total_event': int(total),
                'markers': markers,  # list of 38 values (1-based event index or None)
            }
    return subjects

# ============================================================
# PREPROCESSING
# ============================================================
def preprocess_raw(raw):
    """Basic preprocessing: filter + average reference"""
    # Bandpass 0.5–40 Hz
    raw.filter(l_freq=0.5, h_freq=40.0, method='fir', verbose=False)
    # Average reference
    raw.set_eeg_reference('average', projection=False, verbose=False)
    return raw

# ============================================================
# SEGMENT EXTRACTION
# ============================================================
def extract_segments(raw, event_times_sec, markers, seg_labels, subject_name):
    """
    Extract raw segments based on marker indices.
    markers[i] = 1-based index of event in EEG (None = missing/skip)
    Segment i spans from event[markers[i]-1] to event[markers[i+1]-1]
    """
    sfreq = raw.info['sfreq']
    results = []

    for i, label in enumerate(seg_labels):
        m_start = markers[i]
        # Find next non-None marker for end time
        m_end = None
        for j in range(i + 1, len(markers)):
            if markers[j] is not None:
                m_end = markers[j]
                break

        if m_start is None:
            results.append({'label': label, 'status': 'SKIP (missing marker)', 'segment': None})
            continue

        # Convert 1-based marker index to event_times index (0-based)
        idx_start = m_start - 1
        if idx_start >= len(event_times_sec):
            results.append({'label': label, 'status': f'ERROR (marker {m_start} out of range)', 'segment': None})
            continue

        t_start = event_times_sec[idx_start]

        if m_end is not None:
            idx_end = m_end - 1
            if idx_end < len(event_times_sec):
                t_end = event_times_sec[idx_end]
            else:
                t_end = raw.times[-1]
        else:
            # eye_closed_2: use end of recording
            t_end = raw.times[-1]

        if t_end <= t_start:
            results.append({'label': label, 'status': f'ERROR (t_end <= t_start)', 'segment': None})
            continue

        # Crop raw
        try:
            seg = raw.copy().crop(tmin=t_start, tmax=t_end)
            duration = t_end - t_start
            results.append({
                'label': label,
                'status': f'OK ({duration:.1f}s)',
                'segment': seg,
                't_start': t_start,
                't_end': t_end,
            })
        except Exception as e:
            results.append({'label': label, 'status': f'ERROR: {e}', 'segment': None})

    return results

# ============================================================
# MAIN BATCH LOOP
# ============================================================
def run_batch(dry_run=False):
    print("=" * 80)
    print("BATCH EEG PREPROCESSING & SEGMENTATION")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Mode: {'DRY RUN (no save)' if dry_run else 'FULL RUN (saving .fif)'}")
    print("=" * 80)

    subjects = read_correction_csv()

    summary = []

    for csv_name, data in subjects.items():
        if csv_name not in FILE_MAP:
            print(f"\n[SKIP] {csv_name} — no EEG file mapped (July_30/June_25 not available locally)")
            summary.append({'name': csv_name, 'status': 'SKIP: no local file', 'segments': 0})
            continue

        vhdr_path = FILE_MAP[csv_name]
        if not vhdr_path.exists():
            print(f"\n[SKIP] {csv_name} — file not found: {vhdr_path}")
            summary.append({'name': csv_name, 'status': 'SKIP: file missing', 'segments': 0})
            continue

        print(f"\n{'='*80}")
        print(f"Processing: {csv_name}  (total_event={data['total_event']})")
        print(f"{'='*80}")

        try:
            # Load raw
            raw = mne.io.read_raw_brainvision(str(vhdr_path), preload=True, verbose='ERROR')
            print(f"  Loaded: {raw.info['sfreq']} Hz, {len(raw.ch_names)} ch, {raw.times[-1]:.1f}s")

            # Preprocess
            raw = preprocess_raw(raw)
            print(f"  Preprocessed: 0.5–40 Hz filter + avg reference")

            # Get event timestamps
            events, event_id = mne.events_from_annotations(raw, verbose=False)
            event_times = events[:, 0] / raw.info['sfreq']  # in seconds
            print(f"  Events found: {len(event_times)}")

            if len(event_times) != data['total_event']:
                print(f"  WARNING: CSV total_event={data['total_event']} but EEG has {len(event_times)} events")

            # Create output folder
            folder_name = csv_name.replace('.xlsx', '').replace('(', '_').replace(')', '').replace(' ', '_')
            out_dir = OUTPUT_DIR / folder_name
            if not dry_run:
                out_dir.mkdir(parents=True, exist_ok=True)

            # Extract segments
            segs = extract_segments(raw, event_times, data['markers'], SEG_LABELS, csv_name)

            ok_count = 0
            for seg_info in segs:
                label = seg_info['label']
                status = seg_info['status']
                seg = seg_info['segment']

                if seg is not None:
                    out_file = out_dir / f"{label}.fif"
                    if not dry_run:
                        seg.save(str(out_file), overwrite=True, verbose=False)
                    ok_count += 1
                    print(f"  ✓ {label:<20} {status}{'  → '+str(out_file.name) if not dry_run else ''}")
                else:
                    print(f"  ⬜ {label:<20} {status}")

            summary.append({'name': csv_name, 'status': f'OK ({ok_count}/{len(segs)} segments)', 'segments': ok_count})

        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback; traceback.print_exc()
            summary.append({'name': csv_name, 'status': f'ERROR: {e}', 'segments': 0})

    # Final summary
    print("\n" + "=" * 80)
    print("BATCH SUMMARY")
    print("=" * 80)
    print(f"{'File':<25} {'Segments':>9}  Status")
    print("-" * 80)
    for s in summary:
        print(f"  {s['name']:<23} {s['segments']:>9}  {s['status']}")

    total_segs = sum(s['segments'] for s in summary)
    ok_files = sum(1 for s in summary if 'OK' in s['status'])
    print(f"\nTotal: {ok_files} files processed, {total_segs} segments saved")
    if not dry_run:
        print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    import sys
    dry = "--dry" in sys.argv
    run_batch(dry_run=dry)
