#!/usr/bin/env python3
"""
标记映射框架 - 用于六问题认知研究EEG数据

基于用户提供的信息:
- 标记是顺序递增的事件Trigger (Sequential Event Markers)
- S 14, S 15的具体含义需要查看被试日志
- 每个被试都有独特的时间线和问题顺序
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

# ============================================================================
# 数据结构定义
# ============================================================================

@dataclass
class MarkerSequenceInfo:
    """标记序列信息"""
    subject_id: str
    file_name: str
    recording_date: Optional[str] = None
    s14_meaning: Optional[str] = None  # 需要从日志查找
    s15_meaning: Optional[str] = None  # 需要从日志查找
    problem_order: Optional[str] = None  # e.g., "3,1,6,2,5,4"
    notes: Optional[str] = None

@dataclass
class ExtractedMarkerData:
    """提取的标记数据"""
    file_name: str
    total_events: int
    s14_count: int
    s15_count: int
    duration_sec: float
    sampling_rate: float
    channels: int

# ============================================================================
# September数据信息
# ============================================================================

SEPTEMBER_DATA = {
    'sep_12.vhdr': ExtractedMarkerData(
        file_name='sep_12.vhdr',
        total_events=43,
        s14_count=22,
        s15_count=21,
        duration_sec=5612.21,
        sampling_rate=500.0,
        channels=63
    ),
    'sep_12(2).vhdr': ExtractedMarkerData(
        file_name='sep_12(2).vhdr',
        total_events=41,
        s14_count=None,  # 需要计算
        s15_count=None,
        duration_sec=2347.34,
        sampling_rate=500.0,
        channels=63
    ),
    'sep_13.vhdr': ExtractedMarkerData(
        file_name='sep_13.vhdr',
        total_events=42,
        s14_count=None,
        s15_count=None,
        duration_sec=4562.686,
        sampling_rate=500.0,
        channels=63
    ),
    'sep_13(2).vhdr': ExtractedMarkerData(
        file_name='sep_13(2).vhdr',
        total_events=43,
        s14_count=None,
        s15_count=None,
        duration_sec=2662.962,
        sampling_rate=500.0,
        channels=63
    ),
    'eeg_sep_18.vhdr': ExtractedMarkerData(
        file_name='eeg_sep_18.vhdr',
        total_events=44,
        s14_count=None,
        s15_count=None,
        duration_sec=5370.416,
        sampling_rate=500.0,
        channels=63
    ),
}

# ============================================================================
# 六问题实验的标准认知流程
# ============================================================================

STANDARD_COGNITIVE_SEQUENCE = """
标准化认知循环 (对每个设计问题):
  1. Read problem          - 阅读并理解设计要求
  2. Generate solution     - 生成解决方案并绘制草图
  3. Evaluate WL (前)      - 评估当前的脑力负荷
  4. Evaluate solution     - 评估自己生成方案的质量
  5. Typing                - 打字输入设计说明或想法
  6. Evaluate WL (后)      - 任务结束后的脑力负荷评估

6个设计问题 (随机分配顺序):
  1. Cake               - 儿童旋转蛋糕相关
  2. Recycle bin        - 垃圾回收桶
  3. Toothbrush         - 牙刷/牙膏相关
  4. Metro/Wheelchair   - 无障碍设计
  5. Workspace+Exercise - 结合锻炼的办公空间
  6. Drinking fountain  - 饮水机

记录类型 (EEG + 生理数据):
  - EEG (脑电图)
  - HRV (心率变异性)
  - GSR (皮肤电)
  - 眼动追踪
