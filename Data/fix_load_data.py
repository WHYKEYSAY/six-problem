import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import argparse
import json
import mne
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--path", required=True)
parser.add_argument("--label-map", required=True)
parser.add_argument("--no-plot", action="store_true")
args = parser.parse_args()

label_map = json.loads(args.label_map)
label_map = {int(k): v for k, v in label_map.items()}

def format_hms(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:05.2f}"
    return f"{m:02d}:{s:05.2f}"

raw = mne.io.read_raw_brainvision(args.path, preload=True)
print("Extracting parameters from", args.path)
raw.rename_channels(lambda x: x.strip().upper())

print("\n===== ANNOTATIONS =====")
annotations = raw.annotations
print("Total annotations:", len(annotations))
df_anno = pd.DataFrame({'onset_sec': annotations.onset, 'duration': annotations.duration, 'description': annotations.description})
print(df_anno.head(20))

print("\n===== ANNOTATION COUNTS =====")
print(df_anno['description'].value_counts())

events, event_id = mne.events_from_annotations(raw)
inv_map = {v: k for k, v in event_id.items()}
stim_events = [ev for ev in events if 'Stimulus' in inv_map[ev[2]] or inv_map[ev[2]].startswith('S')]

df_events = pd.DataFrame({
    'time_sec': [ev[0] / raw.info['sfreq'] for ev in stim_events],
    'label': [inv_map[ev[2]] for ev in stim_events]
})
print("\nTotal events:", len(df_events))

df_events = df_events.sort_values('time_sec').reset_index(drop=True)
df_events['duration_sec'] = df_events['time_sec'].diff()
df_events.loc[0, 'duration_sec'] = df_events.iloc[0]['time_sec']

df_events['Proposed Label'] = ""
for idx, lbl in label_map.items():
    if 1 <= idx <= len(df_events):
        df_events.at[idx-1, 'Proposed Label'] = lbl

df_events['time_hms'] = df_events['time_sec'].apply(format_hms)
df_events['dur_hms'] = df_events['duration_sec'].apply(format_hms)

df_events_disp = df_events.copy()
df_events_disp.index = df_events_disp.index + 1

print("\n===== FIRST 30 EVENTS (HUMAN READABLE) =====")
print(df_events_disp[['time_hms', 'label', 'dur_hms', 'Proposed Label']].head(30))

print("\n===== EVENT COUNTS =====")
print(df_events['label'].value_counts())

print("\n===== FULL EVENTS LIST (WITH DURATION & LABELS) =====")
print(df_events_disp[['time_hms', 'label', 'dur_hms', 'Proposed Label']])

print("\n===== SUMMARY =====")
print(f"Total annotations: {len(df_anno)}")
print(f"Unique event types: {len(event_id)}")
print(f"Total events: {len(df_events)}")
print(f"Recording length: {raw.times[-1]:.2f} sec")
