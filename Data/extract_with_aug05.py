# -*- coding: utf-8 -*-
"""
提取August和September的数据进行对比
Extract August and September data for comparison
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mne
import pandas as pd
from pathlib import Path

# ============================================================================
# 文件列表 - August + September
# ============================================================================

FILES_TO_EXTRACT = {
    # August - 作为参考
    "aug_05": r"C:\Users\whyke\github\six-problem\Data\eeg_aug_05\eeg_aug_05.vhdr",

    # September
    "sep_12(2)": r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026\eeg_sep_12(2)\sep_12(2).vhdr",
    "sep_12": r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026\eeg_sep_12\sep_12.vhdr",
    "sep_13(2)": r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026\eeg_sep_13(2)\sep_13(2).vhdr",
    "sep_13": r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026\eeg_sep_13\sep_13.vhdr",
    "eeg_sep_18": r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026\eeg_sep_18\eeg_sep_18.vhdr",
}

# ============================================================================
# 提取函数
# ============================================================================

def extract_and_save(name, filepath):
    """提取单个文件的数据并保存"""

    print(f"\n{'='*100}")
    print(f"Processing: {name}")
    print(f"{'='*100}")

    output_lines = []

    try:
        # 加载EEG
        print(f"  加载文件...")
        raw = mne.io.read_raw_brainvision(filepath, preload=True, verbose='ERROR')
        output_lines.append(f"✓ Successfully loaded: {filepath}\n")

        # RAW信息
        output_lines.append("\n===== RAW INFO =====\n")
        output_lines.append(f"Sampling rate: {raw.info['sfreq']} Hz\n")
        output_lines.append(f"Duration: {raw.times[-1]:.2f} sec\n")
        output_lines.append(f"Channels: {len(raw.ch_names)}\n")

        # Annotations
        annotations = raw.annotations
        output_lines.append(f"\n===== ANNOTATIONS (前30个) =====\n")
        output_lines.append(f"Total annotations: {len(annotations)}\n\n")

        df_anno = pd.DataFrame({
            'onset_sec': annotations.onset / raw.info['sfreq'],
            'duration': annotations.duration,
            'description': annotations.description
        })

        output_lines.append(df_anno.head(30).to_string())
        output_lines.append("\n")

        # 计数
        output_lines.append(f"\n===== ANNOTATION COUNTS =====\n")
        counts = df_anno['description'].value_counts()
        output_lines.append(counts.to_string())
        output_lines.append("\n")

        # Events
        events, event_id = mne.events_from_annotations(raw)
        output_lines.append(f"\n===== EVENT ID =====\n")
        output_lines.append(str(event_id))
        output_lines.append(f"\nTotal events: {len(events)}\n")

        # Events DataFrame
        df_events = pd.DataFrame({
            'sample': events[:, 0],
            'event_code': events[:, 2]
        })
        df_events['time_sec'] = df_events['sample'] / raw.info['sfreq']

        inv_map = {v: k for k, v in event_id.items()}
        df_events['label'] = df_events['event_code'].map(inv_map)

        output_lines.append(f"\n===== ALL EVENTS (按时间) =====\n")
        output_lines.append(df_events[['time_sec', 'label']].to_string())
        output_lines.append("\n")

        # 汇总
        output_lines.append(f"\n===== SUMMARY =====\n")
        output_lines.append(f"Total annotations: {len(df_anno)}\n")
        output_lines.append(f"Total events: {len(events)}\n")
        output_lines.append(f"Duration: {raw.times[-1]:.2f} sec\n")

        # 保存到文件
        output_text = "".join(output_lines)
        output_filename = f"{name}_output_full.txt"
        output_path = Path(r"C:\Users\whyke\github\six-problem\Data") / output_filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_text)

        print(f"  ✓ Output saved: {output_filename}")
        print(f"  ✓ Total events: {len(events)}")

        # 返回关键信息
        return {
            'name': name,
            'total_events': len(events),
            'counts': counts.to_dict(),
            'event_id': event_id
        }

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

# ============================================================================
# 主程序
# ============================================================================

def main():
    print("="*100)
    print("EEG DATA EXTRACTION WITH AUGUST REFERENCE")
    print("="*100)

    results = {}

    for name, filepath in FILES_TO_EXTRACT.items():
        result = extract_and_save(name, filepath)
        if result:
            results[name] = result

    # 生成对比报告
    print("\n" + "="*100)
    print("COMPARISON SUMMARY")
    print("="*100)

    if 'aug_05' in results:
        print("\n【AUGUST REFERENCE (参考)】")
        aug = results['aug_05']
        print(f"  File: aug_05")
        print(f"  Total events: {aug['total_events']}")
        print(f"  Marker types: {dict(aug['counts'])}")

    print("\n【SEPTEMBER DATA (要填充的)】")
    for name in ['sep_12(2)', 'sep_12', 'sep_13(2)', 'sep_13', 'eeg_sep_18']:
        if name in results:
            sep = results[name]
            print(f"\n  {name}:")
            print(f"    Total events: {sep['total_events']}")
            print(f"    Markers: {dict(sep['counts'])}")

    print("\n" + "="*100)

if __name__ == "__main__":
    main()
