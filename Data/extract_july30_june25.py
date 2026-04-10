# -*- coding: utf-8 -*-
"""
Extract markers from July_30 and June_25 EEG files
Also verify against CSV data and run batch segmentation for both
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mne
import pandas as pd
import csv
from pathlib import Path

DATA_DIR = Path(r"C:\Users\whyke\github\six-problem\Data")

FILES = {
    "july_30": DATA_DIR / "OneDrive_1_09-04-2026" / "eeg_July_30" / "july_30.vhdr",
    "june_25": DATA_DIR / "OneDrive_1_09-04-2026" / "june_25_eeg" / "june_25.vhdr",
}

# CSV data already filled (from EEG_Segmentation(Sheet1).csv)
CSV_DATA = {
    "July_30.xlsx": {
        "total_event": 46,
        "markers": [3,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,38,39,40,41,42,43,45]
    },
    "June_25.xlsx": {
        "total_event": 45,
        "markers": [3,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,None,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,42,44]
    },
}

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


def preprocess_raw(raw):
    raw.filter(l_freq=0.5, h_freq=40.0, method='fir', verbose=False)
    raw.set_eeg_reference('average', projection=False, verbose=False)
    return raw


def extract_and_verify(name, vhdr_path):
    print(f"\n{'='*70}")
    print(f"FILE: {name}")
    print(f"{'='*70}")

    raw = mne.io.read_raw_brainvision(str(vhdr_path), preload=False, verbose='ERROR')
    annotations = raw.annotations
    events, event_id = mne.events_from_annotations(raw, verbose=False)

    print(f"  Sampling rate : {raw.info['sfreq']} Hz")
    print(f"  Duration      : {raw.times[-1]:.2f} sec ({raw.times[-1]/60:.1f} min)")
    print(f"  Channels      : {len(raw.ch_names)}")
    print(f"  Total events  : {len(events)}")
    print(f"  Event types   : {event_id}")

    ann_counts = {}
    for d in annotations.description:
        ann_counts[d] = ann_counts.get(d, 0) + 1
    print(f"  Annotation counts: {ann_counts}")

    # Build event DataFrame
    df = pd.DataFrame({'sample': events[:, 0], 'code': events[:, 2]})
    df['time_sec'] = df['sample'] / raw.info['sfreq']
    inv = {v: k for k, v in event_id.items()}
    df['label'] = df['code'].map(inv)

    print(f"\n  ALL EVENTS (time, label):")
    for idx, row in df.iterrows():
        print(f"    [{idx+1:2d}] {row['time_sec']:8.2f}s  {row['label']}")

    # Output txt file
    csv_name = "July_30.xlsx" if "july" in name else "June_25.xlsx"
    out_txt = DATA_DIR / f"{name}_output.txt"
    with open(out_txt, 'w', encoding='utf-8') as f:
        f.write(f"File: {vhdr_path}\n")
        f.write(f"Total events: {len(events)}\n")
        f.write(f"Event types: {event_id}\n\n")
        f.write("===== ALL EVENTS =====\n")
        f.write(df[['time_sec', 'label']].to_string())
        f.write("\n")
    print(f"\n  Saved: {out_txt.name}")

    # Verify vs CSV
    csv_info = CSV_DATA.get(csv_name, {})
    csv_total = csv_info.get('total_event', '?')
    match = "MATCH" if str(len(events)) == str(csv_total) else f"MISMATCH (EEG={len(events)}, CSV={csv_total})"
    print(f"\n  CSV total_event={csv_total}  EEG events={len(events)}  → {match}")

    return raw, events, event_id


def run_segmentation(name, raw, events, event_id, csv_name):
    print(f"\n--- Segmenting: {csv_name} ---")

    csv_info = CSV_DATA.get(csv_name, {})
    markers = csv_info.get('markers', [])

    if len(markers) != 38:
        print(f"  ERROR: Expected 38 marker values, got {len(markers)}")
        return

    # Preprocess
    raw.load_data()
    raw = preprocess_raw(raw)

    # Event times
    event_times = events[:, 0] / raw.info['sfreq']
    print(f"  Events available: {len(event_times)}")

    # Output folder
    folder_name = csv_name.replace('.xlsx', '').replace('(', '_').replace(')', '').replace(' ', '_')
    out_dir = DATA_DIR / "segments_output" / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)

    ok_count = 0
    skip_count = 0

    for i, label in enumerate(SEG_LABELS):
        m_start = markers[i]

        # Find next non-None marker
        m_end = None
        for j in range(i + 1, len(markers)):
            if markers[j] is not None:
                m_end = markers[j]
                break

        if m_start is None:
            print(f"  SKIP {label:<20} (missing marker in CSV)")
            skip_count += 1
            continue

        idx_start = m_start - 1  # 1-based → 0-based
        if idx_start >= len(event_times):
            print(f"  ERROR {label:<20} marker {m_start} out of range")
            continue

        t_start = event_times[idx_start]

        if m_end is not None and (m_end - 1) < len(event_times):
            t_end = event_times[m_end - 1]
        else:
            t_end = raw.times[-1]

        if t_end <= t_start:
            print(f"  ERROR {label:<20} t_end <= t_start ({t_start:.1f} → {t_end:.1f})")
            continue

        try:
            seg = raw.copy().crop(tmin=t_start, tmax=t_end)
            out_file = out_dir / f"{label}.fif"
            seg.save(str(out_file), overwrite=True, verbose=False)
            dur = t_end - t_start
            print(f"  OK    {label:<20} {dur:6.1f}s  → {out_file.name}")
            ok_count += 1
        except Exception as e:
            print(f"  ERROR {label:<20} {e}")

    print(f"\n  Results: {ok_count} segments saved, {skip_count} skipped")
    print(f"  Output: {out_dir}")


def main():
    print("=" * 70)
    print("EXTRACTING + SEGMENTING: July_30 and June_25")
    print("=" * 70)

    results = {}
    for name, vhdr_path in FILES.items():
        if not vhdr_path.exists():
            print(f"\nSKIP {name}: file not found at {vhdr_path}")
            continue

        raw, events, event_id = extract_and_verify(name, vhdr_path)
        csv_name = "July_30.xlsx" if "july" in name else "June_25.xlsx"
        run_segmentation(name, raw, events, event_id, csv_name)
        results[name] = len(events)

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
    for name, count in results.items():
        print(f"  {name}: {count} events")


if __name__ == "__main__":
    main()
