#!/usr/bin/env python3
"""
处理September EEG数据
基于完整的被试日志映射生成分析和Excel填充
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from pathlib import Path
from datetime import datetime

# ============================================================================
# 被试日志映射 (来自用户提供的信息)
# ============================================================================

SEPTEMBER_MARKER_MAPPING = {
    "sep_12.vhdr": {
        "recording_date": "2013-09-12",
        "subject_info": "1990 F, Quality",
        "problem_order": ["Cake", "Bin", "Toothbrush", "Workspace", "Fountain", "Metro"],
        "s14_meaning": "Typing (Problem 2)",
        "s15_meaning": "Evaluate WL (Problem 2)",
        "notes": "Standard sequence"
    },
    "sep_12(2).vhdr": {
        "recording_date": "2013-09-12",
        "subject_info": "1987, Anthropology",
        "problem_order": ["Toothbrush", "Workspace", "Cake", "Metro", "Bin", "Fountain"],
        "s14_meaning": "Typing (Problem 2)",
        "s15_meaning": "Evaluate WL (Problem 2)",
        "notes": "Standard sequence"
    },
    "sep_13.vhdr": {
        "recording_date": "2013-09-13",
        "subject_info": "1987, Info Sys Eng",
        "problem_order": ["Metro", "Bin", "Cake", "Brush", "Fountain", "Exercise"],
        "s14_meaning": "Typing (Problem 2)",
        "s15_meaning": "Evaluate WL (Problem 2)",
        "notes": "Standard sequence"
    },
    "sep_13(2).vhdr": {
        "recording_date": "2013-09-13",
        "subject_info": "1987, ECE",
        "problem_order": ["Cake", "Exercise", "Brush", "Bin", "Metro", "Fountain"],
        "s14_meaning": "Typing (Problem 2)",
        "s15_meaning": "Evaluate WL (Problem 2)",
        "notes": "Signal bad, very relax"
    },
    "eeg_sep_18.vhdr": {
        "recording_date": "2013-09-18",
        "subject_info": "1982 F, Management",
        "problem_order": ["Cake", "Exercise", "Fountain", "Bin", "Brush", "Metro"],
        "s14_meaning": "Evaluate Solution (Problem 2)",
        "s15_meaning": "Typing (Problem 2)",
        "notes": "Sequence shifted by +1 due to 'done' marker inserted at marker 10."
    }
}

# 已提取的标记数据
EXTRACTED_DATA = {
    "sep_12.vhdr": {"total_events": 43, "s14_count": 22, "s15_count": 21},
    "sep_12(2).vhdr": {"total_events": 41, "s14_count": None, "s15_count": None},
    "sep_13.vhdr": {"total_events": 42, "s14_count": None, "s15_count": None},
    "sep_13(2).vhdr": {"total_events": 43, "s14_count": None, "s15_count": None},
    "eeg_sep_18.vhdr": {"total_events": 44, "s14_count": None, "s15_count": None},
}

# ============================================================================
# 分析函数
# ============================================================================

def analyze_september_data():
    """分析September数据并生成报告"""

    print("=" * 100)
    print("SEPTEMBER EEG DATA ANALYSIS - 基于完整的被试日志映射")
    print("=" * 100)

    print("\n[被试信息总结]")
    print("-" * 100)

    for filename, mapping in SEPTEMBER_MARKER_MAPPING.items():
        extracted = EXTRACTED_DATA.get(filename, {})

        print(f"\n{filename}")
        print(f"  日期: {mapping['recording_date']}")
        print(f"  被试: {mapping['subject_info']}")
        print(f"  问题顺序: {' → '.join(mapping['problem_order'])}")
        print(f"  标记映射:")
        print(f"    S 14 = {mapping['s14_meaning']}")
        print(f"    S 15 = {mapping['s15_meaning']}")
        print(f"  提取数据:")
        print(f"    总事件数: {extracted.get('total_events', '?')} 个")
        if extracted.get('s14_count'):
            print(f"    S 14 计数: {extracted['s14_count']}")
            print(f"    S 15 计数: {extracted['s15_count']}")
        print(f"  备注: {mapping['notes']}")

    print("\n" + "=" * 100)
    print("[标记含义统计]")
    print("-" * 100)

    s14_meanings = {}
    s15_meanings = {}

    for mapping in SEPTEMBER_MARKER_MAPPING.values():
        s14 = mapping['s14_meaning']
        s15 = mapping['s15_meaning']

        s14_meanings[s14] = s14_meanings.get(s14, 0) + 1
        s15_meanings[s15] = s15_meanings.get(s15, 0) + 1

    print("\nS 14 含义分布:")
    for meaning, count in s14_meanings.items():
        print(f"  {meaning:30} - {count} 个被试")

    print("\nS 15 含义分布:")
    for meaning, count in s15_meanings.items():
        print(f"  {meaning:30} - {count} 个被试")

    print("\n" + "=" * 100)
    print("[关键观察]")
    print("-" * 100)

    print("""
1. 标记模式理解:
   - S 14 和 S 15 对应"问题2"的认知流程
   - 根据被试日志，标记位置基于实验进程

2. 被试特征:
   - 4个被试在同一天/相邻天进行实验
   - 背景多样化 (设计、人类学、工程、管理等)
   - 2个被试是女性，3个推断为男性

3. 特殊情况:
   - sep_13(2): 信号差，被试状态放松
   - sep_18: 标记序列向后移了1位 (插入'done'标记)

4. 问题顺序:
   - 6个问题随机分配给每个被试
   - 总共6个标准设计题目
   - 有助于控制顺序效应
""")

    print("=" * 100)
    print("[下一步]")
    print("-" * 100)
    print("""
✓ 标记映射已完成
✓ 被试信息已获得
✓ 问题顺序已确认

现在可以:
  1. 创建完整的标记-认知映射
  2. 根据标记含义分段EEG数据
  3. 填充EEG_Segmentation.xlsx
  4. 生成详细的分析报告
""")

    print("=" * 100)

    # 导出为JSON供后续使用
    import json
    output = {
        'timestamp': datetime.now().isoformat(),
        'data_source': 'September 2013 EEG Recordings',
        'total_subjects': len(SEPTEMBER_MARKER_MAPPING),
        'subjects': SEPTEMBER_MARKER_MAPPING,
        'extracted_summary': EXTRACTED_DATA
    }

    with open('september_data_complete_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n✓ 映射数据已导出: september_data_complete_mapping.json")
    print("=" * 100)

if __name__ == "__main__":
    analyze_september_data()
