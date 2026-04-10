# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mne
import pandas as pd
from pathlib import Path

filepath = r"C:\Users\whyke\github\six-problem\Data\eeg_aug_05\eeg_aug_05\aug_05.vhdr"
name = "aug_05"

print(f"Processing: {name}")

raw = mne.io.read_raw_brainvision(filepath, preload=True, verbose='ERROR')

output_lines = []
output_lines.append("===== RAW INFO =====\n")
output_lines.append(f"Total annotations: {len(raw.annotations)}\n\n")

df_anno = pd.DataFrame({
    'onset_sec': raw.annotations.onset / raw.info['sfreq'],
    'description': raw.annotations.description
})

output_lines.append("===== ALL ANNOTATIONS (全部) =====\n")
output_lines.append(df_anno.to_string())
output_lines.append("\n")

output_lines.append("\n===== ANNOTATION COUNTS =====\n")
counts = df_anno['description'].value_counts()
output_lines.append(counts.to_string())

events, event_id = mne.events_from_annotations(raw)
output_lines.append(f"\n\n===== EVENT ID =====\n")
output_lines.append(str(event_id))

output_text = "".join(output_lines)
output_path = Path(r"C:\Users\whyke\github\six-problem\Data") / f"{name}_output_full.txt"

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(output_text)

print(f"✓ Output saved: {name}_output_full.txt")
print(f"✓ Total events: {len(events)}")
