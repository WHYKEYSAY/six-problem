import mne
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ======================================
# 1. 文件路径
# ======================================
file_path = r"D:\Six problem\six-problem\six-problem\EEG_six_problem\eeg_april_02(1)\april_2(1).vhdr"
locs_path = r"C:\Users\umroot\Downloads\Cap63 (1).locs"

# ======================================
# 2. 读取 EEG
# ======================================
raw = mne.io.read_raw_brainvision(file_path, preload=True)

print("\n===== RAW INFO =====")
print(raw)
print("\nSampling rate:", raw.info['sfreq'])
print("Duration (sec):", raw.times[-1])
print("Channels:", len(raw.ch_names))

print("\nChannel names:")
print(raw.ch_names)

# ======================================
# 3. 设置 montage（你的63通道cap）
# ======================================
print("\n===== LOADING LOCS =====")

# 通道名统一（避免不匹配）
raw.rename_channels(lambda x: x.strip().upper())

montage = mne.channels.read_custom_montage(locs_path)

raw.set_montage(montage, on_missing='ignore')

print("Montage loaded successfully!")

# 可视化电极位置（强烈建议看）
raw.plot_sensors(show_names=True)

# ======================================
# 4. 查看 annotations（最原始 marker）
# ======================================
print("\n===== ANNOTATIONS =====")

annotations = raw.annotations
print("Total annotations:", len(annotations))

df_anno = pd.DataFrame({
    'onset_sec': annotations.onset,
    'duration': annotations.duration,
    'description': annotations.description
})

print(df_anno.head(20))

# ======================================
# 5. annotation 类型统计
# ======================================
print("\n===== ANNOTATION COUNTS =====")
print(df_anno['description'].value_counts())

# ======================================
# 6. 转换为 events
# ======================================
events, event_id = mne.events_from_annotations(raw)

print("\n===== EVENT ID =====")
print(event_id)

print("\nTotal events:", len(events))

# ======================================
# 7. events DataFrame
# ======================================
df_events = pd.DataFrame({
    'sample': events[:, 0],
    'event_code': events[:, 2]
})

df_events['time_sec'] = df_events['sample'] / raw.info['sfreq']

# 反向映射 label
inv_map = {v: k for k, v in event_id.items()}
df_events['label'] = df_events['event_code'].map(inv_map)

print("\n===== FIRST 30 EVENTS =====")
print(df_events.head(30))

# ======================================
# 8. 每种 event 数量
# ======================================
print("\n===== EVENT COUNTS =====")
print(df_events['label'].value_counts())

# ======================================
# 9. 时间间隔分析（判断是否是 trial）
# ======================================
print("\n===== EVENT TIME DIFFERENCE =====")

df_events = df_events.sort_values('time_sec').reset_index(drop=True)
df_events['delta_t'] = df_events['time_sec'].diff()

print(df_events[['time_sec', 'label', 'delta_t']].head(30))

# ======================================
# 10. 可视化 event 分布
# ======================================
plt.figure(figsize=(12,4))
plt.scatter(df_events['time_sec'], df_events['label'], s=10)
plt.xlabel("Time (sec)")
plt.ylabel("Event label")
plt.title("Event distribution over time")
plt.show()

# ======================================
# 11. 判断是否有分段（block / trial）
# ======================================
print("\n===== CHECK SEGMENTATION =====")

if any(df_anno['duration'] > 0):
    print("⚠️ 存在持续时间 annotation（可能是block或trial）")
else:
    print("✔ 没有持续时间 annotation（只有marker）")

# ======================================
# 12. 判断是否有trial结构
# ======================================
print("\n===== TRIAL STRUCTURE CHECK =====")

counts = df_events['label'].value_counts()

print("Top event candidates:")
print(counts.head())

print("\n👉 判断逻辑：")
print("如果某个event重复 ≈ 20–30次 → 很可能是 trial start")

# ======================================
# 13. 自动找可能的trial marker（辅助）
# ======================================
candidate_trials = counts[counts > 10]
print("\nPotential trial markers:")
print(candidate_trials)

# ======================================
# 14. 输出总结
# ======================================
print("\n===== SUMMARY =====")
print(f"Total annotations: {len(df_anno)}")
print(f"Unique event types: {len(event_id)}")
print(f"Total events: {len(events)}")
print(f"Recording length: {raw.times[-1]:.2f} sec")