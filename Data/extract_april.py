# -*- coding: utf-8 -*-
"""
Extract all April EEG data files
Based on load_data.py reference
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mne
import pandas as pd
from pathlib import Path

APRIL_FILES = {
    "april_02(1)":  r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_02(1)\april_2(1).vhdr",
    "april_02(3)":  r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_02(3)\april_02(3).vhdr",
    "april_04(1)":  r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\EEG_april_04(1)\april_04(1).vhdr",
    "april_04(2)":  r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_04(2)\apri_04(2).vhdr",
    "april_08":     r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_08\april_08.vhdr",
    "april_15":     r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_15\april_15.vhdr",
    "april_16(1)":  r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\EEG_april_16(1)\april_16(1).vhdr",
    "april_16(3)":  r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_16(3)\april_16(3).vhdr",
    "april_18(1)":  r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_18(1)\april_18(1).vhdr",
    "april_18(2)":  r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_18(2)\april_18(2).vhdr",
    "april_19(1)":  r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_19(1)\april_19(1).vhdr",
    "april_19(2)":  r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_19(2)\april_19(2).vhdr",
    "april_22":     r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_22\april_22.vhdr",
    "april_24":     r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_08-04-2026\eeg_april_24\april_24.vhdr",
}

OUTPUT_DIR = Path(r"C:\Users\whyke\github\six-problem\Data")

def extract_and_save(name, filepath):
    print(f"\n{'='*80}")
    print(f"Processing: {name}")
    print(f"{'='*80}")

    lines = []

    try:
        raw = mne.io.read_raw_brainvision(filepath, preload=True, verbose='ERROR')
        lines.append(f"File: {filepath}\n")

        lines.append(f"\n===== RAW INFO =====\n")
        lines.append(f"Sampling rate: {raw.info['sfreq']} Hz\n")
        lines.append(f"Duration: {raw.times[-1]:.2f} sec\n")
        lines.append(f"Channels: {len(raw.ch_names)}\n")

        annotations = raw.annotations
        lines.append(f"\n===== ANNOTATIONS =====\n")
        lines.append(f"Total annotations: {len(annotations)}\n\n")

        df_anno = pd.DataFrame({
            'onset_sec': annotations.onset,
            'duration':  annotations.duration,
            'description': annotations.description
        })
        lines.append(df_anno.head(20).to_string())
        lines.append("\n")

        lines.append(f"\n===== ANNOTATION COUNTS =====\n")
        lines.append(df_anno['description'].value_counts().to_string())
        lines.append("\n")

        events, event_id = mne.events_from_annotations(raw)

        lines.append(f"\n===== EVENT ID =====\n")
        lines.append(str(event_id) + "\n")
        lines.append(f"Total events: {len(events)}\n")

        df_events = pd.DataFrame({
            'sample': events[:, 0],
            'event_code': events[:, 2]
        })
        df_events['time_sec'] = df_events['sample'] / raw.info['sfreq']
        inv_map = {v: k for k, v in event_id.items()}
        df_events['label'] = df_events['event_code'].map(inv_map)

        lines.append(f"\n===== ALL EVENTS =====\n")
        lines.append(df_events[['time_sec', 'label']].to_string())
        lines.append("\n")

        lines.append(f"\n===== EVENT COUNTS =====\n")
        lines.append(df_events['label'].value_counts().to_string())
        lines.append("\n")

        df_events_sorted = df_events.sort_values('time_sec').reset_index(drop=True)
        df_events_sorted['delta_t'] = df_events_sorted['time_sec'].diff()

        lines.append(f"\n===== EVENT TIME DIFFERENCE =====\n")
        lines.append(df_events_sorted[['time_sec', 'label', 'delta_t']].to_string())
        lines.append("\n")

        lines.append(f"\n===== SUMMARY =====\n")
        lines.append(f"Total annotations: {len(df_anno)}\n")
        lines.append(f"Total events: {len(events)}\n")
        lines.append(f"Duration: {raw.times[-1]:.2f} sec\n")

        out_path = OUTPUT_DIR / f"{name}_output.txt"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write("".join(lines))

        print(f"  ✓ Saved: {out_path.name}  ({len(events)} events)")
        return len(events)

    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        out_path = OUTPUT_DIR / f"{name}_output.txt"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(f"[ERROR]\n{str(e)}\n")
        return None


def main():
    print("="*80)
    print("APRIL EEG DATA EXTRACTION  (14 files)")
    print("="*80)

    results = {}
    for name, path in APRIL_FILES.items():
        results[name] = extract_and_save(name, path)

    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    for name, count in results.items():
        status = f"{count} events" if count is not None else "FAILED"
        print(f"  {name:<20} {status}")

if __name__ == "__main__":
    main()