"""

# ============================================================================
# 标记映射示例 (来自用户提供的笔记)
# ============================================================================

MARKER_MAPPING_EXAMPLES = {
    "example_1_2013_04_15": {
        "description": "2013年4月15日实验",
        "s14": "开始构思/画图 (Start Solution)",
        "s15": "完成构思 (Finish Solution)"
    },
    "example_2_2013_04_24": {
        "description": "2013年4月24日实验",
        "s14": "评估方案 (Evaluate)",
        "s15": "打字记录 (Typing)"
    },
    "example_3_later_studies": {
        "description": "后期研究中",
        "s14_s15_pattern": "经常被用来标定'评估解决方案'或'生成方案的评分'这一特定时间段",
        "note": "具体含义需要查看对应的被试日志"
    }
}

# ============================================================================
# 标记映射框架
# ============================================================================

class MarkerMappingFramework:
    """标记映射框架 - 为每个被试建立日志查找表"""

    def __init__(self):
        self.subject_mappings = {}
        self.unknown_mappings = []

    def add_subject_mapping(self, mapping_info: MarkerSequenceInfo):
        """添加被试的标记映射"""
        self.subject_mappings[mapping_info.file_name] = mapping_info

    def add_unknown_subject(self, file_name: str):
        """标记为需要查找日志的被试"""
        self.unknown_mappings.append(file_name)

    def generate_lookup_table(self) -> Dict:
        """生成日志查找表"""
        lookup = {}
        for file_name in SEPTEMBER_DATA.keys():
            lookup[file_name] = {
                'status': 'NEED_LOG_LOOKUP',
                'fields_needed': ['recording_date', 's14_meaning', 's15_meaning', 'problem_order'],
                'example_values': {
                    'recording_date': '2013-09-12',
                    's14_meaning': '开始构思 或 评估方案',
                    's15_meaning': '完成构思 或 打字记录',
                    'problem_order': '3,1,6,2,5,4'
                }
            }
        return lookup

    def export_to_json(self, file_path: str):
        """导出映射信息为JSON"""
        data = {
            'framework': 'Marker Mapping for 6-Problem Design Cognition Study',
            'extraction_status': 'PARTIAL - Awaiting Subject Logs',
            'september_data': {
                fname: asdict(edata)
                for fname, edata in SEPTEMBER_DATA.items()
            },
            'required_lookups': self.generate_lookup_table(),
            'known_examples': MARKER_MAPPING_EXAMPLES,
            'standard_sequence': STANDARD_COGNITIVE_SEQUENCE
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

# ============================================================================
# 演示和输出
# ============================================================================

def main():
    print("=" * 80)
    print("MARKER MAPPING FRAMEWORK - 六问题认知研究")
    print("=" * 80)

    print("\n[现状分析]")
    print("-" * 80)
    print("✅ 已提取的数据:")
    for fname, edata in SEPTEMBER_DATA.items():
        print(f"  {fname:20} - {edata.total_events} events (S14:{edata.s14_count}, S15:{edata.s15_count})")

    print("\n⏳ 需要被试日志确定:")
    for fname in SEPTEMBER_DATA.keys():
        print(f"  {fname:20} - S14含义, S15含义, 问题顺序, 日期")

    print("\n[标准认知流程]")
    print("-" * 80)
    print(STANDARD_COGNITIVE_SEQUENCE)

    print("\n[已知的映射示例]")
    print("-" * 80)
    for key, example in MARKER_MAPPING_EXAMPLES.items():
        print(f"\n{key}:")
        for k, v in example.items():
            print(f"  {k}: {v}")

    print("\n[现在需要做的]")
    print("-" * 80)
    print("""
1. 找到被试日志 (Log簿 或 实验记录):
   - 对于 sep_12.vhdr, sep_12(2).vhdr: 2013年9月12日的记录
   - 对于 sep_13.vhdr, sep_13(2).vhdr: 2013年9月13日的记录
   - 对于 eeg_sep_18.vhdr: 2013年9月18日的记录

2. 从日志中提取 (对每个被试):
   - 被试ID
   - 问题顺序编号 (6个问题的随机排列)
   - S 14 对应的认知阶段 (例: "开始构思")
   - S 15 对应的认知阶段 (例: "完成构思")
   - 其他相关元数据

3. 使用这些信息:
   - 创建完整的标记-认知映射
   - 填充 EEG_Segmentation.xlsx
   - 生成详细的分析报告
    """)

    print("\n[导出信息]")
    print("-" * 80)
    framework = MarkerMappingFramework()
    for fname in SEPTEMBER_DATA.keys():
        framework.add_unknown_subject(fname)

    output_file = Path("marker_mapping_lookup_table.json")
    framework.export_to_json(str(output_file))
    print(f"✓ 导出查找表: {output_file}")
    print(f"  (包含所有5个被试的日志查找指南)")

    print("\n" + "=" * 80)
    print("等待被试日志信息...")
    print("=" * 80)

if __name__ == "__main__":
    main()
