# -*- coding: utf-8 -*-
"""
Re-run segmentation for April_2(1) only, using updated CSV (P1_prob: 6→5)
Also updates batch_preprocess_segment.py to use EEG_Segmentation(Sheet1).csv
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import csv
import mne
from pathlib import Path

DATA_DIR   = Path(r"C:\Users\whyke\github\six-problem\Data")
CSV_PATH   = DATA_DIR / "EEG_Segmentation(Sheet1).csv"
OUTPUT_DIR = DATA_DIR / "segments_output"

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

TARGET = "April_2(1).xlsx"
VHDR   = DATA_DIR / "OneDrive_1_08-04-2026" / "eeg_april_02(1)" / "april_2(1).vhdr"


def read_markers_from_csv(target_name):
    with open(CSV_PATH, encoding='latin-1') as f:
        reader = csv.reader(f)
        next(reader)  # header
        for row in reader:
            if row[0].strip() == target_name:
                total = int(row[1].strip())
                raw_vals = [v.strip() for v in row[3:41]]
                markers = []
                for v in raw_vals:
                    if v == '' or v.upper() == 'NA':
                        markers.append(None)
                    elif v.isdigit():
                        markers.append(int(v))
                    else:
                        markers.append(None)
                return total, markers
    return None, None


def run():
    print("=" * 70)
    print(f"Re-segmenting: {TARGET}")
    print("=" * 70)

    total, markers = read_markers_from_csv(TARGET)
    if markers is None:
        print(f"ERROR: {TARGET} not found in CSV")
        return

    print(f"  CSV total_event = {total}")
    print(f"  P1_prob marker  = {markers[1]}  (was 6, now {markers[1]})")
    print(f"  Full marker sequence: {markers}")

    if not VHDR.exists():
        print(f"  ERROR: file not found: {VHDR}")
        return

    # Load and preprocess
    print(f"\n  Loading EEG...")
    raw = mne.io.read_raw_brainvision(str(VHDR), preload=True, verbose='ERROR')
    raw.filter(l_freq=0.5, h_freq=40.0, method='fir', verbose=False)
    raw.set_eeg_reference('average', projection=False, verbose=False)

    events, event_id = mne.events_from_annotations(raw, verbose=False)
    event_times = events[:, 0] / raw.info['sfreq']
    print(f"  EEG events: {len(event_times)}  (CSV says: {total})")
    if len(event_times) != total:
        print(f"  WARNING: count mismatch!")

    out_dir = OUTPUT_DIR / "April_2_1"
    out_dir.mkdir(parents=True, exist_ok=True)

    ok = skip = err = 0
    for i, label in enumerate(SEG_LABELS):
        m_start = markers[i]
        m_end = None
        for j in range(i + 1, len(markers)):
            if markers[j] is not None:
                m_end = markers[j]
                break

        if m_start is None:
            print(f"  SKIP  {label:<22} (NA in CSV)")
            skip += 1
            continue

        idx_s = m_start - 1
        if idx_s >= len(event_times):
            print(f"  ERROR {label:<22} marker {m_start} out of range")
            err += 1
            continue

        t_start = event_times[idx_s]
        if m_end is not None and (m_end - 1) < len(event_times):
            t_end = event_times[m_end - 1]
        else:
            t_end = raw.times[-1]

        if t_end <= t_start:
            print(f"  ERROR {label:<22} t_end({t_end:.1f}) <= t_start({t_start:.1f})")
            err += 1
            continue

        try:
            seg = raw.copy().crop(tmin=t_start, tmax=t_end)
            out_file = out_dir / f"{label}.fif"
            seg.save(str(out_file), overwrite=True, verbose=False)
            print(f"  OK    {label:<22} {t_end - t_start:6.1f}s  [{m_start}→{m_end}]")
            ok += 1
        except Exception as e:
            print(f"  ERROR {label:<22} {e}")
            err += 1

    print(f"\n  Result: {ok} saved, {skip} skipped, {err} errors")
    print(f"  Output: {out_dir}")

    # Final count
    fif_files = list(out_dir.glob("*.fif"))
    print(f"  Total .fif in folder: {len(fif_files)}/38")


if __name__ == "__main__":
    run()
