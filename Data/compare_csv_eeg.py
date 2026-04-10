# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import csv, re
from pathlib import Path

DATA_DIR = Path(r'C:\Users\whyke\github\six-problem\Data')

# Parse CSV
csv_data = {}
with open(DATA_DIR / 'EEG_Segmentation(Sheet1).csv', encoding='latin-1') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        if not row[0]:
            continue
        name = row[0].strip()
        if 'april' not in name.lower():
            continue
        total = row[1].strip()
        markers = [x.strip() for x in row[3:] if x.strip()]
        csv_data[name] = {'total': total, 'markers': [int(m) for m in markers if m.isdigit()]}

# Map CSV name -> output file name
april_map = {
    'april_02(3).xlsx': 'april_02(3)',
    'april_04(1).xlsx': 'april_04(1)',
    'April_04(2).xlsx': 'april_04(2)',
    'april_08.xlsx':    'april_08',
    'April_15.xlsx':    'april_15',
    'April_16(1).xlsx': 'april_16(1)',
    'april_16(3).xlsx': 'april_16(3)',
    'april_18(1).xlsx': 'april_18(1)',
    'april_18(2).xlsx': 'april_18(2)',
    'april_19(1).xlsx': 'april_19(1)',
    'April_19(2).xlsx': 'april_19(2)',
    'April_2(1).xlsx':  'april_02(1)',
    'april_22.xlsx':    'april_22',
    'april_24.xlsx':    'april_24',
}

print("=" * 100)
print("CSV vs EEG EXTRACTION COMPARISON (April files)")
print("=" * 100)
print(f"{'File':<22} {'CSV total':>9} {'EEG events':>10}  {'Total match':>11}  {'CSV markers':>12}  Notes")
print("-" * 100)

all_ok = True
details = []

for csv_name, eeg_name in april_map.items():
    d = csv_data.get(csv_name, {})
    csv_total = d.get('total', '?')
    csv_markers = d.get('markers', [])

    # Read EEG output file
    out_file = DATA_DIR / f'{eeg_name}_output.txt'
    eeg_count = None
    eeg_labels = []
    if out_file.exists():
        txt = out_file.read_text(encoding='utf-8')
        m = re.search(r'Total events: (\d+)', txt)
        if m:
            eeg_count = int(m.group(1))
        # Extract all event labels from ALL EVENTS section
        section = re.search(r'===== ALL EVENTS =====\n(.*?)\n===== EVENT COUNTS', txt, re.DOTALL)
        if section:
            for line in section.group(1).strip().split('\n'):
                parts = line.strip().split()
                if len(parts) >= 3:
                    eeg_labels.append(parts[-1])  # last column = label (S14 or S15)

    total_match = '✓' if str(csv_total) == str(eeg_count) else 'MISMATCH'
    if total_match != '✓':
        all_ok = False

    note = ""
    if eeg_count is not None and str(csv_total) != str(eeg_count):
        note = f"CSV={csv_total} but EEG={eeg_count}"

    print(f"{csv_name:<22} {str(csv_total):>9} {str(eeg_count or '?'):>10}  {total_match:>11}  {len(csv_markers):>12}  {note}")

    details.append({
        'name': csv_name,
        'csv_total': csv_total,
        'eeg_count': eeg_count,
        'csv_markers': csv_markers,
        'eeg_labels': eeg_labels,
    })

print()
print("=" * 100)
print("DETAIL: CSV marker sequences vs expected sequential pattern")
print("=" * 100)

for d in details:
    name = d['name']
    csv_m = d['csv_markers']
    eeg_n = d['eeg_count']

    if not csv_m:
        print(f"\n{name}: No markers in CSV")
        continue

    # Check if CSV markers are sequential
    gaps = []
    for i in range(1, len(csv_m)):
        if csv_m[i] != csv_m[i-1] + 1:
            gaps.append((csv_m[i-1], csv_m[i]))

    expected_count = 38  # 6 problems x 6 stages + 2 eye_closed
    col_count = len(csv_m)

    print(f"\n{name}:")
    print(f"  CSV marker range: {csv_m[0]} - {csv_m[-1]}  ({col_count} markers)")
    print(f"  EEG total events: {eeg_n}")
    if gaps:
        missing = []
        for (a, b) in gaps:
            missing.extend(range(a+1, b))
        print(f"  Gaps in CSV markers (missing): {missing}")
    else:
        print(f"  Markers are fully sequential (no gaps)")

print()
if all_ok:
    print("RESULT: All total_event counts match between CSV and EEG extraction.")
else:
    print("RESULT: Some total_event counts DO NOT match - see MISMATCH rows above.")
