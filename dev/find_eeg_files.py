#!/usr/bin/env python3
"""找到所有EEG文件"""

import os
import sys
from pathlib import Path

print("=" * 80)
print("EEG文件搜索诊断")
print("=" * 80)

# 需要检查的路径
paths_to_check = [
    "C:\\",
    "D:\\",
    Path.home(),
    Path.cwd(),
]

print("\n当前工作目录:", Path.cwd())
print("\n搜索.vhdr文件...\n")

found_files = []

for base_path in paths_to_check:
    try:
        base = Path(base_path)
        if not base.exists():
            print(f"[SKIP] 不存在: {base_path}")
            continue

        print(f"[搜索] {base_path}")
        # 只搜索前3层，避免太深
        for vhdr_file in base.glob("**/*.vhdr"):
            if vhdr_file.is_file():
                found_files.append(vhdr_file)
                print(f"  ✓ 找到: {vhdr_file}")

    except Exception as e:
        print(f"[错误] {base_path}: {e}")

print("\n" + "=" * 80)
if found_files:
    print(f"\n✓ 找到 {len(found_files)} 个EEG文件\n")
    for f in found_files:
        print(f"复制这个路径:")
        print(f"  {f.parent}")
        print()
else:
    print("\n✗ 没有找到任何.vhdr文件")
    print("\n建议:")
    print("1. 检查EEG文件是否存在")
    print("2. 确认文件格式是否是 .vhdr")
    print("3. 查看文件权限是否允许访问")

print("=" * 80)
